from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
from app.models import db, Form, User

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AdmissionForm(FlaskForm):
    birth_date = DateField('Tanggal Lahir', 
                          validators=[DataRequired()],
                          render_kw={"type": "text", "readonly": "readonly"})  # Changed this line
    address = TextAreaField('Address', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    previous_school = StringField('Previous School', validators=[DataRequired()])
    
    nisn = StringField('NISN', validators=[DataRequired()])
    akta_kelahiran = FileField('Akta Kelahiran', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'File harus berformat PDF, PNG, atau JPG!')
    ])
    kartu_keluarga = FileField('Kartu Keluarga', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'File harus berformat PDF, PNG, atau JPG!')
    ])
    ijazah_smp = FileField('Ijazah/SKL SMP', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'File harus berformat PDF, PNG, atau JPG!')
    ])
    foto_siswa = FileField('Foto 3x4', validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg'], 'File harus berformat PNG atau JPG!')
    ])
    ktp_ortu = FileField('KTP Orang Tua', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'File harus berformat PDF, PNG, atau JPG!')
    ])
    nilai_rapor = FileField('Nilai Rapor', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'File harus berformat PDF, PNG, atau JPG!')
    ])
    sertifikat_prestasi = FileField('Sertifikat Prestasi', validators=[
        Optional(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'File harus berformat PDF, PNG, atau JPG!')
    ])

@main.route('/')
def index():
    return render_template('landing_page.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        forms = Form.query.all()
        return render_template('dashboard_admin.html', forms=forms)
    
    form = AdmissionForm()
    user_form = Form.query.filter_by(user_id=current_user.id).first()
    form_status = user_form.status if user_form else None
    form_submitted = user_form
    
    # Calculate age if birth_date exists
    age = None
    if user_form and user_form.parsed_form_data.get('birth_date'):
        birth_date = datetime.strptime(user_form.parsed_form_data['birth_date'], '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    return render_template('dashboard_user.html',
                         form=form,
                         form_status=form_status,
                         form_submitted=form_submitted,
                         age=age,
                         now=datetime.now())

@main.route('/submit-form', methods=['POST'])
@login_required
def submit_form():
    if current_user.role == 'admin':
        return redirect(url_for('main.dashboard'))
    
    form = AdmissionForm()
    if form.validate_on_submit():
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            uploaded_files = {}
            for field_name in ['akta_kelahiran', 'kartu_keluarga', 'ijazah_smp', 
                             'foto_siswa', 'ktp_ortu', 'nilai_rapor', 'sertifikat_prestasi']:
                file = getattr(form, field_name).data
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user.id}_{field_name}_{file.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    uploaded_files[field_name] = filename
            
            form_data = {
                'birth_date': form.birth_date.data.strftime('%Y-%m-%d'),
                'address': form.address.data,
                'phone': form.phone.data,
                'previous_school': form.previous_school.data,
                'nisn': form.nisn.data
            }
            
            new_form = Form(
                user_id=current_user.id,
                form_data=json.dumps(form_data),
                status='pending',
                **uploaded_files
            )
            
            db.session.add(new_form)
            db.session.commit()
            
            flash('Your application has been submitted successfully!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting application: {str(e)}', 'danger')
            return redirect(url_for('main.dashboard'))
    
    # If form validation fails, show errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {field}: {error}', 'danger')
    
    return redirect(url_for('main.dashboard'))

@main.route('/update-status/<int:form_id>', methods=['POST'])
@login_required
def update_status(form_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))
    
    form = Form.query.get_or_404(form_id)
    new_status = request.form.get('status')
    
    if new_status in ['accepted', 'rejected']:
        form.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}', 'success')
    
    return redirect(url_for('main.dashboard'))

@main.route('/form-details/<int:form_id>')
@login_required
def form_details(form_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))
    
    form = Form.query.get_or_404(form_id)
    return jsonify({
        'user': form.user.name,
        'form_data': json.loads(form.form_data),
        'status': form.status,
        'timestamp': form.timestamp.strftime('%Y-%m-%d %H:%M')
    })
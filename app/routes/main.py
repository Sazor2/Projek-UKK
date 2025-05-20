from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Optional
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
from app.models import db, Form, User

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename, types=None):
    if types is None:
        types = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in types

class AdmissionForm(FlaskForm):
    birth_date = DateField('Tanggal Lahir', 
                          validators=[DataRequired()],
                          render_kw={"type": "text", "readonly": "readonly"})  # Changed this line
    address = TextAreaField('Address', validators=[DataRequired()])
    phone = StringField('Nomor Telepon', 
        validators=[
            DataRequired(message='Nomor telepon wajib diisi'),
            Regexp('^[0-9]{10,13}$', message='Nomor telepon harus 10-13 digit angka')
        ]
    )
    previous_school = StringField('Asal Sekolah', 
        validators=[
            DataRequired(message='Asal sekolah wajib diisi'),
            Length(min=3, max=100, message='Nama sekolah harus antara 3-100 karakter')
        ]
    )
    
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
    gender = SelectField('Jenis Kelamin', 
                      choices=[
                          ('', 'Pilih Jenis Kelamin'),
                          ('L', 'Laki-laki'),
                          ('P', 'Perempuan')
                      ],
                      validators=[DataRequired()])
                      
    jurusan = SelectField('Pilihan Jurusan',
                       choices=[
                           ('', 'Pilih Jurusan'),
                           ('ipa', 'IPA (Ilmu Pengetahuan Alam)'),
                           ('ips', 'IPS (Ilmu Pengetahuan Sosial)')
                       ],
                       validators=[DataRequired()])

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
    
    # Pre-fill form jika ada data tersimpan
    if user_form and user_form.parsed_form_data:
        form_data = user_form.parsed_form_data
        form.nisn.data = form_data.get('nisn')
        try:
            form.birth_date.data = datetime.strptime(form_data.get('birth_date'), '%Y-%m-%d')
        except (ValueError, TypeError):
            form.birth_date.data = None
        form.address.data = form_data.get('address')
        form.phone.data = form_data.get('phone')
        form.previous_school.data = form_data.get('previous_school')
        form.gender.data = form_data.get('gender')
        form.jurusan.data = form_data.get('jurusan')
    
    return render_template('dashboard_user.html',
                         form=form,
                         form_status=form_status,
                         form_submitted=user_form,
                         now=datetime.now())

@main.route('/submit-form', methods=['POST'])
@login_required
def submit_form():
    form = AdmissionForm()
    if form.validate_on_submit():
        try:
            # Cek apakah user sudah submit
            existing_form = Form.query.filter_by(user_id=current_user.id).first()
            if existing_form:
                flash('Anda sudah mengirimkan pendaftaran sebelumnya', 'error')
                return redirect(url_for('main.dashboard'))

            # Buat folder uploads jika belum ada
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Simpan data formulir
            form_data = {
                'birth_date': form.birth_date.data.strftime('%Y-%m-%d'),
                'address': form.address.data.strip(),
                'phone': form.phone.data.strip(),
                'previous_school': form.previous_school.data.strip(),
                'nisn': form.nisn.data.strip(),
                'gender': form.gender.data,
                'jurusan': form.jurusan.data
            }
            
            # Proses file yang diunggah
            uploaded_files = {}
            required_files = {
                'foto_siswa': ['png', 'jpg', 'jpeg'],
                'akta_kelahiran': ['pdf', 'png', 'jpg', 'jpeg'],
                'kartu_keluarga': ['pdf', 'png', 'jpg', 'jpeg'],
                'ijazah_smp': ['pdf', 'png', 'jpg', 'jpeg'],
                'ktp_ortu': ['pdf', 'png', 'jpg', 'jpeg'],
                'nilai_rapor': ['pdf', 'png', 'jpg', 'jpeg']
            }

            # Validasi dan simpan file
            for field_name, allowed_types in required_files.items():
                file = getattr(form, field_name).data
                if not file:
                    flash(f'{field_name.replace("_", " ").title()} wajib diunggah', 'error')
                    return redirect(url_for('main.dashboard'))
                
                if not allowed_file(file.filename, set(allowed_types)):
                    flash(f'Format file {field_name.replace("_", " ").title()} tidak sesuai', 'error')
                    return redirect(url_for('main.dashboard'))
                
                try:
                    filename = secure_filename(f"{current_user.id}_{field_name}_{file.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    uploaded_files[field_name] = filename
                except Exception as e:
                    flash(f'Gagal mengunggah {field_name.replace("_", " ").title()}: {str(e)}', 'error')
                    return redirect(url_for('main.dashboard'))

            # Handle sertifikat prestasi (opsional)
            if form.sertifikat_prestasi.data:
                file = form.sertifikat_prestasi.data
                if allowed_file(file.filename, {'pdf', 'png', 'jpg', 'jpeg'}):
                    filename = secure_filename(f"{current_user.id}_sertifikat_prestasi_{file.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    uploaded_files['sertifikat_prestasi'] = filename

            # Buat entri form baru
            new_form = Form(
                user_id=current_user.id,
                form_data=json.dumps(form_data),
                status='pending',
                **uploaded_files
            )
            
            db.session.add(new_form)
            db.session.commit()
            
            flash('Pendaftaran berhasil! Silakan lakukan pembayaran', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error saat mengirim pendaftaran: {str(e)}', 'error')
            return redirect(url_for('main.dashboard'))
    
    # Tampilkan semua error validasi
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
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

@main.route('/payment/<int:form_id>')
@login_required
def payment(form_id):
    form = Form.query.get_or_404(form_id)
    if form.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
    return render_template('payment.html', form=form)

@main.route('/upload-payment/<int:form_id>', methods=['POST'])
@login_required
def upload_payment(form_id):
    form = Form.query.get_or_404(form_id)
    if form.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
        
    if 'payment_proof' not in request.files:
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('main.payment', form_id=form_id))
        
    file = request.files['payment_proof']
    if file.filename == '':
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('main.payment', form_id=form_id))
        
    if file and allowed_file(file.filename, {'png', 'jpg', 'jpeg'}):
        filename = secure_filename(f"{current_user.id}_payment_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        form.payment_proof = filename
        form.payment_status = 'paid'
        db.session.commit()
        
        flash('Bukti pembayaran berhasil diunggah', 'success')
        return redirect(url_for('main.dashboard'))
        
    flash('Format file tidak diizinkan', 'error')
    return redirect(url_for('main.payment', form_id=form_id))

@main.route('/confirm-payment/<int:form_id>', methods=['POST'])
@login_required
def confirm_payment(form_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))
        
    form = Form.query.get_or_404(form_id)
    form.payment_status = 'confirmed'
    form.status = 'accepted'
    db.session.commit()
    
    flash('Pembayaran telah dikonfirmasi', 'success')
    return redirect(url_for('main.dashboard'))
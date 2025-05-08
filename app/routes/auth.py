from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Form  # Add Form to imports
import os

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    name = StringField('Full Name', validators=[DataRequired()])
    submit = SubmitField('Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            name=form.name.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    if current_user.role == 'admin':
        flash('Admin accounts cannot be deleted', 'danger')
        return redirect(url_for('main.dashboard'))
    
    try:
        # Delete uploaded files if they exist
        user_form = Form.query.filter_by(user_id=current_user.id).first()
        if user_form:
            file_fields = ['akta_kelahiran', 'kartu_keluarga', 'ijazah_smp', 
                          'foto_siswa', 'ktp_ortu', 'nilai_rapor', 'sertifikat_prestasi']
            
            for field in file_fields:
                filename = getattr(user_form, field)
                if filename:
                    file_path = os.path.join('app/static/uploads', filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
            
            # Delete the form
            db.session.delete(user_form)
        
        # Delete the user
        db.session.delete(current_user)
        db.session.commit()
        
        # Logout the user
        logout_user()
        flash('Akun Anda berhasil dihapus', 'success')
        return redirect(url_for('main.index'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus akun: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))
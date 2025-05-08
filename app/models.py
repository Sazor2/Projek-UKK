from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default='user')
    forms = db.relationship('Form', backref='user', lazy=True)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    form_data = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Tambahan kolom untuk dokumen
    akta_kelahiran = db.Column(db.String(255))
    kartu_keluarga = db.Column(db.String(255))
    ijazah_smp = db.Column(db.String(255))
    foto_siswa = db.Column(db.String(255))
    ktp_ortu = db.Column(db.String(255))
    nisn_doc = db.Column(db.String(255))
    nilai_rapor = db.Column(db.String(255))
    sertifikat_prestasi = db.Column(db.String(255))

    @property
    def parsed_form_data(self):
        """Return parsed JSON data"""
        try:
            if isinstance(self.form_data, str):
                return json.loads(self.form_data)
            return self.form_data
        except:
            return {}
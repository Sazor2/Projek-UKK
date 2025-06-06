# PPDB Online SMA Yadika 🏫

> Sistem Penerimaan Peserta Didik Baru Online menggunakan Flask Framework

## 📋 Deskripsi
Sistem PPDB Online untuk memudahkan proses pendaftaran siswa baru secara digital. Mendukung verifikasi dokumen, pembayaran, dan manajemen data calon siswa.

## 🛠️ Instalasi

1. Clone repository
```bash
git clone https://github.com/username/ppdb-sma-yadika.git
cd ppdb-sma-yadika
```

2. Buat virtual environment
```bash
python -m venv venv
# Untuk Windows
venv\Scripts\activate
# Untuk Linux/Mac
source venv/bin/activate
```

3. Install dependencies dan setup
```bash
pip install -r requirements.txt
flask db upgrade
flask create-admin admin password123
python run.py
```

## ✨ Fitur Utama

### 👨‍🎓 Portal Siswa
- Pendaftaran akun dan login
- Form pendaftaran multi-step
- Upload dokumen persyaratan
- Tracking status pendaftaran
- Upload bukti pembayaran
- Cetak bukti penerimaan

### 👨‍💼 Portal Admin
- Dashboard statistik
- Verifikasi dokumen
- Konfirmasi pembayaran
- Filter & pencarian data
- Manajemen status siswa

## 📑 Dokumen Yang Dibutuhkan
- Pas Foto 3x4 (JPG/PNG)
- Kartu Keluarga (PDF/JPG/PNG)
- KTP Orang Tua (PDF/JPG/PNG)
- Akta Kelahiran (PDF/JPG/PNG)
- Ijazah/SKL SMP (PDF/JPG/PNG)
- Nilai Rapor (PDF/JPG/PNG)
- Sertifikat Prestasi (Opsional)

## 🔒 Batasan File
- Max size: 2MB/file
- Format foto: JPG, PNG
- Format dokumen: PDF, JPG, PNG

## 🔄 Alur Pendaftaran
1. Siswa registrasi akun
2. Upload dokumen persyaratan
3. Admin verifikasi dokumen
4. Siswa upload bukti pembayaran
5. Admin verifikasi pembayaran
6. Cetak bukti penerimaan

## 💻 Teknologi

### Backend
- Python Flask
- SQLAlchemy ORM
- Flask-Login
- WTForms

### Frontend
- Bootstrap 5
- JavaScript/jQuery
- DataTables
- Font Awesome 5

### Database
- SQLite

## 🛡️ Keamanan
- Password hashing
- CSRF protection
- File validation
- Role-based access
- Input sanitization

## 📱 Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 💾 Database Management

### Backup Database
```bash
sqlite3 instance/ppdb.db .dump > backup.sql
```

### Restore Database
```bash
sqlite3 instance/ppdb.db < backup.sql
```

## ⚠️ Troubleshooting

### Reset Password Admin
```bash
flask shell
>>> from app.models import User, db
>>> admin = User.query.filter_by(username='admin').first()
>>> admin.password = generate_password_hash('newpassword')
>>> db.session.commit()
```

### Clear Database
```bash
flask shell
>>> from app.models import db
>>> db.drop_all()
>>> db.create_all()
```

## 🤝 Kontribusi
1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📞 Kontak & Dukungan
- Email: ppdb@smayadika.sch.id
- Phone: 021-1234567

## 📜 Lisensi
[MIT License](LICENSE)

## 🔄 Changelog
Lihat [CHANGELOG.md](CHANGELOG.md) untuk detail perubahan.



##  Tampilan Landing page
![Screenshot 2025-05-22 124021](https://github.com/user-attachments/assets/f7f1f5e2-cb50-402a-a056-d4d7035dc0a7)


##  Tampilan Register
![Screenshot 2025-05-22 122946](https://github.com/user-attachments/assets/7329c809-e797-43b5-af23-1f0b51941045)


##  Tampilan Login
![Screenshot 2025-05-22 123057](https://github.com/user-attachments/assets/1375fa96-04ce-4b21-a080-eeccc7eca16c)


##  Tampilan isi dokumen pendaftaran
![Screenshot 2025-05-22 123826](https://github.com/user-attachments/assets/f4ea66f5-6814-4fb2-a94e-29188fd164fd)



##  Tampilan user dashboard untuk siswa
![Screenshot 2025-05-22 123737](https://github.com/user-attachments/assets/4251b31c-1e99-40d6-9273-3989c2b8f74d)



##  Tampilan admin dashboard
![Screenshot 2025-05-22 125724](https://github.com/user-attachments/assets/31be80ab-fbfd-47a8-b597-af11d6fea73c)



##  Tampilan detail siswa
![Screenshot 2025-05-22 125735](https://github.com/user-attachments/assets/d55b81f0-65f9-47c0-92c2-c4545fd5bbc7)



## 👨‍💻 Author

Made with ❤️ by **Nabil Akbar Kurnia Wijaya Putra**

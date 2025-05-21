# Sistem PPDB Online

Sistem Penerimaan Peserta Didik Baru (PPDB) Online adalah aplikasi web yang memudahkan proses pendaftaran siswa baru secara digital.

## Fitur Utama

### Untuk Calon Siswa
- Registrasi dan login akun
- Form pendaftaran online
- Upload dokumen persyaratan
- Tracking status pendaftaran
- Pembayaran dan upload bukti
- Cetak bukti pendaftaran

### Untuk Admin
- Dashboard admin
- Verifikasi pendaftaran
- Filter dan manajemen pendaftar
- Konfirmasi pembayaran
- Statistik pendaftaran

## Teknologi Yang Digunakan

### Backend
- Python Flask
- SQLAlchemy (Database ORM)
- Flask-Login (Autentikasi)
- Flask-Migrate (Database Migration)

### Frontend
- HTML5 & CSS3
- Bootstrap 5
- JavaScript & jQuery
- DataTables
- Font Awesome Icons
- AOS (Animate On Scroll)

### Database
- SQLite

## Persyaratan Sistem

```bash
# Python packages required
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Login==0.5.0
Flask-Migrate==3.1.0
Flask-WTF==0.15.1
Werkzeug==2.0.1
```

## Instalasi

1. Clone repository
```bash
git clone https://github.com/username/ppdb-online.git
cd ppdb-online
```

2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup database
```bash
flask db upgrade
```

5. Buat admin pertama
```bash
flask create-admin admin password123
```

6. Jalankan aplikasi
```bash
python run.py
```

## Struktur Folder

```
ppdb-online/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   ├── templates/
│   ├── routes/
│   ├── models.py
│   └── __init__.py
├── migrations/
├── config.py
├── run.py
└── requirements.txt
```

## Fitur Keamanan

- Password hashing
- Form validation
- File upload validation
- User authentication
- Role-based access control
- CSRF protection

## Status Pendaftaran

1. **Menunggu Verifikasi** - Dokumen sedang diverifikasi admin
2. **Diterima** - Pendaftaran diterima, menunggu pembayaran
3. **Ditolak** - Pendaftaran ditolak oleh admin

## Dokumen Yang Dibutuhkan

1. Pas Foto 3x4
2. Akta Kelahiran
3. Kartu Keluarga
4. Ijazah/SKL SMP
5. KTP Orang Tua
6. Nilai Rapor
7. Sertifikat Prestasi (opsional)

## Batasan File

- Maksimum ukuran: 2MB per file
- Format yang diizinkan: 
  - Foto: JPG, PNG
  - Dokumen: PDF, JPG, PNG

## Kontribusi

Silakan berkontribusi dengan membuat pull request. Untuk perubahan besar, harap buka issue terlebih dahulu.

## Lisensi

[MIT License](LICENSE)

## Kontak

Email: ppdb@sekolah.sch.id
Phone: +62 123 4567 890

## Screenshots

[Tambahkan screenshot aplikasi di sini]

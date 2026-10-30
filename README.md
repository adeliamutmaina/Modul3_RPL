# Aplikasi Perpustakaan
## 1. Deskripsi Aplikasi
Aplikasi Perpustakaan merupakan aplikasi berbasis Python yang digunakan untuk membantu pengelolaan data buku dan pengguna perpustakaan. Aplikasi ini menggunakan CustomTkinter sebagai antarmuka pengguna dan menerapkan pola arsitektur Model-View-Controller (MVC). Data aplikasi disimpan menggunakan database MySQL.

## 2. Struktur Direktori MVC
Struktur direktori proyek disusun menggunakan pola MVC sebagai berikut:
```text
Modul 3/
├── config/
│   └── database.py
├── controllers/
│   ├── auth_controller.py
│   └── buku_controller.py
├── models/
│   ├── user_model.py
│   └── buku_model.py
├── views/
│   ├── auth_view.py
│   └── buku_view.py
├── tests/
│   └── test_auth.py
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
Keterangan:
- config/: Mengatur konfigurasi koneksi database.
- models/: Mengelola data dan proses interaksi dengan database.
- views/: Menampilkan antarmuka aplikasi kepada pengguna.
- controllers/: Mengatur alur proses antara Model dan View.
- tests/: Menyimpan kode pengujian otomatis.
- main.py: File utama untuk menjalankan aplikasi.

## 3. Instalasi dan Konfigurasi Database MySQL
### Persiapan
1. Instal Python pada komputer.
2. Instal Laragon untuk menjalankan MySQL.
3. Aktifkan layanan MySQL melalui Laragon.
4. Siapkan database sesuai nama database yang digunakan dalam konfigurasi proyek.
### Instalasi Dependensi
Buka terminal pada folder proyek, kemudian jalankan:
```bash
python -m venv env
```
Aktifkan lingkungan virtual pada Windows:
```powershell
.\env\Scripts\Activate.ps1
```
Instal pustaka yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### Konfigurasi Database
Buka file config/database.py dan sesuaikan konfigurasi koneksi MySQL, meliputi:
- Host database.
- Username MySQL.
- Password MySQL.
- Nama database.
Pastikan database sudah tersedia dan layanan MySQL dalam keadaan aktif.

## 4. Cara Menjalankan Aplikasi
1. Jalankan MySQL melalui Laragon.
2. Buka terminal pada direktori utama proyek.
3. Aktifkan lingkungan virtual:
```powershell
.\env\Scripts\Activate.ps1
```
4. Jalankan aplikasi dengan perintah:
```bash
python main.py
```
Aplikasi akan menampilkan halaman login. Masukkan username dan password yang telah terdaftar untuk mengakses fitur perpustakaan.

## 5. Pengujian Aplikasi
Pengujian otomatis dilakukan menggunakan Pytest dengan perintah:
```bash
pytest -v
```
Pemeriksaan kualitas kode dilakukan menggunakan Flake8:
```bash
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 6. Pemaketan Aplikasi
Aplikasi dikemas menggunakan PyInstaller dengan perintah:
```bash
pyinstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```
Hasil pemaketan berupa file AplikasiPerpustakaan.exe yang tersimpan di dalam folder dist/.
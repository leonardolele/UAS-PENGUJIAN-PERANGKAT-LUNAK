[![CI Pipeline](https://github.com/leonardolele/UAS-PENGUJIAN-PERANGKAT-LUNAK/actions/workflows/ci.yml/badge.svg)](https://github.com/leonardolele/UAS-PENGUJIAN-PERANGKAT-LUNAK/actions/workflows/ci.yml)

Aplikasi URL Shortener sederhana yang dibangun menggunakan Python, FastAPI, dan SQLite. Proyek ini dikembangkan untuk mengimplementasikan praktik Automated Testing dan Continuous Integration (CI).

## Fitur Utama
1. Memendekkan URL (URL Shortening).
2. Redirect dari URL pendek ke URL asli.
3. Melacak statistik jumlah klik pada URL pendek.


Cara Menjalankan

1. Persiapan Environmen
Gunakan Virtual Environment untuk menjaga isolasi library:

Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

2. Install Dependencies
pip install -r requirements.txt

3. Menjalankan Aplikasi
python -m uvicorn src.main:app --reload
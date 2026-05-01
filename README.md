# Simple URL Shortener 🔗

![Build Status](https://github.com/USERNAME_GITHUB_KAMU/url_shortener_project/actions/workflows/ci.yml/badge.svg)

Aplikasi URL Shortener sederhana yang dibangun menggunakan Python, FastAPI, dan SQLite. Proyek ini dikembangkan untuk mengimplementasikan praktik *Automated Testing* dan *Continuous Integration* (CI).

## Fitur Utama
1. Memendekkan URL (*URL Shortening*).
2. *Redirect* dari URL pendek ke URL asli.
3. Melacak statistik jumlah klik pada URL pendek.

## Cara Menjalankan Aplikasi Lokal
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

   .\venv\Scripts\Activate.ps1
   python -m uvicorn src.main:app --reload
   http://localhost:8000
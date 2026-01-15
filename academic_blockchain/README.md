# Academic Blockchain – Deteksi Manipulasi Data Akademik

## Deskripsi Proyek
Proyek ini merupakan implementasi sederhana teknologi **Blockchain** untuk menjaga **integritas data akademik mahasiswa**.  
Sistem ini menggabungkan:
- Blockchain lokal (Python)
- Cloud storage (Google Sheets)
- API berbasis Flask

Tujuan utama proyek adalah **mendeteksi manipulasi data akademik** yang dilakukan di sisi cloud dengan membandingkan hash data cloud dan hash blockchain.

---

##  Struktur Blockchain
Blockchain terdiri dari beberapa blok yang merepresentasikan tahapan akademik:

| Block ID | Keterangan |
|--------|------------|
| 1 | Input nilai UTS |
| 2 | Input nilai UAS |
| 3 | Finalisasi mata kuliah |
| 4 | Penerbitan sertifikat |

Minimal 4 blok digunakan agar simulasi pemalsuan sertifikat dapat diuji.

---

## Teknologi yang Digunakan
- Python 3
- Flask
- Google Apps Script
- Google Sheets
- Postman
- SHA-256 Hashing

---



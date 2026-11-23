SMART KANTIN PLANNER - STREAMLIT

STRUKTUR FILE
-------------
smartplanner/
  app.py
  style.css
  requirements.txt
  menus.json        (dibuat otomatis saat aplikasi berjalan)

MENJALANKAN DI KOMPUTER
-----------------------
1. Install Python 3.10 atau lebih baru.
2. Buka terminal di folder proyek.
3. Jalankan:
   python -m pip install -r requirements.txt
4. Jalankan:
   streamlit run app.py
5. Browser akan membuka aplikasi Streamlit.

DEPLOY KE STREAMLIT COMMUNITY CLOUD
-----------------------------------
1. Upload app.py, style.css, dan requirements.txt ke repository GitHub.
2. Buka https://share.streamlit.io/
3. Login dengan GitHub dan pilih repository.
4. Pilih branch main dan file utama app.py.
5. Klik Deploy.

CATATAN PENYIMPANAN
-------------------
Aplikasi menyimpan perubahan ke menus.json di folder proyek.
Ini cocok untuk uji coba lokal. Pada Streamlit Community Cloud, filesystem
aplikasi tidak dijamin persisten saat aplikasi di-restart atau di-deploy ulang.
Untuk data produksi yang harus tetap aman, sambungkan database eksternal
(misalnya PostgreSQL/Supabase) pada tahap berikutnya.

Aplikasi ini tidak menggunakan Flask.

Sistem sederhana untuk manajemen event kampus dan pendaftaran peserta.

## Fitur
- CRUD Event (hanya admin dgn auth)
- Pendaftaran peserta ke event (dengan pengecekan kuota)
- Frontend HTML sederhana
- Dokumentasi otomatis via Swagger

## Admin Token
Gunakan header: `x-token: santo_admin` untuk akses admin.

## Instalasi
1. `pip install -r requirements.txt`
2. Jalankan: `uvicorn main:app --reload`
3. Buka:
   - API Docs: http://localhost:8000/docs (sebagai admin) (KLIK BUTTON "TRY IT OUT" UNTUK MENJALANKAN FUNC)
        -Cek Koneksi ke Index
            -Get / Read Root -> Execute
        -Tambah Event
            POST /events
                Isi header x-token
                Isi body JSON -> Execute
        -Cek Event
            GET /events -> Execute
        -Update Event
            PUT /events
                Isi ID Event
                Isi header x-token
                Isi body JSON -> Execute
        -Delete Event
            DELETE /events (CASCADE: jadi saat dihapus maka peserta yg terdaftar akan ikut terhapus)
                Isi ID Event
                Isi header x-token -> execute
        -Register Peserta Manual
            POST /register
                Isi body JSON -> Execute
        -Cek Peserta
            GET /participants → Execute


   - Frontend: http://localhost:8000/static/index.html
        -Dapat Melihat Event yang tersedia

        -Isi form → klik “Daftar Sekarang”
            Lihat pesan sukses/error
        
# Folder img berisi screenshoot uji coba

# Sistem Pemesanan Tiket Kereta Api Digital

Program berbasis terminal yang dibuat menggunakan Python untuk mengelola dan memesan tiket kereta api. Program memiliki dua role, yaitu **Admin** yang mengelola jadwal kereta dan **User** yang mencari jadwal, mengisi saldo, memesan tiket, serta mencetak invoice. Seluruh data disimpan dalam file **JSON**, sehingga tetap tersimpan setelah program ditutup.

# Flowchart Pemesanan Tiket Kereta Api Digital

## Menu Utama

<img width="2162" height="1732" alt="pa ddprr-1  Menu Utama, Login, Registrasi, Menu Admin" src="https://github.com/user-attachments/assets/3bd92a25-a3ee-4643-8c10-0ac409ba985c" />

Flowchart menu utama ini menggambarkan alur utama sistem pemesanan Tiket kereta api digital, mulai dari login, registrasi, hingga keluar. Pengguna dapat membuat akun baru atau masuk menggunakan akun yang sudah ada. Setelah login, sistem membedakan akses antara admin dan user sesuai perannya.

## CRUD Menu Admin

<img width="3782" height="1772" alt="pa ddprr-Menu Admin drawio (4)" src="https://github.com/user-attachments/assets/9f122f10-8fdd-4fcb-909c-be3ce4afe892" />


flowchart ini menggambarkan alur kerja Menu Utama Admin yang menyediakan 10 fitur utama: pengelolaan jadwal perjalanan CRUD (melihat, menambah, mengubah, dan menghapus jadwal), pengelolaan akun pengguna/user (melihat, menambah, mengubah, dan menghapus data akun), serta pemantauan riwayat semua transaksi dan pembuatan laporan ringkas, yang diakhiri dengan opsi keluar logout.

## Menu User

<img width="2372" height="1678" alt="pa ddprr-menu user drawio (1)" src="https://github.com/user-attachments/assets/9aaabcc5-d7d5-46c8-8445-a4144acde475" />


Flowchart  ini menggambarkan alur kerja Menu User yang menyediakan 6 pilihan utama: melihat jadwal perjalanan, pengisian saldo top up, pemesanan tiket, melihat riwayat transaksi pribadi, mengubah password akun, serta opsi keluar logout.



## Anggota & Peran

| No | Nama | NIM | Peran |
| --- | --- | --- | --- |
| 1 | Ignatius Imanuel Saroha Simalango | 2609116029 | Laporan & Pemrograman |
| 2 | Wisnu Aji| 2609116022 | Flowchart , Bug hunt, Laporan|
| 3 | Muhammad Royyan| 2609116005 | Buat laporan, Flowchart, Pemrograman|
| 4 | Aura Rizki Tariti | 2609116032 | Menjelaskan Program Di Flowchart, Flowchart

## Deskripsi & Tujuan

Pemesanan tiket kereta api secara manual membuat data jadwal, stok kursi, dan transaksi sulit dikelola. Program ini dibuat agar admin dapat mengelola jadwal secara digital, dan user dapat memesan tiket langsung dari terminal dengan sistem saldo (e-money). Tujuan project ini adalah menerapkan konsep dasar pemrograman Python, yaitu struktur data, percabangan, perulangan, fungsi, penyimpanan file, dan penanganan error.

## Fitur

- **Menu utama interaktif** yang terus ditampilkan hingga pengguna memilih keluar. Pilihan selain `1`, `2`, atau `3` akan menghasilkan pesan `Harus memilih 1-3....`

  ```python
  print("1. Login\n2. Registrasi\n3. Keluar")
  pilih = input("Pilih menu (1-3): ").strip()
  ```

- **Registrasi akun baru** dengan validasi. Username tidak boleh kosong, minimal 5 karakter, dan tidak boleh sama dengan username yang sudah ada (huruf besar dan kecil dianggap sama). Password tidak boleh kosong dan minimal 6 karakter. Password disembunyikan menggunakan `pwinput`

  ```python
  if username == "":
      raise ValueError("Username tidak boleh kosong....")
  if len(username) < 5:
      raise ValueError("Username minimal 5 karakter....")
  if username.lower() in [u["username"].lower() for u in users]:
      raise ValueError("Username sudah dipakai....")
  ```

- **Login dengan batas 3 kali percobaan.** Jika username atau password salah sebanyak 3 kali, program kembali ke menu utama. Role akun menentukan menu yang dibuka (admin atau user)

  ```python
  for ipanbenciben in range(1, 4):
      username = input("Username: ").strip()
      password = pwinput.pwinput("Password: ", mask="*")
      for u in users:
          if u["username"] == username and u["password"] == password:
              return u
  ```

- **Menampilkan jadwal kereta** dalam bentuk tabel menggunakan `PrettyTable`. Harga ditampilkan dengan format rupiah, misalnya `Rp450.000`

  ```python
  tabel = PrettyTable(["Tiket", "Kereta", "Dari", "Tujuan", "Jam", "Kelas", "Harga", "Stok"])
  for m in jadwal:
      tabel.add_row([m["Tiket"], m["nama"], m["Dari"], m["Tujuan"], m["Jam"], m["kelas"], rupiah(m["harga"]), m["stok"]])
  ```

- **CRUD jadwal untuk admin.** Admin dapat menambah, melihat, mengubah, dan menghapus jadwal. Kode tiket otomatis menjadi huruf besar dan tidak boleh duplikat. Jam harus berformat `HH:MM`, harga minimal 1, dan stok minimal 0. Pada menu ubah, input yang dikosongkan berarti data lama tidak diubah

  ```python
  tikets = detekinput("Kode tiket kereta: ").upper()
  if deteksiuser(jadwalss, "Tiket", tikets):
      raise ValueError("Kode sudah ada!")
  jam = cekjam(detekinput("Jam berangkat (HH:MM): "))
  ```

- **Menghapus jadwal dengan konfirmasi.** Sebelum data dihapus, program menanyakan `y/n`. Jawaban selain `y` atau `n` akan diulang

  ```python
  if konfirmasi(f"Yakin mau hapus {o['nama']}?"):
      jadwalss.remove(o)
      savedata(FileJadwall, jadwalss)
  ```

- **Mencari tiket** berdasarkan kode tiket, nama kereta, atau nama stasiun (asal atau tujuan). Pencarian tidak membedakan huruf besar dan kecil

  ```python
  kata = detekinput("Cari kode tiket / nama kereta / stasiun: ").lower()
  hasil = [m for m in jadwal if kata in m["Tiket"].lower() or kata in m["nama"].lower()
           or kata in m["Dari"].lower() or kata in m["Tujuan"].lower()]
  ```


- **Error handling dengan `try-except`** yang menangani `ValueError` dan `FileNotFoundError`, ditambah `KeyError` dan `TypeError` untuk data yang tidak lengkap, sehingga program tidak crash saat input salah atau file bermasalah

  ```python
  try:
      jumlah = detekangka("Jumlah tiket: ", 1)
  except ValueError as e:
      print(e)
  except FileNotFoundError:
      print("File data gak ketemu, transaksi gagal disimpan.....")
  ```

# Menjalankan Sistem Pemesanan Ticket kereta Api Digital

## Login Sebagai Admin

<img width="270" height="110" alt="Screenshot 2026-10-27 113859" src="https://github.com/user-attachments/assets/34a2d835-6528-4c8a-8bb1-cfd0f328e516" />
<br>
<img width="257" height="122" alt="Screenshot 2026-10-27 113913" src="https://github.com/user-attachments/assets/0f6c0b06-4f81-4445-a5d3-88e2d9e9db7c" />
<br>
<img width="295" height="160" alt="Screenshot 2026-10-31 210118" src="https://github.com/user-attachments/assets/370a4f8b-e55f-4f9e-a6ef-db6a9e904221" />

Tampilan ini menampilkan antarmuka berbasis terminal untuk alur Login Sebagai Admin pada Sistem Pemesanan Tiket Kereta Api. Alurnya dimulai dari menu awal (opsi 1: Login), proses verifikasi hak akses berupa autentikasi akun admin, hingga pengguna berhasil masuk dan diarahkan ke dasbor utama MENU ADMIN yang siap menerima input pilihan fitur.

## 1.Lihat Jadwal

<img width="205" height="152" alt="Screenshot 2026-10-31 210256" src="https://github.com/user-attachments/assets/0d2bc6f3-7263-42c9-b6b2-fbcbeda31f2e" />
<br>
<img width="625" height="170" alt="Screenshot 2026-10-27 114602" src="https://github.com/user-attachments/assets/4ae276cf-cc1e-4d55-8005-e7c40f20f62f" />

Tampilan ini menunjukkan antarmuka berbasis terminal untuk fitur 1. Lihat Jadwal pada Menu Admin. Setelah admin memilih opsi "1", sistem menampilkan daftar tabel jadwal keberangkatan kereta api secara terstruktur—mencakup kode tiket, nama kereta, stasiun asal, tujuan, jam keberangkatan, kelas, harga, hingga sisa stok tiket—dan meminta penekanan tombol Enter untuk melanjutkan kembali ke menu.

## 2.Tambah Jadwal

<img width="366" height="154" alt="Screenshot 2026-10-31 210437" src="https://github.com/user-attachments/assets/1c8af3ac-9a2d-4c7b-96bd-27dc2dbbf003" />
<br>
<img width="434" height="205" alt="Screenshot 2026-10-27 114920" src="https://github.com/user-attachments/assets/7ed367d6-25ec-41a1-b027-67ad4eb46b09" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 2. Tambah Jadwal pada Menu Admin. Setelah memilih opsi ke-2, admin memasukkan detail jadwal baru secara interaktif mulai dari kode tiket (berawalan T), nama kereta, stasiun asal dan tujuan, jam keberangkatan, pilihan kelas (Ekonomi/Bisnis/Eksekutif), harga tiket, hingga stok kursi. Sistem kemudian memproses penyimpanan dan menampilkan pesan "Jadwal berhasil ditambahkan" sebelum meminta pengguna menekan Enter untuk melanjutkan.

## 3. ubah Jadwal

<img width="291" height="151" alt="Screenshot 2026-10-31 210444" src="https://github.com/user-attachments/assets/9efcc726-febd-4e63-a77b-b5e683d6dfd0" />
<br>
<img width="619" height="396" alt="Screenshot 2026-10-27 115307" src="https://github.com/user-attachments/assets/6cbcd163-997b-4d10-8e47-56be13db95c6" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 3. Ubah Jadwal pada Menu Admin. Setelah memilih opsi ke-3, admin memasukkan kode tiket yang ingin diubah (contohnya t05), lalu dapat memperbarui informasi seperti nama kereta, stasiun asal, tujuan, jam keberangkatan, kelas, harga, dan stok kursi. Sistem kemudian memproses perubahan dan menampilkan pesan "Jadwal berhasil diubah" sebelum meminta pengguna menekan Enter untuk melanjutkan.

## 4. Hapus Jadwal

<img width="354" height="150" alt="Screenshot 2026-10-31 210456" src="https://github.com/user-attachments/assets/545958cd-5c39-4725-a961-a039142c56ff" />
<br>
<img width="580" height="247" alt="Screenshot 2026-10-27 115502" src="https://github.com/user-attachments/assets/ab1936fe-31fb-4f9a-82ed-ad3532cbc1ab" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 4. Hapus Jadwal pada Menu Admin. Setelah memilih opsi ke-4, admin memasukkan kode tiket yang ingin dihapus (contohnya t08), lalu sistem meminta konfirmasi penghapusan ("y/n"). Setelah dikonfirmasi dengan y, sistem menghapus jadwal tersebut, menampilkan pesan "Jadwal berhasil dihapus.....", dan meminta pengguna menekan Enter untuk melanjutkan.

## 5. Lihat User

<img width="422" height="158" alt="Screenshot 2026-10-31 210504" src="https://github.com/user-attachments/assets/73a09f9e-353f-4bb2-aebc-ba9ccd11f929" />
<br>
<img width="244" height="116" alt="Screenshot 2026-10-27 115744" src="https://github.com/user-attachments/assets/fb6bde66-4d5f-4ccd-b615-3fc29852801a" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 5. Lihat User pada Menu Admin. Setelah admin memilih opsi ke-5, sistem menampilkan daftar tabel berisi informasi seluruh pengguna yang terdaftar—meliputi nomor, username, peran (role), dan saldo masing-masing—serta meminta penekanan tombol Enter untuk melanjutkan.

## 6. Tambah User

<img width="419" height="152" alt="Screenshot 2026-10-31 210810" src="https://github.com/user-attachments/assets/8424ea5d-2b27-43eb-9c89-63bd1ae3761c" />
<br>
<img width="371" height="130" alt="Screenshot 2026-10-31 210830" src="https://github.com/user-attachments/assets/4a73ad8d-a925-44b0-8611-514672a83dc2" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 6. Tambah User pada Menu Admin. Setelah admin memilih opsi ke-6, sistem meminta input username (minimal 5 karakter), password (minimal 6 karakter), pemilihan role (1 untuk user atau 2 untuk admin), serta saldo awal. Sistem kemudian memproses dan menampilkan pesan "User berhasil ditambahkan....." sebelum meminta pengguna menekan tombol Enter untuk melanjutkan.

## 7. Ubah User

<img width="374" height="155" alt="Screenshot 2026-10-31 210938" src="https://github.com/user-attachments/assets/8b9a2ab5-4ba2-48d3-a2ae-169ab8b1dcad" />
<br>
<img width="409" height="185" alt="Screenshot 2026-10-31 211046" src="https://github.com/user-attachments/assets/5246cd66-5a2c-499d-8051-89a01c7cc6f4" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 7. Ubah User pada Menu Admin. Setelah admin memilih opsi ke-7, sistem menampilkan daftar tabel user, meminta input username yang ingin diubah, serta memungkinkan admin untuk memperbarui informasi seperti username baru, password baru, atau saldo. Sistem kemudian menampilkan pesan "saldo user berhasil diubah....." dan meminta penekanan tombol Enter untuk melanjutkan.

## 8. Hapus User

<img width="338" height="146" alt="Screenshot 2026-10-31 211349" src="https://github.com/user-attachments/assets/040acbe3-a31c-428e-a8a4-5a870e0d2979" />
<br>
<img width="316" height="150" alt="Screenshot 2026-10-31 211403" src="https://github.com/user-attachments/assets/210ad091-fd5d-483f-a8ef-c80f7389c3e0" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 8. Hapus User pada Menu Admin. Setelah memilih opsi ke-8, sistem menampilkan daftar tabel user, meminta input username yang ingin dihapus (contohnya wisnu), serta meminta konfirmasi penghapusan dengan memasukkan y/n. Setelah dikonfirmasi dengan y, sistem menghapus akun tersebut, menampilkan pesan "User berhasil dihapus.....", dan meminta pengguna menekan tombol Enter untuk melanjutkan.

## 9. Riwayat Semua Transaksi

<img width="353" height="151" alt="image" src="https://github.com/user-attachments/assets/a4fe71a5-36b4-4ee8-874c-da1b00e8536d" />
<br>
<img width="643" height="124" alt="image" src="https://github.com/user-attachments/assets/20b4386e-de84-4760-8037-1d8c2eec0cb9" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 9. Riwayat Semua Transaksi pada Menu Admin. Setelah admin memilih opsi ke-9, sistem menampilkan daftar tabel berisi rekapitulasi seluruh transaksi pengguna—meliputi kode transaksi, nama user, waktu, nama kereta, rute, jam, kelas, jumlah, dan total harga—serta meminta penekanan tombol Enter untuk melanjutkan.

## 10. Laporan Ringkas 

<img width="345" height="162" alt="Screenshot 2026-10-31 212221" src="https://github.com/user-attachments/assets/66b5b4c0-0d3f-42c1-89a1-c90383d8e04f" />
<br>
<img width="470" height="164" alt="image" src="https://github.com/user-attachments/assets/783ebf84-41f5-4bc7-a844-9ea1fb42757b" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 10. Laporan Ringkas pada Menu Admin. Setelah admin memilih opsi ke-10, sistem menampilkan rekapitulasi data yang mencakup total pendapatan, jumlah transaksi keseluruhan, informasi kereta terlaris, serta tabel rincian jumlah tiket terjual per kereta, lalu meminta penekanan tombol Enter untuk melanjutkan.

## 11. Logout

<img width="365" height="151" alt="Screenshot 2026-10-31 212908" src="https://github.com/user-attachments/assets/2e9f672d-25ec-46a5-b79a-b89bdfc5de83" />

Tampilan ini menunjukkan antarmuka terminal untuk opsi 11. Logout (atau pilihan angka 0 pada menu) pada Menu Admin. Setelah admin memilih opsi keluar tersebut, sistem akan memproses pengakhiran sesi aktif dan mengembalikan pengguna ke halaman utama login sistem.

## Login Sebagai User

<img width="198" height="95" alt="image" src="https://github.com/user-attachments/assets/ca52d8e7-8115-471c-b3f9-1bde3cc0a9d5" />
<br>
<img width="163" height="58" alt="Screenshot 2026-11-02 195757" src="https://github.com/user-attachments/assets/1bb74671-6c8d-4115-bb86-1e841eff1dbe" />
<br>
<img width="194" height="110" alt="image" src="https://github.com/user-attachments/assets/79464bb7-8c97-4cb3-bc8e-444b7d01eaaa" />

Tampilan ini menunjukkan antarmuka terminal untuk proses Login Sebagai User pada Sistem Pemesanan Tiket Kereta Api. Alur dimulai dari menu utama (pilihan 1: Login), dilanjutkan dengan memasukkan kredensial akun pengguna (Username dan Password), dan setelah berhasil masuk, sistem menampilkan dasbor MENU USER yang memuat informasi sisa saldo serta 6 pilihan menu layanan pengguna (Lihat Jadwal, Top up Saldo, Pesan Tiket, Riwayat Transaksi Saya, Ubah Password, hingga Logout).

## 1. Lihat Jadwal

<img width="165" height="113" alt="image" src="https://github.com/user-attachments/assets/e4d131bd-e662-4d14-bd02-252f95792dc7" />
<br>
<img width="520" height="191" alt="image" src="https://github.com/user-attachments/assets/d722ff0a-dd18-4628-8420-c8a7b2e419ed" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 1. Lihat Jadwal pada Menu User. Setelah pengguna memilih opsi nomor 1 dari menu utama, sistem menampilkan daftar tabel rincian jadwal kereta yang tersedia—termasuk informasi kode tiket, nama kereta, stasiun asal dan tujuan, jam, kelas, harga, hingga sisa stok—dan meminta pengguna menekan tombol Enter untuk melanjutkan.

## 2. Top up Saldo

<img width="173" height="119" alt="image" src="https://github.com/user-attachments/assets/52f4306b-0495-437e-9302-3843166d89ef" />
<br>
<img width="257" height="86" alt="image" src="https://github.com/user-attachments/assets/b8314a83-e418-4581-95ae-3eda66015ecf" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 2. Top Up Saldo pada Menu User. Setelah pengguna memilih opsi nomor 2, sistem menampilkan informasi saldo saat ini, meminta input nominal top up, lalu menampilkan pesan keberhasilan beserta pembaruan jumlah saldo terkini sebelum meminta pengguna menekan tombol Enter untuk melanjutkan.

## 3. Pesan Ticket

<img width="179" height="106" alt="Screenshot 2026-11-02 202203" src="https://github.com/user-attachments/assets/07218561-64a3-4289-952f-82ca7f805eeb" />
<br>
<img width="519" height="421" alt="Screenshot 2026-11-02 202308" src="https://github.com/user-attachments/assets/95d21f51-10a3-412e-8742-c2426a90f74b" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 3. Pesan Tiket pada Menu User. Setelah pengguna memilih opsi nomor 3, sistem menampilkan daftar jadwal kereta, meminta input kode tiket yang ingin dipesan, jumlah tiket, serta konfirmasi pembayaran menggunakan saldo akun (y/n). Setelah pembayaran berhasil, sistem menampilkan rincian Invoice Pembelian Tiket yang memuat kode transaksi, waktu, nama pemesan, rincian kereta, rute, jumlah, total bayar, dan ucapan terima kasih sebelum meminta pengguna menekan tombol Enter untuk melanjutkan.

## 4. Riwayat Transaksi Saya

<img width="158" height="120" alt="image" src="https://github.com/user-attachments/assets/0e851f12-fe0d-4aa8-8f00-3973eef2258c" />
<br>
<img width="590" height="147" alt="image" src="https://github.com/user-attachments/assets/406b8bba-94c9-46b8-8237-4cacd47c9133" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 4. Riwayat Transaksi Saya pada Menu User. Setelah pengguna memilih opsi nomor 4, sistem menampilkan tabel rekapitulasi daftar riwayat pembelian tiket yang pernah dilakukan oleh akun tersebut—meliputi kode transaksi, waktu, nama kereta, rute, jam, kelas, jumlah tiket, dan total biaya—serta meminta pengguna menekan tombol Enter untuk melanjutkan.

## 5. Ubah Password

<img width="163" height="112" alt="image" src="https://github.com/user-attachments/assets/06667613-fa3c-45bf-a877-c158628715aa" />
<br>
<img width="238" height="98" alt="image" src="https://github.com/user-attachments/assets/af9b0810-3efb-46e5-b66a-e6b1932064f4" />

Tampilan ini menunjukkan antarmuka terminal untuk fitur 5. Ubah Password pada Menu User. Setelah pengguna memilih opsi nomor 5, sistem meminta input password lama, password baru (minimal 6 karakter), serta konfirmasi ulangi password baru. Setelah validasi berhasil, sistem menampilkan pesan "Password berhasil diubah....." dan meminta pengguna menekan tombol Enter untuk melanjutkan.

## 6. Log Out

<img width="144" height="111" alt="image" src="https://github.com/user-attachments/assets/b18bea85-3aa9-4833-9add-abb6467c2497" />

Tampilan ini menunjukkan antarmuka terminal untuk opsi 0. Logout pada Menu User. Setelah pengguna memilih opsi 0, sistem memproses pengakhiran sesi aktif dari akun pengguna dan mengembalikan tampilan layar ke menu utama login sistem pemesanan tiket kereta api.















## Penerapan Materi

| Materi | Penerapan |
| --- | --- |
| List | Daftar jadwal, daftar user, dan daftar transaksi |
| Tuple | `KelasTiket` dan `topupsaldo` |
| Dictionary | Setiap data user, jadwal, dan transaksi, serta penghitung tiket terjual pada laporan |
| Percabangan (`if/elif/else`) | Menu, validasi input, dan pengecekan stok dan saldo |
| Perulangan (`for/while`) | Menu yang berulang, batas login 3 kali, dan menampilkan data |
| Fungsi | Seluruh logika dipisah ke fungsi berparameter dan ber-return |
| Library | `json`, `os`, `time`, `random`, `datetime`, `prettytable`, `pwinput` |

## Struktur Fungsi

| Fungsi | Tanggung jawab |
| --- | --- |
| `cleanterminal()` | Membersihkan layar terminal sesuai sistem operasi |
| `slow()` | Memberi jeda sebelum layar berpindah |
| `inputaman()` | `input()` yang aman dari `Ctrl+C` dan `Ctrl+D` |
| `passaman()` | Input password tersembunyi yang aman dari `Ctrl+C` dan `Ctrl+D` |
| `tekanenter()` | Menahan layar sampai user menekan Enter |
| `savedata()` | Menyimpan data ke file JSON |
| `loaddata()` | Membaca file JSON, membuat file baru bila belum ada atau rusak |
| `detekinput()` | Meminta input teks yang tidak boleh kosong |
| `detekangka()` | Meminta input angka bulat dengan batas minimal |
| `detekjam()` | Meminta input jam sampai formatnya benar |
| `detekkode()` | Meminta kode tiket yang diawali huruf `T` tanpa spasi |
| `konfirmasi()` | Meminta jawaban `y/n` |
| `rupiah()` | Mengubah angka ke format rupiah |
| `deteksiuser()` | Mencari satu data berdasarkan key dan nilai |
| `cekjam()` | Memvalidasi dan merapikan format jam `HH:MM` |
| `cekusername()` | Memvalidasi username (tidak kosong, minimal 5 karakter, belum dipakai) |
| `cekpassword()` | Memvalidasi password (tidak kosong, minimal 6 karakter) |
| `buatkode()` | Membuat kode transaksi unik (`TRXxxxxx`) |
| `tampilanJadwal()` | Menampilkan jadwal dalam bentuk tabel |
| `tampilanUser()` | Menampilkan daftar user dalam bentuk tabel |
| `tampilanRiwayat()` | Menampilkan daftar transaksi dalam bentuk tabel |
| `cetakinvoice()` | Mencetak invoice transaksi |
| `registrasi()` | Membuat akun user baru |
| `login()` | Memeriksa username dan password, maksimal 3 kali |
| `addjadwal()` | Menambah jadwal baru |
| `ubahjadwal()` | Mengubah data jadwal |
| `hapusjadwal()` | Menghapus jadwal setelah konfirmasi |
| `tambahuser()` | Menambah user baru oleh admin |
| `ubahuser()` | Mengubah data user oleh admin |
| `hapususer()` | Menghapus user setelah konfirmasi |
| `topsaldo()` | Menambah saldo user |
| `pesantiket()` | Memproses pemesanan tiket dan pembayaran dengan saldo |
| `riwayatsaya()` | Menampilkan riwayat transaksi milik user |
| `ubahpassword()` | Mengubah password user |
| `laporan()` | Menampilkan laporan ringkas untuk admin |
| `menuadmin()` | Mengatur perulangan menu admin |
| `menuuser()` | Mengatur perulangan menu user |
| `main()` | Memuat data, mengatur menu utama, dan menjalankan login atau registrasi |


## Ketentuan Data

- Username minimal 5 karakter dan tidak boleh sama dengan username lain. Password minimal 6 karakter.
- Kode tiket bersifat unik, otomatis diubah menjadi huruf besar, diawali huruf `T`, dan tanpa spasi.
- Jam berformat `HH:MM`, harga lebih dari 0, dan stok tidak boleh negatif.
- Top up maksimal `Rp100.000.000` per sekali top up.
- Saldo dan stok tidak boleh negatif. Pemesanan ditolak jika saldo atau stok tidak cukup.
- Pada `riwayat.json`, key `kode` berisi kode transaksi (`TRXxxxxx`), sedangkan key `Tiket` berisi kode tiket kereta yang dipesan.
- Jika file JSON dihapus atau rusak, file dibuat ulang dari data awal saat program dijalankan. Akun awal adalah `admin` dengan password `admin123`.
- Contoh isi `jadwal.json`:

  ```json
  {
      "Tiket": "T01",
      "nama": "Majapahit",
      "Dari": "Malang",
      "Tujuan": "Pasar Senen PP",
      "Jam": "09:45",
      "kelas": "Bisnis",
      "harga": 450000,
      "stok": 25
  }
  ```

- Contoh isi `users.json`:

  ```json
  {
      "username": "admin",
      "password": "admin123",
      "role": "admin",
      "saldo": 0
  }
  ```

- Contoh isi `transaksi.json`:

  ```json
  {
      "Tiket": "TKT-185324",
      "waktu": "2026-10-18 08:59:34",
      "username": "ipanbenci",
      "kereta": "Malabar",
      "kelas": "Ekonomi",
      "Dari": "Malang",
      "Tujuan": "Bandung PP",
      "Jam": "08:30",
      "jumlah": 2,
      "total": 400000
  }
  ```


### Built With
<img src="https://skillicons.dev/icons?i=py,vscode,github"/>


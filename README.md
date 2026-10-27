# Sistem Pemesanan Tiket Kereta Api Digital

Program berbasis terminal yang dibuat menggunakan Python untuk mengelola dan memesan tiket kereta api. Program memiliki dua role, yaitu **Admin** yang mengelola jadwal kereta dan **User** yang mencari jadwal, mengisi saldo, memesan tiket, serta mencetak invoice. Seluruh data disimpan dalam file **JSON**, sehingga tetap tersimpan setelah program ditutup.

# Flowchart Pemesanan Tiket Kereta Api Digital

## Menu Utama

<img width="2572" height="1612" alt="pa ddp-1  Menu Utama, Login, Registrasi, Menu Admin drawio" src="https://github.com/user-attachments/assets/7ee9d9aa-34c3-4f80-8777-095719ac3999" />


## CRUD Menu Admin

<img width="2272" height="1112" alt="DDP PA (1)-Menu Admin" src="https://github.com/user-attachments/assets/d4367b91-d2c0-47e6-80c3-0adad268ef8b" />

## Menu User

<img width="1682" height="1212" alt="pa ddp-menu user drawio" src="https://github.com/user-attachments/assets/c3c953d0-a460-4cba-a08c-feb547ef3308" />


## Anggota & Peran

| No | Nama | NIM | Peran |
| --- | --- | --- | --- |
| 1 | Ignatius Imanuel Saroha Simalango | 2609116029 | Flowchart & Pemrograman |
| 2 | Wisnu Aji| 2609116022 | Flowchart , Bug hunt|
| 3 | Muhammad Royyan| 2609116005 | Buat laporan, Flowchart, Pemrograman|
| 4 | Aura Rizki Tariti | 2609116032 |

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
<img width="249" height="152" alt="Screenshot 2026-10-27 113927" src="https://github.com/user-attachments/assets/a2423eb8-77e1-458a-b362-15a7202c8484" />

## 1.Lihat Jadwal

<img width="204" height="146" alt="Screenshot 2026-10-27 114553" src="https://github.com/user-attachments/assets/e9f4d332-d8e6-430d-b867-de9733ff3cec" />
<br>
<img width="625" height="170" alt="Screenshot 2026-10-27 114602" src="https://github.com/user-attachments/assets/4ae276cf-cc1e-4d55-8005-e7c40f20f62f" />

## 2.Tambah Jadwal

<img width="308" height="161" alt="Screenshot 2026-10-27 114929" src="https://github.com/user-attachments/assets/a83beafb-baac-4307-bf4f-9d160ce4eede" />
<br>
<img width="434" height="205" alt="Screenshot 2026-10-27 114920" src="https://github.com/user-attachments/assets/7ed367d6-25ec-41a1-b027-67ad4eb46b09" />

## 3. ubah Jadwal

<img width="189" height="149" alt="Screenshot 2026-10-27 115120" src="https://github.com/user-attachments/assets/e7be15b9-ef68-4615-a3bd-80010191c2ba" />
<br>
<img width="619" height="396" alt="Screenshot 2026-10-27 115307" src="https://github.com/user-attachments/assets/6cbcd163-997b-4d10-8e47-56be13db95c6" />

## 4. Hapus Jadwal

<img width="245" height="144" alt="Screenshot 2026-10-27 115516" src="https://github.com/user-attachments/assets/3657acb0-7317-45d4-9cc7-6752ab23ef6a" />
<br>
<img width="580" height="247" alt="Screenshot 2026-10-27 115502" src="https://github.com/user-attachments/assets/ab1936fe-31fb-4f9a-82ed-ad3532cbc1ab" />

## 5. Lihat User

<img width="234" height="144" alt="Screenshot 2026-10-27 115649" src="https://github.com/user-attachments/assets/10a22779-d781-4cc2-a6f0-51c86aa37080" />
<br>
<img width="244" height="116" alt="Screenshot 2026-10-27 115744" src="https://github.com/user-attachments/assets/fb6bde66-4d5f-4ccd-b615-3fc29852801a" />







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
| `savedata()` | Menyimpan data ke file JSON |
| `loaddata()` | Membaca file JSON, membuat file baru bila belum ada atau rusak |
| `detekinput()` | Meminta input teks yang tidak boleh kosong |
| `detekangka()` | Meminta input angka bulat dengan batas minimal dan maksimal |
| `konfirmasi()` | Meminta jawaban `y/n` |
| `rupiah()` | Mengubah angka ke format rupiah |
| `deteksiuser()` | Mencari satu data berdasarkan key dan nilai |
| `cekjam()` | Memvalidasi dan merapikan format jam `HH:MM` |
| `tampilanJadwal()` | Menampilkan jadwal dalam bentuk tabel |
| `transaksi()` | Menampilkan daftar transaksi dalam bentuk tabel |
| `invoice()` | Mencetak invoice transaksi |
| `registrasi()` | Membuat akun user baru |
| `login()` | Memeriksa username dan password, maksimal 3 kali |
| `addjadwal()` | Menambah jadwal baru |
| `ubahjadwal()` | Mengubah data jadwal |
| `hapusjadwal()` | Menghapus jadwal setelah konfirmasi |
| `laporan()` | Menampilkan laporan ringkas untuk admin |
| `caritiket()` | Mencari tiket berdasarkan kode, nama kereta, atau stasiun |
| `topup()` | Menambah saldo user |
| `kodetrx()` | Membuat kode transaksi unik |
| `pesantiket()` | Memproses pemesanan tiket dan pembayaran dengan saldo |
| `riwayat()` | Menampilkan riwayat transaksi milik user |
| `menuadmin()` | Mengatur perulangan menu admin |
| `menuuser()` | Mengatur perulangan menu user |
| `main()` | Memuat data, mengatur menu utama, dan menjalankan login atau registrasi |

## Ketentuan Data

- Username minimal 5 karakter dan tidak boleh sama dengan username lain. Password minimal 6 karakter.
- Kode tiket bersifat unik dan otomatis diubah menjadi huruf besar.
- Jam berformat `HH:MM`, harga lebih dari 0, dan stok tidak boleh negatif.
- Top up minimal `Rp10.000` dan maksimal `Rp10.000.000` untuk nominal lain.
- Saldo dan stok tidak boleh negatif. Pemesanan ditolak jika saldo atau stok tidak cukup.
- Pada `transaksi.json`, key `Tiket` berisi kode transaksi (`TKT-xxxxxx`), sedangkan pada `jadwal.json` key `Tiket` berisi kode tiket kereta.
- Jika file JSON dihapus, file dibuat ulang dari data awal saat program dijalankan.
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


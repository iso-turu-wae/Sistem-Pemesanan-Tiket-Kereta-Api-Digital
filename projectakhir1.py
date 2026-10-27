import json
import os
import time
import random
from datetime import datetime
from prettytable import PrettyTable
import pwinput

FileUser = "users.json"
FileJadwall = "jadwal.json"
FileRiwayat = "riwayat.json"


KelasTiket = ("Ekonomi", "Bisnis", "Eksekutif")
RoleUser = ("user", "admin")
Akundefault = [{"username": "admin", "password": "admin123", "role": "admin", "saldo": 0}]
JadwalTiket = [
    {"Tiket": "T01", "nama": "Majapahit", "Dari": "Malang", "Tujuan": "Pasar Senen PP", "Jam": "09:45", "kelas": "Bisnis", "harga": 450000, "stok": 25},
    {"Tiket": "T02", "nama": "Lodaya", "Dari": "Solo Balapan", "Tujuan": "Bandung PP", "Jam": "12:15", "kelas": "Eksekutif", "harga": 610000, "stok": 35},
    {"Tiket": "T03", "nama": "Malabar", "Dari": "Malang", "Tujuan": "Bandung PP", "Jam": "08:30", "kelas": "Ekonomi", "harga": 200000, "stok": 10},
    {"Tiket": "T04", "nama": "Taksaka", "Dari": "Yogyakarta", "Tujuan": "Gambir PP", "Jam": "15:00", "kelas": "Eksekutif", "harga": 710000, "stok": 50},
    {"Tiket": "T05", "nama": "Ambarawa Ekspres", "Dari": "Semarang Poncol", "Tujuan": "Surabaya Pasarturi PP", "Jam": "13:20", "kelas": "Bisnis", "harga": 350000, "stok": 25},
    {"Tiket": "T06", "nama": "Ciremai", "Dari": "Bandung", "Tujuan": "Semarang Tawang PP", "Jam": "07:00", "kelas": "Ekonomi", "harga": 150000, "stok": 32},
]

def cleanterminal():
    os.system("cls" if os.name == "nt" else "clear")

def slow(detik=2):
    try:
        time.sleep(detik)
    except ValueError:
        time.sleep(1)
    except KeyboardInterrupt:
        time.sleep(1)

def inputaman(wm):
    while True:
        try:
            return input(wm)
        except (KeyboardInterrupt, EOFError):
            print("\nDeteced ctrl....")
            slow(1)

def passaman(wm, mask="*"):
    while True:
        try:
            return pwinput.pwinput(wm, mask=mask)
        except (KeyboardInterrupt, EOFError):
            print("\nDeteced ctrl....")
            slow(1)

def tekanenter():
    try:
        input("\nTekan Enter untuk lanjut...")
    except (KeyboardInterrupt, EOFError):
        pass

def savedata(namafilee, data):
    try:
        with open(namafilee, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except FileNotFoundError:
        print("Erorr, folder/file tujuan gak ketemu.....")
        return False
    except (OSError, ValueError, TypeError):
        print("Erorr, data gak kesimpan ke file.....")
        return False

def loaddata(namafilee, data):
    try:
        with open(namafilee, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {namafilee} belum ada, membuat data awal.....")
        savedata(namafilee, data)
        return data
    except ValueError:
        print(f"File {namafilee} rusak, direset ke data awal.....")
        savedata(namafilee, data)
        return data

def detekinput(wm):
    while True:
        teks = inputaman(wm).strip()
        try:
            if teks:
                return teks
            raise ValueError("Input gak boleh kosong :) ")
        except ValueError as e:
            print(e)


def detekangka(wm, minimal=0):
    while True:
        try:
            angka = int(inputaman(wm))
            if angka >= minimal:
                return angka
            print(f"Ketik angka minimal {minimal}")
        except ValueError:
            print("Input nya angka men....")

def konfirmasi(ipanbencib):
    while True:
        jawab = inputaman(f"{ipanbencib} (y/n): ").lower()
        try:
            if jawab in ("y", "n"):
                return jawab == "y"
            raise ValueError("Ketik y atau n saja...")
        except ValueError as p:
            print(p)

def rupiah(angka):
    try:
        return "Rp{:,}".format(angka).replace(",", ".")
    except ValueError:
        return "Rp0"

def deteksiuser(daftar, key, nilai):
    try:
        for item in daftar:
            if item[key] == nilai:
                return item
    except ValueError:
        print("Data gak sesuai format.....")
    except (KeyError, TypeError):
        print("Data ada yang rusak/gak lengkap.....")
    except FileNotFoundError:
        print("File data gak ketemu.....")
    return None

def cekjam(teks):
    try:
        return datetime.strptime(teks, "%H:%M").strftime("%H:%M")
    except ValueError:
        raise ValueError("Format jam salah, contoh 09:45....")

def detekjam(wm):
    while True:
        try:
            return cekjam(detekinput(wm))
        except ValueError as e:
            print(e)

def detekkode(wm):
    while True:
        kode = detekinput(wm).upper()
        if kode.startswith("T") and len(kode) > 1 and " " not in kode:
            return kode
        print("Kode tiket harus diawali huruf T dan tanpa spasi, contoh T07....")

def cekusername(users, username):
    if username == "":
        raise ValueError("Username tidak boleh kosong....")
    if len(username) < 5:
        raise ValueError("Username minimal 5 karakter....")
    if deteksiuser(users, "username", username):
        raise ValueError("Username sudah dipakai....")
    return username

def cekpassword(password):
    if password == "":
        raise ValueError("Password tidak boleh kosong....")
    if len(password) < 6:
        raise ValueError("Password minimal 6 karakter....")
    return password

def buatkode(riwayat):
    kode = f"TRX{random.randint(10000, 99999)}"
    while deteksiuser(riwayat, "kode", kode):
        kode = f"TRX{random.randint(10000, 99999)}"
    return kode

# ================== TAMPILAN ==================

def tampilanJadwal(jadwal):
    try:
        if not jadwal:
            print("Jadwal belum ada....")
            return
        tabel = PrettyTable(["Tiket", "Kereta", "Dari", "Tujuan", "Jam", "Kelas", "Harga", "Stok"])
        for m in jadwal:
            tabel.add_row([m["Tiket"], m["nama"], m["Dari"], m["Tujuan"], m["Jam"], m["kelas"], rupiah(m["harga"]), m["stok"]])
        print(tabel)
    except ValueError:
        print("Data jadwal gak sesuai format.....")
    except (KeyError, TypeError):
        print("Data jadwal ada yang rusak/gak lengkap.....")
    except FileNotFoundError:
        print("File jadwal gak ketemu.....")

def tampilanUser(users):
    try:
        if not users:
            print("User belum ada....")
            return
        tabel = PrettyTable(["No", "Username", "Role", "Saldo"])
        for i, u in enumerate(users, 1):
            tabel.add_row([i, u["username"], u["role"], rupiah(u["saldo"])])
        print(tabel)
    except ValueError:
        print("Data user gak sesuai format.....")
    except (KeyError, TypeError):
        print("Data user ada yang rusak/gak lengkap.....")

def tampilanRiwayat(riwayat, semua=False):
    try:
        if not riwayat:
            print("Belum ada transaksi....")
            return
        kolom = ["Kode", "Waktu", "Kereta", "Rute", "Jam", "Kelas", "Jml", "Total"]
        if semua:
            kolom.insert(1, "User")
        tabel = PrettyTable(kolom)
        for t in riwayat:
            baris = [t["kode"], t["waktu"], t["kereta"], f"{t['dari']} - {t['tujuan']}", t["jam"], t["kelas"], t["jumlah"], rupiah(t["total"])]
            if semua:
                baris.insert(1, t["username"])
            tabel.add_row(baris)
        print(tabel)
    except ValueError:
        print("Data riwayat gak sesuai format.....")
    except (KeyError, TypeError):
        print("Data riwayat ada yang rusak/gak lengkap.....")

def cetakinvoice(trx):
    try:
        print("=" * 42)
        print("          INVOICE PEMBELIAN TIKET")
        print("=" * 42)
        print(f"Kode Transaksi : {trx['kode']}")
        print(f"Waktu          : {trx['waktu']}")
        print(f"Nama Pemesan   : {trx['username']}")
        print("-" * 42)
        print(f"Kereta         : {trx['kereta']} ({trx['kelas']})")
        print(f"Rute           : {trx['dari']} - {trx['tujuan']}")
        print(f"Jam Berangkat  : {trx['jam']}")
        print(f"Harga Satuan   : {rupiah(trx['harga'])}")
        print(f"Jumlah Tiket   : {trx['jumlah']}")
        print("-" * 42)
        print(f"TOTAL BAYAR    : {rupiah(trx['total'])}")
        print("=" * 42)
        print("   Terima kasih, selamat menikmati perjalanan!")
    except (KeyError, TypeError):
        print("Data invoice ada yang rusak/gak lengkap.....")

# ================== AUTH ==================

def registrasi(users):
    print("=== REGISTRASI ===")
    try:
        username = cekusername(users, inputaman("Masukkan username (min 5 karakter): "))
        password = cekpassword(passaman("Password (min. 6 karakter): "))
        users.append({"username": username, "password": password, "role": "user", "saldo": 0})
        savedata(FileUser, users)
        print("Registrasi berhasil! Silakan login....")
    except ValueError as ipan:
        print(ipan)
    except FileNotFoundError:
        print("File user tidak ditemukan, registrasi gagal....")
    return users

def login(users):
    print("===== LOGIN =====")
    try:
        for ipanbenciben in range(1, 4):
            username = inputaman("Username: ")
            password = passaman("Password: ")
            for u in users:
                if u["username"] == username and u["password"] == password:
                    print(f"Selamat datang, {username} 😊")
                    return u
            print(f"Username/password salah! percobaan {ipanbenciben}/3")
        print("Login gagal 3 kali kembali ke menu utama.....")
    except ValueError:
        print("Input gak valid, login gagal.....")
    except (KeyError, TypeError):
        print("Data user rusak/gak lengkap, login gagal.....")
    except FileNotFoundError:
        print("File user gak ketemu, login gagal.....")
    return None

# ================== CRUD JADWAL (ADMIN) ==================

def addjadwal(jadwalss):
    print("=== TAMBAH JADWAL ===")
    try:
        tikets = detekkode("Kode tiket kereta (awali dengan T, contoh T07): ")
        if deteksiuser(jadwalss, "Tiket", tikets):
            raise ValueError("Kode sudah ada!")
        nama = detekinput("Nama kereta: ")
        Dari = detekinput("Stasiun Dari: ")
        tujuan = detekinput("Stasiun tujuan: ")
        jam = detekjam("Jam berangkat (HH:MM): ")
        for i, k in enumerate(KelasTiket, 1):
            print(f"{i}. {k}")
        pilih = detekangka("Pilih kelas: ", 1)
        if pilih > len(KelasTiket):
            raise ValueError("Pilihan kelas tidak valid....")
        harga = detekangka("Harga tiket: ", 1)
        stok = detekangka("Stok kursi: ", 0)
        jadwalss.append({"Tiket": tikets, "nama": nama, "Dari": Dari, "Tujuan": tujuan,
                         "Jam": jam, "kelas": KelasTiket[pilih - 1], "harga": harga, "stok": stok})
        savedata(FileJadwall, jadwalss)
        print("Jadwal berhasil ditambahkan.")
    except ValueError as e:
        print(f"Gagal tambah jadwal: {e}")
    except FileNotFoundError:
        print("File jadwal gak ketemu, jadwal gagal ditambahkan.....")
    return jadwalss

def ubahjadwal(ipansukablame):
    print("==== UBAH JADWAL ====")
    try:
        tampilanJadwal(ipansukablame)
        o = deteksiuser(ipansukablame, "Tiket", detekinput("Kode tiket yang mau di reschedule: ").upper())
        if not o:
            raise ValueError("Tiket tidak ditemukan😞")
        print("Kosongkan input jika tidak ingin mengubah.....")
        for field, label in (("nama", "Nama"), ("Dari", "Dari"), ("Tujuan", "Tujuan"), ("Jam", "Jam")):
            baru = inputaman(f"{label} [{o[field]}]: ")
            if baru:
                if field == "Jam":
                    while baru:
                        try:
                            baru = cekjam(baru)
                            break
                        except ValueError as err:
                            print(err)
                            baru = inputaman("Jam [kosongkan jika batal]: ")
                    if not baru:
                        continue
                o[field] = baru
        for i, k in enumerate(KelasTiket, 1):
            print(f"{i}. {k}")
        pilihkelas = inputaman(f"Kelas [{o['kelas']}] (pilih nomor): ")
        if pilihkelas:
            try:
                nomor = int(pilihkelas)
                if nomor < 1 or nomor > len(KelasTiket):
                    raise ValueError
                o["kelas"] = KelasTiket[nomor - 1]
            except ValueError:
                print("Kelas tidak valid, tidak diubah.....")
        for field, label in (("harga", "Harga"), ("stok", "Stok")):
            baru = inputaman(f"{label} [{o[field]}]: ")
            if baru:
                try:
                    nilai = int(baru)
                    if nilai < 0 or (field == "harga" and nilai == 0):
                        raise ValueError
                    o[field] = nilai
                except ValueError:
                    print(f"{label} tidak valid, tidak diubah.....")
        savedata(FileJadwall, ipansukablame)
        print("Jadwal berhasil diubah.....")
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("File jadwal gak ketemu, perubahan gagal disimpan.....")
    return ipansukablame

def hapusjadwal(jadwalss):
    print("=== HAPUS JADWAL ===")
    try:
        tampilanJadwal(jadwalss)
        o = deteksiuser(jadwalss, "Tiket", detekinput("Kode tiket yang mau dihapus: ").upper())
        if not o:
            raise ValueError("Tiket tidak ditemukan😞")
        if konfirmasi(f"Yakin mau hapus {o['nama']}?"):
            jadwalss.remove(o)
            savedata(FileJadwall, jadwalss)
            print("Jadwal berhasil dihapus.....")
        else:
            print("Dibatalkan....")
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("File jadwal gak ketemu, penghapusan gagal disimpan.....")
    return jadwalss

# ================== CRUD USER (ADMIN) ==================

def tambahuser(users):
    print("=== TAMBAH USER ===")
    try:
        username = cekusername(users, inputaman("Username (min 5 karakter): "))
        password = cekpassword(passaman("Password (min. 6 karakter): "))
        for i, r in enumerate(RoleUser, 1):
            print(f"{i}. {r}")
        pilih = detekangka("Pilih role: ", 1)
        if pilih > len(RoleUser):
            raise ValueError("Pilihan role tidak valid....")
        saldo = detekangka("Saldo awal: ", 0)
        users.append({"username": username, "password": password, "role": RoleUser[pilih - 1], "saldo": saldo})
        savedata(FileUser, users)
        print("User berhasil ditambahkan.....")
    except ValueError as e:
        print(f"Gagal tambah user: {e}")
    except FileNotFoundError:
        print("File user gak ketemu, user gagal ditambahkan.....")
    return users

def ubahuser(users, riwayat):
    print("=== UBAH USER ===")
    try:
        tampilanUser(users)
        o = deteksiuser(users, "username", detekinput("Username yang mau diubah: "))
        if not o:
            raise ValueError("User tidak ditemukan😞")
        print("Kosongkan input jika tidak ingin mengubah.....")
        lama = o["username"]
        usernamebaru = inputaman(f"Username [{lama}]: ")
        if usernamebaru and usernamebaru != lama:
            cekusername(users, usernamebaru)
        else:
            usernamebaru = ""
        passwordbaru = passaman("Password baru [kosongkan jika tidak diubah]: ")
        if passwordbaru:
            cekpassword(passwordbaru)
        saldobaru = inputaman(f"Saldo [{rupiah(o['saldo'])}]: ")
        if usernamebaru:
            o["username"] = usernamebaru
            for t in riwayat:
                if t["username"] == lama:
                    t["username"] = usernamebaru
            savedata(FileRiwayat, riwayat)
        if passwordbaru:
            o["password"] = passwordbaru
        if saldobaru:
            try:
                nilai = int(saldobaru)
                if nilai < 0:
                    raise ValueError
                o["saldo"] = nilai
            except ValueError:
                print("Saldo tidak valid, tidak diubah.....")
        savedata(FileUser, users)
        print("User berhasil diubah.....")
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("File user gak ketemu, perubahan gagal disimpan.....")
    return users

def hapususer(users, admin):
    print("=== HAPUS USER ===")
    try:
        tampilanUser(users)
        o = deteksiuser(users, "username", detekinput("Username yang mau dihapus: "))
        if not o:
            raise ValueError("User tidak ditemukan😞")
        if o["username"] == admin["username"]:
            raise ValueError("Gak bisa hapus akun yang lagi dipakai login....")
        if konfirmasi(f"Yakin mau hapus user {o['username']}?"):
            users.remove(o)
            savedata(FileUser, users)
            print("User berhasil dihapus.....")
        else:
            print("Dibatalkan....")
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("File user gak ketemu, penghapusan gagal disimpan.....")
    return users

# ================== FITUR USER ==================

def topsaldo(user, users):
    print("=== TOP UP SALDO ===")
    try:
        print(f"Saldo sekarang: {rupiah(user['saldo'])}")
        uang = detekangka("Masukan nominal top up: ", 1)

        if uang > 100000000:
            raise ValueError("Nominal top up maksimal Rp100.000.000!")

        user["saldo"] += uang
        savedata(FileUser, users)
        print(f"Top up berhasil! Saldo sekarang: {rupiah(user['saldo'])}")
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("File user tidak ditemukan, top-up gagal disimpan.....")
    
    return user

def pesantiket(user, jadwal, users, riwayat):
    print("=== PESAN TIKET ===")
    try:
        if not jadwal:
            print("Jadwal belum ada....")
            return None
        tampilanJadwal(jadwal)
        print(f"Saldo kamu: {rupiah(user['saldo'])}")
        o = deteksiuser(jadwal, "Tiket", detekkode("Kode tiket yang mau dipesan: "))
        if not o:
            raise ValueError("Tiket tidak ditemukan😞")
        if o["stok"] <= 0:
            raise ValueError("Stok tiket habis....")
        jumlah = detekangka(f"Jumlah tiket (maks {o['stok']}): ", 1)
        if jumlah > o["stok"]:
            raise ValueError("Stok gak cukup....")
        total = o["harga"] * jumlah
        if user["saldo"] < total:
            raise ValueError(f"Saldo gak cukup! Total {rupiah(total)}, saldo kamu {rupiah(user['saldo'])}")
        print(f"Total bayar: {rupiah(total)}")
        if not konfirmasi("Lanjut bayar pakai saldo?"):
            print("Dibatalkan....")
            return None
        user["saldo"] -= total
        o["stok"] -= jumlah
        trx = {
            "kode": buatkode(riwayat),
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": user["username"],
            "Tiket": o["Tiket"],
            "kereta": o["nama"],
            "dari": o["Dari"],
            "tujuan": o["Tujuan"],
            "jam": o["Jam"],
            "kelas": o["kelas"],
            "harga": o["harga"],
            "jumlah": jumlah,
            "total": total,
        }
        riwayat.append(trx)
        savedata(FileUser, users)
        savedata(FileJadwall, jadwal)
        savedata(FileRiwayat, riwayat)
        print("Pembayaran berhasil!\n")
        cetakinvoice(trx)
        return trx
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("File data gak ketemu, transaksi gagal disimpan.....")
    return None

def riwayatsaya(user, riwayat):
    print("=== RIWAYAT TRANSAKSI SAYA ===")
    try:
        punyaku = [t for t in riwayat if t["username"] == user["username"]]
        tampilanRiwayat(punyaku)
        return punyaku
    except (KeyError, TypeError):
        print("Data riwayat ada yang rusak/gak lengkap.....")
    return []

def ubahpassword(user, users):
    print("=== UBAH PASSWORD ===")
    try:
        lama = passaman("Password lama: ")
        if lama != user["password"]:
            raise ValueError("Password lama salah....")
        baru = cekpassword(passaman("Password baru (min. 6 karakter): "))
        ulang = passaman("Ulangi password baru: ")
        if baru != ulang:
            raise ValueError("Password baru gak sama....")
        user["password"] = baru
        savedata(FileUser, users)
        print("Password berhasil diubah.....")
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("File user gak ketemu, perubahan gagal disimpan.....")
    return user

# ================== LAPORAN (ADMIN) ==================

def laporan(riwayat):
    print("=== LAPORAN RINGKAS ===")
    try:
        if not riwayat:
            print("Belum ada transaksi....")
            return None
        totalpendapatan = sum(t["total"] for t in riwayat)
        terjual = {}
        for t in riwayat:
            terjual[t["kereta"]] = terjual.get(t["kereta"], 0) + t["jumlah"]
        terlaris = max(terjual, key=terjual.get)
        print(f"Total pendapatan : {rupiah(totalpendapatan)}")
        print(f"Jumlah transaksi : {len(riwayat)}")
        print(f"Kereta terlaris  : {terlaris} ({terjual[terlaris]} tiket)\n")
        tabel = PrettyTable(["Kereta", "Tiket Terjual"])
        for nama, jml in sorted(terjual.items(), key=lambda x: x[1], reverse=True):
            tabel.add_row([nama, jml])
        print(tabel)
        return {"pendapatan": totalpendapatan, "transaksi": len(riwayat), "terlaris": terlaris}
    except (KeyError, TypeError, ValueError):
        print("Data riwayat ada yang rusak/gak lengkap.....")
    return None

# ================== MENU ==================

def menuadmin(user, jadwal, users, riwayat):
    while True:
        try:
            cleanterminal()
            print("=== MENU ADMIN ===")
            print("1. Lihat Jadwal\n2. Tambah Jadwal\n3. Ubah Jadwal\n4. Hapus Jadwal")
            print("5. Lihat User\n6. Tambah User\n7. Ubah User\n8. Hapus User")
            print("9. Riwayat Semua Transaksi\n10. Laporan Ringkas\n0. Logout")
            pilih = inputaman("Pilih: ")
            cleanterminal()
            if pilih == "1":
                tampilanJadwal(jadwal)
            elif pilih == "2":
                addjadwal(jadwal)
            elif pilih == "3":
                ubahjadwal(jadwal)
            elif pilih == "4":
                hapusjadwal(jadwal)
            elif pilih == "5":
                tampilanUser(users)
            elif pilih == "6":
                tambahuser(users)
            elif pilih == "7":
                ubahuser(users, riwayat)
            elif pilih == "8":
                hapususer(users, user)
            elif pilih == "9":
                tampilanRiwayat(riwayat, True)
            elif pilih == "10":
                laporan(riwayat)
            elif pilih == "0":
                return
            else:
                raise ValueError("Pilihan gak valid....")
        except ValueError as e:
            print(e)
        except (KeyError, TypeError):
            print("Data ada yang rusak/gak lengkap.....")
        except FileNotFoundError:
            print("File data gak ketemu.....")
        except (KeyboardInterrupt, EOFError):
            print("\nDDeteced ctrl...")
            slow(1)
            continue
        tekanenter()

def menuuser(user, jadwal, users, riwayat):
    while True:
        try:
            cleanterminal()
            print("=== MENU USER ===")
            print(f"Saldo: {rupiah(user['saldo'])}")
            print("1. Lihat Jadwal\n2. Top Up Saldo\n3. Pesan Tiket\n4. Riwayat Transaksi Saya\n5. Ubah Password\n0. Logout")
            pilih = inputaman("Pilih: ")
            cleanterminal()
            if pilih == "1":
                tampilanJadwal(jadwal)
            elif pilih == "2":
                topsaldo(user, users)
            elif pilih == "3":
                pesantiket(user, jadwal, users, riwayat)
            elif pilih == "4":
                riwayatsaya(user, riwayat)
            elif pilih == "5":
                ubahpassword(user, users)
            elif pilih == "0":
                return
            else:
                raise ValueError("Pilihan gak valid....")
        except ValueError as e:
            print(e)
        except (KeyError, TypeError):
            print("Data ada yang rusak/gak lengkap.....")
        except FileNotFoundError:
            print("File data gak ketemu.....")
        except (KeyboardInterrupt, EOFError):
            print("\nDeteced ctrl....")
            slow(1)
            continue
        tekanenter()

def main():
    users = loaddata(FileUser, Akundefault)
    jadwal = loaddata(FileJadwall, JadwalTiket)
    riwayat = loaddata(FileRiwayat, [])
    while True:
        try:
            cleanterminal()
            print("=====================================")
            print("   SISTEM PEMESANAN TIKET KERETA API")
            print("=====================================")
            print("1. Login\n2. Registrasi\n3. Keluar")
            pilih = inputaman("Pilih menu (1-3): ")
            cleanterminal()
            if pilih == "1":
                user = login(users)
                if user:
                    slow()
                    if user["role"] == "admin":
                        menuadmin(user, jadwal, users, riwayat)
                    else:
                        menuuser(user, jadwal, users, riwayat)
                else:
                    slow()
            elif pilih == "2":
                registrasi(users)
                slow()
            elif pilih == "3":
                print("Terima kasih, sampai jumpa.....")
                break
            else:
                raise ValueError("Harus memilih 1/2/3....")
        except ValueError as e:
            print(e)
            slow()
        except FileNotFoundError:
            print("File data gak ketemu.....")
            slow()
        except (KeyboardInterrupt, EOFError):
            print("\nDeteced ctrl....")
            slow(1)

try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\nProgram dihentikan.....")

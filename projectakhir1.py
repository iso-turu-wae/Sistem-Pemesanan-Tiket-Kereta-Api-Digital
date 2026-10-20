import json
import os
import time
from datetime import datetime
from prettytable import PrettyTable
import pwinput
topupsaldo = ""
FileUser = "users.json"
FileJadwall = "jadwal.json"


KelasTiket = ("Ekonomi", "Bisnis", "Eksekutif")
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
        teks = input(wm).strip()
        try:
            if teks:
                return teks
            raise ValueError("Input gak boleh kosong :) ")
        except ValueError as e:
            print(e)


def detekangka(wm, minimal=0):
    while True:
        try:
            angka = int(input(wm))
            if angka >= minimal:
                return angka
            print(f"Ketik angka minimal {minimal}")
        except ValueError:
            print("Input nya angka men....")

def konfirmasi(ipanbencib):
    while True:
        jawab = input(f"{ipanbencib} (y/n): ").lower()
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

def registrasi(users):
    print("=== REGISTRASI ===")
    try:
        username = input("Masukkan username (min 5 karakter): ")
        if username == "":
            raise ValueError("Username tidak boleh kosong....")
        if len(username) < 5:
            raise ValueError("Username minimal 5 karakter....")
        if deteksiuser(users, "username", username):
            raise ValueError("Username sudah dipakai....")
        password = pwinput.pwinput("Password (min. 6 karakter): ", mask="*")
        if password == "":
            raise ValueError("Password tidak boleh kosong....")
        if len(password) < 6:
            raise ValueError("Password minimal 6 karakter....")
        users.append({"username": username, "password": password, "role": "user", "saldo": 0})
        savedata(FileUser, users)
        print("Registrasi berhasil! Silakan login....")
    except ValueError as ipan:
        print(ipan)
    except FileNotFoundError:
        print("File user tidak ditemukan, registrasi gagal....")
    except (KeyboardInterrupt, EOFError):
        print("\nJangan pencet Ctrl, kembali ke menu utama...")
    return users

def login(users):
    print("===== LOGIN =====")
    try:
        for ipanbenciben in range(1, 4):
            username = input("Username: ")
            password = pwinput.pwinput("Password: ")
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
    except (KeyboardInterrupt, EOFError):
        print("\nJangan pencet Ctrl, kembali ke menu utama...")
    return None

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
    except (KeyboardInterrupt, EOFError):
        print("\nJangan pencet Ctrl, kembali ke menu utama...")
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
            baru = input(f"{label} [{o[field]}]: ")
            if baru:
                if field == "Jam":
                    while baru:
                        try:
                            baru = cekjam(baru)
                            break
                        except ValueError as err:
                            print(err)
                            baru = input("Jam [kosongkan jika batal]: ")
                    if not baru:
                        continue
                o[field] = baru
        for field, label in (("harga", "Harga"), ("stok", "Stok")):
            baru = input(f"{label} [{o[field]}]: ")
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
    except (KeyboardInterrupt, EOFError):
        print("\nJangan pencet Ctrl, kembali ke menu utama...")
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
    except (KeyboardInterrupt, EOFError):
        print("\nJangan pencet Ctrl, kembali ke menu utama...")
    return jadwalss

def menuadmin(user, jadwal):
    while True:
        try:
            cleanterminal()
            print("=== MENU ADMIN ===")
            print("1. Lihat Jadwal\n2. Tambah Jadwal\n3. Ubah Jadwal\n4. Hapus Jadwal\n0. Logout")
            pilih = input("Pilih: ")
            cleanterminal()
            if pilih == "1":
                tampilanJadwal(jadwal)
            elif pilih == "2":
                addjadwal(jadwal)
            elif pilih == "3":
                ubahjadwal(jadwal)
            elif pilih == "4":
                hapusjadwal(jadwal)
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
            print("\nJangan pencet Ctrl, kembali ke menu utama...")
        tekanenter()

def main():
    users = loaddata(FileUser, Akundefault)
    jadwal = loaddata(FileJadwall, JadwalTiket)
    while True:
        try:
            cleanterminal()
            print("=====================================")
            print("   SISTEM PEMESANAN TIKET KERETA API")
            print("=====================================")
            print("1. Login\n2. Registrasi\n3. Keluar")
            pilih = input("Pilih menu (1-3): ")
            cleanterminal()
            if pilih == "1":
                user = login(users)
                if user:
                    slow()
                    if user["role"] == "admin":
                        menuadmin(user, jadwal)
                    else:
                        print("Menu user masih dikerjakan.....")
                        slow()
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
            print("\nJangan pencet Ctrl, kembali ke menu utama...")
            slow()

try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\nProgram dihentikan.....")

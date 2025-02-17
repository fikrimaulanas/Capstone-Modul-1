import random
import string
import time
from tabulate import tabulate
from colorama import Fore, Style
import pwinput

# Data dummy
contacts = [
    {"id": "A1b@123", "Nama": "Fikri", "Nomor HP": "082273055570", "Alamat": "Jl. Merdeka No.1", "Kode Pos": "20219", "Kota": "Medan"},
    {"id": "B2c#456", "Nama": "Maulana", "Nomor HP": "081281236556", "Alamat": "Jl. Sudirman No.2", "Kode Pos": "40112", "Kota": "Jakarta"},
    {"id": "C3d$789", "Nama": "Stephen", "Nomor HP": "087869770898", "Alamat": "Jl. Gatot Subroto No.3", "Kode Pos": "40113", "Kota": "Jakarta"},
    {"id": "D4e%012", "Nama": "Dwi", "Nomor HP": "081273625253", "Alamat": "Jl. Diponegoro No.4", "Kode Pos": "40114", "Kota": "Surabaya"},
    {"id": "E5f&345", "Nama": "Siregar", "Nomor HP": "081265887868", "Alamat": "Jl. Ahmad Yani No.5", "Kode Pos": "40115", "Kota": "Medan"},
]

recycle_bin = []

# Username dan password user
users = {
    "Dukcapil": "admin123",
    "Rakyat": "rakyatkecil"
}

# Display emergency number
def show_emergency_numbers():
    emergency_numbers = [
        ["Informasi Gangguan Listrik", "123"],
        ["Pemadam Kebakaran", "113"],
        ["Polisi", "110"],
        ["SAR/Basarnas", "115"],
        ["Posko Bencana Alam", "129"],
        ["Panggilan Darurat", "112"]
    ]
    print(f"{Fore.GREEN}\nSELAMAT DATANG DI APLIKASI YELLOW PAGES{Style.RESET_ALL}")
    print(f"{Fore.GREEN}\n===== DAFTAR NOMOR TELEPON DARURAT ====={Style.RESET_ALL}")
    print(tabulate(emergency_numbers, headers=["Layanan", "Nomor"], tablefmt="grid"))

# Fitur otomatis generate unik id untuk kontak yang baru ditambahkan
def generate_unique_id():
    characters = string.ascii_letters + string.digits + "@#$%^&*"
    return ''.join(random.choices(characters, k=7))

# Fitur login
def login():
    show_emergency_numbers()
    attempts = 0
    while attempts < 5:
        username = input("Masukkan username: ")
        password = pwinput.pwinput("Masukkan password: ")
        
        if username in users and users[username] == password:
            print(f"{Fore.GREEN}Login berhasil sebagai {username}{Style.RESET_ALL}")
            return username
        else:
            attempts += 1
            print(f"{Fore.RED}Username atau password salah! Percobaan {attempts}/5.{Style.RESET_ALL}")
    print(f"{Fore.RED}Anda telah gagal login 5 kali.{Style.RESET_ALL}")
    exit()

# Fungsi Read
def show_contacts(user_role):
    print("\nDaftar Kontak:")
    if not contacts:
        print("Kontak kosong.")
    else:
        if user_role == "Rakyat":
            contacts_filtered = [{k: v for k, v in c.items() if k != "id"} for c in contacts]
            print(tabulate(contacts_filtered, headers="keys", tablefmt="grid"))
        else:
            print(tabulate(contacts, headers="keys", tablefmt="grid"))

# Fitur recycle bin
def show_recycle_bin():
    print("\nRecycle Bin:")
    if not recycle_bin:
        print("Recycle Bin kosong.")
    else:
        print(tabulate(recycle_bin, headers="keys", tablefmt="grid"))

# Fungsi Create
def add_contact():
    unique_id = generate_unique_id()
    name = input("Masukkan Nama: ")
    while True:
        phone = input("Masukkan Nomor HP: ")
        if phone.isdigit():
            break
        print(f"{Fore.RED}Hanya menerima angka!{Style.RESET_ALL}")
    address = input("Masukkan Alamat: ")
    while True:
        postal_code = input("Masukkan Kode Pos: ")
        if postal_code.isdigit():
            break
        print(f"{Fore.RED}Hanya menerima angka!{Style.RESET_ALL}")
    city = input("Masukkan Kota: ")
    confirmation = input("Apakah data sudah benar? (y/n): ")
    if confirmation.lower() == 'y':
        contacts.append({"id": unique_id, "Nama": name, "Nomor HP": phone, "Alamat": address, "Kode Pos": postal_code, "Kota": city})
        print(f"{Fore.YELLOW}Kontak {name} berhasil ditambahkan!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Penambahan kontak dibatalkan.{Style.RESET_ALL}")

# Fungsi Update dengan fitur timestamp
def edit_contact():
    attempts = 0
    while attempts < 3:
        unique_id = input("Masukkan ID unik kontak yang ingin diedit: ")
        contact = next((c for c in contacts if c["id"] == unique_id), None)
        if contact:
            print(f"{Fore.CYAN}Data ditemukan:{Style.RESET_ALL}")
            print(tabulate([contact], headers="keys", tablefmt="grid"))
            confirmation = input("Apakah data tersebut sesuai? (y/n): ")
            if confirmation.lower() == 'y':
                old_contact = contact.copy()
                contact["Nama"] = input("Masukkan Nama Baru: ") or contact["Nama"]
                while True:
                    phone = input("Masukkan Nomor HP Baru: ")
                    if phone.isdigit() or phone == "":
                        if phone:
                            contact["Nomor HP"] = phone
                        break
                    print(f"{Fore.RED}Hanya menerima angka!{Style.RESET_ALL}")
                contact["Alamat"] = input("Masukkan Alamat Baru: ") or contact["Alamat"]
                while True:
                    postal_code = input("Masukkan Kode Pos Baru: ")
                    if postal_code.isdigit() or postal_code == "":
                        if postal_code:
                            contact["Kode Pos"] = postal_code
                        break
                    print(f"{Fore.RED}Hanya menerima angka!{Style.RESET_ALL}")
                contact["Kota"] = input("Masukkan Kota Baru: ") or contact["Kota"]
                contact["Updated at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                confirmation = input("Apakah data sudah benar? (y/n): ")
                if confirmation.lower() == 'y':
                    print(f"{Fore.YELLOW}Kontak {contact['Nama']} berhasil diperbarui!{Style.RESET_ALL}")
                else:
                    contact.update(old_contact)
                    print(f"{Fore.RED}Perubahan dibatalkan.{Style.RESET_ALL}")
                return
            else:
                attempts += 1
                print(f"{Fore.RED}Silakan coba input ID unik kembali. Percobaan {attempts}/3.{Style.RESET_ALL}")
        else:
            attempts += 1
            print(f"{Fore.RED}ID unik tidak ditemukan. Percobaan {attempts}/3.{Style.RESET_ALL}")
    print(f"{Fore.RED}Anda telah gagal 3 kali. Program akan keluar.{Style.RESET_ALL}")
    exit()

# Fitur filter dari kota
def filter_contacts_by_city():
    city = input("Masukkan nama kota untuk filter kontak: ")
    filtered_contacts = [contact for contact in contacts if contact["Kota"].lower() == city.lower()]
    if filtered_contacts:
        print(f"{Fore.CYAN}Kontak di kota {city}:{Style.RESET_ALL}")
        print(tabulate(filtered_contacts, headers="keys", tablefmt="grid"))
    else:
        print(f"{Fore.RED}Tidak ada kontak yang ditemukan di kota {city}.{Style.RESET_ALL}")

# Fungsi delete dengan fitur timestamp
def delete_contact():
    unique_id = input("Masukkan ID unik kontak yang ingin dihapus: ")
    contact = next((c for c in contacts if c["id"] == unique_id), None)
    if contact:
        confirmation = input("Apakah Anda yakin ingin menghapus kontak ini? (y/n): ")
        if confirmation.lower() == 'y':
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            recycle_bin.append({**contact, "Deleted at": timestamp})
            contacts.remove(contact)
            print(f"{Fore.YELLOW}Kontak {contact['Nama']} berhasil dihapus dan dipindahkan ke Recycle Bin!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Penghapusan kontak dibatalkan.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}ID unik tidak ditemukan.{Style.RESET_ALL}")

# Fitur restorasi dengan timestamp
def restore_contact():
    unique_id = input("Masukkan ID unik kontak yang ingin dipulihkan: ")
    contact = next((c for c in recycle_bin if c["id"] == unique_id), None)
    if contact:
        contact["Restored at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        contacts.append(contact)
        recycle_bin.remove(contact)
        print(f"{Fore.GREEN}Kontak {contact['Nama']} berhasil dipulihkan!{Style.RESET_ALL}")

# Display main menu dan sub menu
def main():
    user = login()
    while True:
        print("\nMenu:")
        if user == "Dukcapil":
            print("1. Daftar Kontak\n2. Recycle Bin\n3. Keluar")
            choice = input("Pilih menu: ")
            if choice == "1":
                show_contacts(user)
                while True:
                    print("\nSub Menu Daftar Kontak:")
                    print("1. Filter Kontak Berdasarkan Kota\n2. Tambah Kontak\n3. Hapus Kontak\n4. Kembali ke Menu Utama")
                    sub_choice = input("Pilih sub menu: ")
                    if sub_choice == "1":
                        filter_contacts_by_city()
                    elif sub_choice == "2":
                        add_contact()
                    elif sub_choice == "3":
                        delete_contact()
                    elif sub_choice == "4":
                        break
                    else:
                        print(f"{Fore.YELLOW}Pilihan tidak valid!{Style.RESET_ALL}")
            elif choice == "2":
                show_recycle_bin()
                while True:
                    print("\nSub Menu Recycle Bin:")
                    print("1. Restorasi Kontak\n2. Kembali ke Menu Utama")
                    recycle_bin_choice = input("Pilih sub menu: ")
                    if recycle_bin_choice == "1":
                        restore_contact()
                    elif recycle_bin_choice == "2":
                        break
                    else:
                        print(f"{Fore.YELLOW}Pilihan tidak valid!{Style.RESET_ALL}")
            elif choice == "3":
                print(f'{Fore.BLUE}Terimakasih sudah menggunakan Yellow Pages!{Style.RESET_ALL}')
                exit()
            else:
                print(f"{Fore.YELLOW}Pilihan tidak valid!{Style.RESET_ALL}")
        elif user == "Rakyat":
            print("1. Lihat Kontak\n2. Filter Kontak Berdasarkan Kota\n3. Edit Kontak\n4. Keluar")
            choice = input("Pilih menu: ")
            if choice == "1":
                show_contacts(user)
            elif choice == "2":
                filter_contacts_by_city()
            elif choice == "3":
                edit_contact()
            elif choice == "4":
                print(f'{Fore.BLUE}Terimakasih sudah menggunakan Yellow Pages!{Style.RESET_ALL}')
                exit()
            else:
                print(f"{Fore.YELLOW}Pilihan tidak valid!{Style.RESET_ALL}")
if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, messagebox
import random

# ============================================================
#                    WINDOW UTAMA
# ============================================================
root = tk.Tk()
root.title("Pembayaran & Verifikasi Acara - 4 Halaman + 2FA")
root.geometry("600x850")
root.configure(bg="#2B2B2B")

# ============================================================
#                   STYLE TAMPILAN
# ============================================================
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#3A3A3A")
style.configure("TLabel", background="#3A3A3A", foreground="white", font=("Segoe UI", 11))
style.configure("TEntry", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 12, "bold"))

# ============================================================
#        KELAS PESERTA
# ============================================================
class Peserta:
    def __init__(self, nama="", hp="", acara="", jumlah=1, metode="Dana", kode_tiket="", nomor_pembayaran=""):
        self._nama = nama
        self._hp = hp
        self._acara = acara
        self._jumlah = jumlah
        self._metode = metode
        self._kode_tiket = kode_tiket
        self._nomor_pembayaran = nomor_pembayaran

    # Getter
    def get_nama(self): return self._nama
    def get_hp(self): return self._hp
    def get_acara(self): return self._acara
    def get_jumlah(self): return self._jumlah
    def get_metode(self): return self._metode
    def get_kode_tiket(self): return self._kode_tiket
    def get_nomor_pembayaran(self): return self._nomor_pembayaran

# ============================================================
#        VARIABEL GLOBAL & ARRAY
# ============================================================
peserta_terdaftar = []
MAX_PESERTA = 5

# Input halaman 1
nama_var = tk.StringVar()
hp_var = tk.StringVar()
acara_var = tk.StringVar()
jumlah_var = tk.StringVar()
metode_var = tk.StringVar(value="Dana")

# Input halaman 3 (verifikasi)
nama_masuk_var = tk.StringVar()
kode_masuk_var = tk.StringVar()
otp_var = tk.StringVar()
otp_terkirim = ""  # OTP saat ini

# Output halaman
hasil_pembayaran_text = tk.StringVar()
hasil_verifikasi_text = tk.StringVar()
hasil_final_text = tk.StringVar()
riwayat_text = tk.StringVar()

# ============================================================
#        FUNCTION NAVIGASI HALAMAN
# ============================================================
def buka_halaman1():
    halaman2.pack_forget()
    halaman3.pack_forget()
    halaman4.pack_forget()
    hasil_verifikasi_text.set("")
    otp_var.set("")
    otp_entry.config(state="disabled")
    otp_button.config(state="disabled")
    halaman1.pack(fill="both", expand=True)

def buka_halaman2():
    halaman1.pack_forget()
    halaman3.pack_forget()
    halaman4.pack_forget()
    halaman2.pack(fill="both", expand=True)

def buka_halaman3():
    halaman1.pack_forget()
    halaman2.pack_forget()
    halaman4.pack_forget()
    halaman3.pack(fill="both", expand=True)

def buka_halaman4():
    halaman1.pack_forget()
    halaman2.pack_forget()
    halaman3.pack_forget()
    update_riwayat()
    halaman4.pack(fill="both", expand=True)

# ============================================================
#        FUNCTION PENDUKUNG
# ============================================================
def update_riwayat():
    teks = "RIWAYAT PEMBUATAN TIKET:\n\n"
    for i, p in enumerate(peserta_terdaftar, start=1):
        teks += f"{i}. {p.get_nama()} - {p.get_acara()} (Nomor Pembayaran: {p.get_nomor_pembayaran()})\n"
    riwayat_text.set(teks)

def cek_blacklist(nama):
    blacklist = ["budi","ucok","joni"]
    return nama.lower() in blacklist

# ============================================================
#        FUNCTION PEMBUATAN TIKET
# ============================================================
def buat_tiket():
    if len(peserta_terdaftar) >= MAX_PESERTA:
        messagebox.showwarning("Info", "Jumlah peserta sudah maksimal 5 orang!")
        return

    nama = nama_var.get().strip().title()
    hp = hp_var.get().strip()
    acara = acara_var.get().strip()
    try:
        jumlah = int(jumlah_var.get())
        if jumlah != 1:
            raise ValueError
    except:
        messagebox.showerror("Error", "Jumlah tiket harus 1 tiket!")
        return

    if nama=="" or hp=="" or acara=="":
        messagebox.showerror("Error", "Isi semua data!")
        return

    kode_tiket = "TK-" + str(random.randint(10000,99999))
    nomor_pembayaran = "PAY-" + str(random.randint(100000,999999))

    peserta = Peserta(nama, hp, acara, jumlah, metode_var.get(), kode_tiket, nomor_pembayaran)
    peserta_terdaftar.append(peserta)

    hasil_pembayaran_text.set(
        f"TIKET BERHASIL DIBUAT!\n\n"
        f"Nama Peserta: {peserta.get_nama()}\n"
        f"Nomor HP: {peserta.get_hp()}\n"
        f"Acara: {peserta.get_acara()}\n"
        f"Jumlah: {peserta.get_jumlah()} tiket\n"
        f"Metode Pembayaran: {peserta.get_metode()}\n\n"
        f"Nomor Pembayaran: {peserta.get_nomor_pembayaran()}\n"
        f"Kode Tiket: {peserta.get_kode_tiket()}\n\n"
        f"⚠ Jangan sebarkan kode tiket!"
    )
    buka_halaman2()

# ============================================================
#        FUNCTION OTP (2FA)
# ============================================================
def kirim_otp(nama):
    global otp_terkirim
    otp_terkirim = str(random.randint(100000, 999999))
    messagebox.showinfo("OTP Terkirim", f"OTP untuk {nama}: {otp_terkirim}")

def cek_otp():
    otp_input = otp_var.get().strip()
    if otp_input == otp_terkirim:
        for p in peserta_terdaftar:
            if p.get_nama() == nama_masuk_var.get().strip().title():
                hasil_final_text.set(
                    f"VERIFIKASI BERHASIL!\n\n"
                    f"Selamat {p.get_nama()}!\n"
                    f"Nomor HP: {p.get_hp()}\n"
                    f"Anda dinyatakan sah sebagai peserta acara.\n\n"
                    f"Silahkan menuju ke tempat yang sudah disediakan.\n"
                )
                otp_entry.config(state="disabled")
                otp_button.config(state="disabled")
                buka_halaman4()
                break
    else:
        messagebox.showerror("Error", "OTP salah! Silahkan coba lagi.")

# ============================================================
#        FUNCTION VERIFIKASI PESERTA
# ============================================================
def cek_peserta():
    nama_masuk = nama_masuk_var.get().strip().title()
    kode_masuk = kode_masuk_var.get().strip()

    if nama_masuk=="" or kode_masuk=="":
        messagebox.showerror("Error", "Isi nama & kode tiket!")
        return

    if cek_blacklist(nama_masuk):
        hasil_verifikasi_text.set("❌ Nama ini masuk daftar blacklist!")
        return

    found = False
    for p in peserta_terdaftar:
        if p.get_nama() == nama_masuk and p.get_kode_tiket() == kode_masuk:
            found = True
            kirim_otp(nama_masuk)
            hasil_verifikasi_text.set("✔ Nama & kode tiket cocok! Masukkan OTP yang dikirim.")
            otp_entry.config(state="normal")
            otp_button.config(state="normal")
            break

    if not found:
        hasil_verifikasi_text.set("❌ PENYUSUP TERDETEKSI!\nNama atau kode tiket SALAH.")

# ============================================================
#        HALAMAN 1 — Pendaftaran Peserta
# ============================================================
halaman1 = ttk.Frame(root, padding=20)
tk.Label(halaman1, text="Halaman 1 — Pendaftaran Peserta",
         fg="white", bg="#2B2B2B", font=("Segoe UI", 20, "bold")).pack(pady=20)

tk.Label(halaman1, text="Nama Peserta:", bg="#3A3A3A", fg="white").pack(anchor="w")
ttk.Entry(halaman1, textvariable=nama_var).pack(fill="x")
tk.Label(halaman1, text="Nomor HP:", bg="#3A3A3A", fg="white").pack(anchor="w", pady=(10,0))
ttk.Entry(halaman1, textvariable=hp_var).pack(fill="x")
tk.Label(halaman1, text="Nama Acara:", bg="#3A3A3A", fg="white").pack(anchor="w", pady=(10,0))
ttk.Entry(halaman1, textvariable=acara_var).pack(fill="x")
tk.Label(halaman1, text="Jumlah Tiket (max:1 tiket):", bg="#3A3A3A", fg="white").pack(anchor="w", pady=(10,0))
ttk.Entry(halaman1, textvariable=jumlah_var).pack(fill="x")
tk.Label(halaman1, text="Metode Pembayaran:", bg="#3A3A3A", fg="white").pack(anchor="w", pady=(10,0))
ttk.Combobox(halaman1, values=["Dana","OVO","Gopay"], textvariable=metode_var).pack(fill="x")
ttk.Button(halaman1, text="Buat Tiket", command=buat_tiket).pack(pady=20)

# ============================================================
#        HALAMAN 2 — Hasil Pembayaran
# ============================================================
halaman2 = ttk.Frame(root, padding=20)
tk.Label(halaman2, text="Halaman 2 — Hasil Pembayaran",
         fg="white", bg="#2B2B2B", font=("Segoe UI", 20, "bold")).pack(pady=20)
tk.Label(halaman2, textvariable=hasil_pembayaran_text, bg="#3A3A3A", fg="white",
         font=("Segoe UI",12), justify="left", wraplength=500).pack(pady=20)
ttk.Button(halaman2, text="Lanjut ke Verifikasi", command=buka_halaman3).pack(pady=5)
ttk.Button(halaman2, text="Kembali", command=buka_halaman1).pack()

# ============================================================
#        HALAMAN 3 — Verifikasi Peserta + OTP
# ============================================================
halaman3 = ttk.Frame(root, padding=20)
tk.Label(halaman3, text="Halaman 3 — Verifikasi Peserta",
         fg="white", bg="#2B2B2B", font=("Segoe UI", 20, "bold")).pack(pady=20)

tk.Label(halaman3, text="Nama Peserta:", bg="#3A3A3A", fg="white").pack(anchor="w")
ttk.Entry(halaman3, textvariable=nama_masuk_var).pack(fill="x")
tk.Label(halaman3, text="Kode Tiket:", bg="#3A3A3A", fg="white").pack(anchor="w", pady=(10,0))
ttk.Entry(halaman3, textvariable=kode_masuk_var).pack(fill="x")

ttk.Button(halaman3, text="Verifikasi", command=cek_peserta).pack(pady=10)

tk.Label(halaman3, text="Masukkan OTP:", bg="#3A3A3A", fg="white").pack(anchor="w", pady=(10,0))
otp_entry = ttk.Entry(halaman3, textvariable=otp_var, state="disabled")
otp_entry.pack(fill="x")
otp_button = ttk.Button(halaman3, text="Verifikasi OTP", command=cek_otp, state="disabled")
otp_button.pack(pady=10)

tk.Label(halaman3, textvariable=hasil_verifikasi_text, bg="#3A3A3A", fg="white",
         font=("Segoe UI",12), wraplength=400).pack(pady=20)
ttk.Button(halaman3, text="Kembali ke Awal", command=buka_halaman1).pack()

# ============================================================
#        HALAMAN 4 — Hasil Verifikasi + Riwayat
# ============================================================
halaman4 = ttk.Frame(root, padding=20)
tk.Label(halaman4, text="Halaman 4 — Hasil Verifikasi",
         fg="white", bg="#2B2B2B", font=("Segoe UI", 20, "bold")).pack(pady=20)
tk.Label(halaman4, textvariable=hasil_final_text, bg="#3A3A3A", fg="white",
         font=("Segoe UI",12), justify="left", wraplength=500).pack(pady=20)
# Hanya Nomor Pembayaran di riwayat, bukan kode tiket
tk.Label(halaman4, textvariable=riwayat_text, bg="#3A3A3A", fg="white",
         font=("Segoe UI",11), justify="left", wraplength=500).pack(pady=20)
ttk.Button(halaman4, text="Kembali ke Halaman Utama", command=buka_halaman1).pack(pady=10)

# ============================================================
#                     START
# ============================================================
buka_halaman1()
root.mainloop()

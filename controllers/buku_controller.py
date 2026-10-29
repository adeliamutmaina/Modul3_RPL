
# Adelia Mutmaina 012
import customtkinter as ctk
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role.lower()
        self.model = BukuModel()
        self.view = BukuView()
        self.selected_id = None

        # Menyesuaikan judul jendela
        self.view.title(
            f"Sistem Manajemen Perpustakaan - Role: {self.user_role.upper()}")

        # Menghubungkan tabel dengan fungsi pilih buku
        self.view.tabel.bind(
            "<<TreeviewSelect>>", self.pilih_buku)

        # Mengatur tombol berdasarkan role pengguna
        if self.user_role == "admin":
            self.view.btn_simpan.configure(command=self.simpan_data)
            self.view.btn_update.configure(command=self.perbarui_data)
            self.view.btn_hapus.configure(command=self.hapus_data)

        else:
            # Tombol tetap terlihat, tetapi dikunci
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")

            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")

            # Nonaktifkan kolom input
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        # Menghubungkan tombol Logout untuk semua pengguna
        self.view.btn_logout.configure(command=self.logout, state="normal")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan isi tabel
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Mengambil data buku dari database
        data_buku = self.model.get_all_buku()

        if data_buku:
            for buku in data_buku:
                self.view.tabel.insert("", "end",
                    values=(buku["id_buku"], buku["judul"],
                            buku["penulis"], buku["tahun_terbit"]))

    def pilih_buku(self, event=None):
        # Mengambil buku yang dipilih pada tabel
        pilihan = self.view.tabel.selection()

        if not pilihan:
            self.selected_id = None
            return

        data = self.view.tabel.item(pilihan[0], "values")
        self.selected_id = data[0]

        # Anggota hanya boleh melihat data
        if self.user_role != "admin":
            return

        # Mengisi form dengan data buku terpilih
        self.view.entry_judul.delete(0, "end")
        self.view.entry_judul.insert(0, data[1])

        self.view.entry_penulis.delete(0, "end")
        self.view.entry_penulis.insert(0, data[2])

        self.view.entry_tahun.delete(0, "end")
        self.view.entry_tahun.insert(0, data[3])

    def simpan_data(self):
        # Memeriksa hak akses
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Hanya admin yang boleh menambah buku!")
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if not tahun.isdigit():
            messagebox.showwarning("Peringatan", "Tahun terbit harus berupa angka!")
            return

        try:
            berhasil = self.model.create_buku(
                judul, penulis, int(tahun)
            )

            if berhasil:
                messagebox.showinfo("Sukses", "Buku berhasil disimpan!")
                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Gagal", "Buku gagal disimpan.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def perbarui_data(self):
        # Memeriksa hak akses
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Hanya admin yang boleh memperbarui buku!")
            return

        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih buku pada tabel terlebih dahulu!")
            return

        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if not tahun.isdigit():
            messagebox.showwarning("Peringatan", "Tahun terbit harus berupa angka!")
            return

        if not hasattr(self.model, "update_buku"):
            messagebox.showerror("Error","Metode update_buku() belum tersedia di BukuModel.")
            return

        try:
            berhasil = self.model.update_buku(self.selected_id, judul, penulis, int(tahun))

            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Gagal", "Data buku gagal diperbarui.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def hapus_data(self):
        # Memeriksa hak akses
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak","Hanya admin yang boleh menghapus buku!")
            return

        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih buku pada tabel terlebih dahulu!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi","Apakah kamu yakin ingin menghapus buku ini?")

        if not konfirmasi:
            return

        if not hasattr(self.model, "delete_buku"):
            messagebox.showerror("Error", "Metode delete_buku() belum tersedia di BukuModel.")
            return

        try:
            berhasil = self.model.delete_buku(self.selected_id)

            if berhasil:
                messagebox.showinfo("Sukses", "Buku berhasil dihapus!")
                self.kosongkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Gagal", "Buku gagal dihapus.")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def kosongkan_form(self):
        self.selected_id = None

        # Mengosongkan form hanya untuk admin
        if self.user_role == "admin":
            self.view.entry_judul.delete(0, "end")
            self.view.entry_penulis.delete(0, "end")
            self.view.entry_tahun.delete(0, "end")

        # Menghapus pilihan pada tabel
        for item in self.view.tabel.selection():
            self.view.tabel.selection_remove(item)

    def logout(self):
        # Menutup jendela perpustakaan
        self.view.destroy()

        # Membuka kembali halaman login
        from controllers.auth_controller import AuthController
        login = AuthController()
        login.run()

    def run(self):
        self.view.mainloop()
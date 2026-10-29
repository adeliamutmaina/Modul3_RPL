#
import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView


class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()
        self.id_anggota_terpilih = None

        self.view.btn_simpan.configure(
            command=self.simpan_data
        )
        self.view.btn_hapus.configure(
            command=self.hapus_data
        )
        self.view.btn_update.configure(
            command=self.perbarui_data
        )

        self.view.tabel.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_anggota = self.model.get_all_anggota()

        for anggota in data_anggota:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    anggota["id_anggota"],
                    anggota["nama"],
                    anggota["alamat"],
                    anggota["telepon"]
                )
            )

    def pilih_data(self, event=None):
        pilihan = self.view.tabel.selection()

        if not pilihan:
            return

        data = self.view.tabel.item(
            pilihan[0], "values"
        )

        self.id_anggota_terpilih = data[0]

        self.view.entry_nama.delete(0, "end")
        self.view.entry_nama.insert(0, data[1])

        self.view.entry_alamat.delete(0, "end")
        self.view.entry_alamat.insert(0, data[2])

        self.view.entry_telepon.delete(0, "end")
        self.view.entry_telepon.insert(0, data[3])

    def simpan_data(self):
        nama = self.view.entry_nama.get().strip()
        alamat = self.view.entry_alamat.get().strip()
        telepon = self.view.entry_telepon.get().strip()

        if not nama or not alamat or not telepon:
            messagebox.showwarning(
                "Peringatan", "Semua kolom harus diisi!"
            )
            return

        berhasil = self.model.create_anggota(
            nama, alamat, telepon
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses", "Data anggota berhasil disimpan!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error", "Data anggota gagal disimpan!"
            )

    def hapus_data(self):
        if self.id_anggota_terpilih is None:
            messagebox.showwarning(
                "Peringatan", "Pilih anggota terlebih dahulu!"
            )
            return

        if not messagebox.askyesno(
            "Konfirmasi", "Hapus data anggota yang dipilih?"
        ):
            return

        if self.model.delete_anggota(
            self.id_anggota_terpilih
        ):
            messagebox.showinfo(
                "Sukses", "Data anggota berhasil dihapus!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error", "Data anggota gagal dihapus!"
            )

    def perbarui_data(self):
        if self.id_anggota_terpilih is None:
            messagebox.showwarning(
                "Peringatan", "Pilih anggota terlebih dahulu!"
            )
            return

        nama = self.view.entry_nama.get().strip()
        alamat = self.view.entry_alamat.get().strip()
        telepon = self.view.entry_telepon.get().strip()

        if not nama or not alamat or not telepon:
            messagebox.showwarning(
                "Peringatan", "Semua kolom harus diisi!"
            )
            return

        berhasil = self.model.update_anggota(
            self.id_anggota_terpilih,
            nama,
            alamat,
            telepon
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses", "Data anggota berhasil diperbarui!"
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error", "Data anggota gagal diperbarui!"
            )

    def bersihkan_form(self):
        self.view.entry_nama.delete(0, "end")
        self.view.entry_alamat.delete(0, "end")
        self.view.entry_telepon.delete(0, "end")
        self.id_anggota_terpilih = None

        pilihan = self.view.tabel.selection()
        if pilihan:
            self.view.tabel.selection_remove(*pilihan)

    def run(self):
        self.view.mainloop()

# Adelia Mutmaina 012
from config.database import Database

class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    def get_all_buku(self):
        if not self.conn:
            print("Koneksi database tidak tersedia.")
            return []

        cursor = None

        try:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print("Error mengambil data buku:", repr(e))
            return []

        finally:
            if cursor:
                cursor.close()

    def create_buku(self, judul, penulis, tahun_terbit):
        if not self.conn:
            print("Koneksi database tidak tersedia.")
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = f"""
                INSERT INTO {self.table_name}
                (judul, penulis, tahun_terbit)
                VALUES (%s, %s, %s)
            """

            values = (judul, penulis, tahun_terbit)
            cursor.execute(query, values)
            self.conn.commit()

            return True

        except Exception as e:
            self.conn.rollback()
            print("Error menyimpan data buku:", repr(e))
            return False

        finally:
            if cursor:
                cursor.close()

    def delete_buku(self, id_buku):
        if not self.conn:
            print("Koneksi database tidak tersedia.")
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = f"""
                DELETE FROM {self.table_name}
                WHERE id_buku = %s
            """

            cursor.execute(query, (id_buku,))
            berhasil = cursor.rowcount > 0
            self.conn.commit()

            return berhasil

        except Exception as e:
            self.conn.rollback()
            print("Error menghapus buku:", repr(e))
            return False

        finally:
            if cursor:
                cursor.close()

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if not self.conn:
            print("Koneksi database tidak tersedia.")
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            query = f"""
                UPDATE {self.table_name}
                SET judul = %s,
                    penulis = %s,
                    tahun_terbit = %s
                WHERE id_buku = %s
            """

            values = (judul, penulis, tahun_terbit, id_buku)
            cursor.execute(query, values)

            # rowcount dapat bernilai 0 jika data tidak berubah.
            # Periksa apakah buku dengan ID tersebut masih ada.
            if cursor.rowcount == 0:
                cursor.execute(
                    f"SELECT id_buku FROM {self.table_name} "
                    "WHERE id_buku = %s",
                    (id_buku,)
                )

                data = cursor.fetchone()

                if data is None:
                    self.conn.rollback()
                    print(
                        f"Buku dengan ID {id_buku} tidak ditemukan."
                    )
                    return False

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            print("Error memperbarui buku:", repr(e))
            return False

        finally:
            if cursor:
                cursor.close()
import sqlite3

DB_NAME = "keuangan.db"

def init_db():
    """Membuat tabel transaksi jika belum ada di database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
            tipe TEXT,
            kategori TEXT,
            nominal REAL,
            keterangan TEXT
        )
    ''')
    conn.commit()
    conn.close()

def simpan_transaksi(tipe, kategori, nominal, keterangan):
    """Menyimpan data transaksi baru ke dalam database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transaksi (tipe, kategori, nominal, keterangan) VALUES (?, ?, ?, ?)",
        (tipe, kategori, nominal, keterangan)
    )
    conn.commit()
    conn.close()

def ambil_rekap():
    """Mengambil total pengeluaran dan pemasukan dari database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(nominal) FROM transaksi WHERE tipe = 'pengeluaran'")
    total_pengeluaran = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(nominal) FROM transaksi WHERE tipe = 'pemasukan'")
    total_pemasukan = cursor.fetchone()[0] or 0
    
    conn.close()
    return total_pemasukan, total_pengeluaran
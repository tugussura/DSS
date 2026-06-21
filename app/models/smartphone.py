from app import db

class Smartphone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Float, nullable=False) # Harga dalam Rupiah
    foto = db.Column(db.Float, nullable=False) # Skor Foto (1-100)
    video = db.Column(db.Float, nullable=False) # Skor Video (1-100)
    chipset = db.Column(db.Float, nullable=False) # Performa Chipset (Skor AnTuTu e.g., dalam puluhan ribu)
    baterai = db.Column(db.Float, nullable=False) # Kapasitas Baterai (mAh)
    storage = db.Column(db.Float, nullable=False) # Kapasitas Penyimpanan (GB)

    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'harga': self.harga,
            'foto': self.foto,
            'video': self.video,
            'chipset': self.chipset,
            'baterai': self.baterai,
            'storage': self.storage
        }

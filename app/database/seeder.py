from app import db
from app.models.smartphone import Smartphone

def seed_data():
    if Smartphone.query.count() == 0:
        smartphones = [
            Smartphone(nama="Huawei Pura 80 Ultra", foto=180, video=166, chipset=59, baterai=5170, storage=512, harga=17500000),
            Smartphone(nama="Vivo x300 Pro", foto=171, video=169, chipset=96, baterai=6510, storage=512, harga=19000000),
            Smartphone(nama="Oppo Find X9 Pro", foto=169, video=159, chipset=96, baterai=7500, storage=512, harga=20000000),
            Smartphone(nama="Xiaomi 17 Ultra", foto=170, video=157, chipset=97, baterai=6000, storage=1000, harga=23000000),
            Smartphone(nama="Iphone 17 Pro Max", foto=166, video=172, chipset=93, baterai=4832, storage=2000, harga=45000000),
            Smartphone(nama="Xiaomi 15T Pro", foto=152, video=144, chipset=88, baterai=5500, storage=1000, harga=11500000),
            Smartphone(nama="Tecno Camon 50 Ultra", foto=154, video=132, chipset=41, baterai=6500, storage=256, harga=5350000),
            Smartphone(nama="Tecno Camon 50", foto=146, video=134, chipset=31, baterai=6500, storage=128, harga=3500000),
            Smartphone(nama="Samsung Galaxy S26 Ultra", foto=160, video=153, chipset=97, baterai=5000, storage=512, harga=25600000),
            Smartphone(nama="Iphone 13 Pro Max", foto=140, video=146, chipset=66, baterai=4352, storage=256, harga=11000000),
            Smartphone(nama="Iphone 15", foto=147, video=153, chipset=73, baterai=3349, storage=256, harga=14750000),
            Smartphone(nama="Redmi note 14 pro 5g", foto=103, video=117, chipset=38, baterai=5110, storage=256, harga=3770000),
            Smartphone(nama="Samsung A56", foto=117, video=108, chipset=49, baterai=5000, storage=256, harga=6300000),
            Smartphone(nama="Iphone 13", foto=133, video=144, chipset=66, baterai=3227, storage=128, harga=7450000),
            Smartphone(nama="Xiaomi 14t", foto=130, video=133, chipset=57, baterai=5000, storage=512, harga=6500000)
        ]
        db.session.bulk_save_objects(smartphones)
        db.session.commit()
        print("Database seeded with initial smartphone data.")

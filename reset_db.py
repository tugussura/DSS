from app import create_app, db
from app.database.seeder import seed_data

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_data()
    print("Database recreated and seeded successfully.")

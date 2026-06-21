from app import create_app, db
from app.database.seeder import seed_data
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure database directory exists
        db_dir = os.path.join(os.path.dirname(__file__), 'app', 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        # Create all tables
        db.create_all()
        
        # Seed initial data if database is empty
        seed_data()
        
    app.run(debug=True, port=5001)

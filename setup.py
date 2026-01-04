import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_database():
    """Setup the database"""
    print("Setting up database...")
    from app import create_app
    from app.models import db
    
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created.")

def seed_database():
    """Seed the database with initial data"""
    print("Seeding database...")
    import seed
    print("Database seeded successfully.")

if __name__ == '__main__':
    install_requirements()
    setup_database()
    seed_database()
    print("\nSetup complete! Run the app with: python run.py")
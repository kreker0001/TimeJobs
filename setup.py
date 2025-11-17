# setup.py
import subprocess
import sys

def install_requirements():
    packages = [
        'Flask==2.3.3',
        'Flask-SQLAlchemy==3.0.5', 
        'Flask-Login==0.6.3',
        'psycopg2-binary==2.9.7',
        'Werkzeug==2.3.7',
        'python-dotenv==1.0.0'
    ]
    
    for package in packages:
        print(f"Устанавливаю {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_requirements()
    print("Все зависимости установлены!")
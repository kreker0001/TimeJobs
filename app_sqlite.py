# app_sqlite.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timejobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модели
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False, default='worker')
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    city = db.Column(db.String(100))
    wage = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='approved')  # approved для теста
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Маршруты
@app.route('/')
def index():
    jobs = Job.query.filter_by(status='approved').order_by(Job.created_at.desc()).limit(6).all()
    return render_template('index.html', jobs=jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        
        return render_template('auth/login.html', error='Неверные данные')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'worker')
        
        if User.query.filter_by(email=email).first():
            return render_template('auth/register.html', error='Email уже используется')
        
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/vacancies')
def vacancies():
    jobs = Job.query.filter_by(status='approved').order_by(Job.created_at.desc()).all()
    return render_template('vacancies/list.html', jobs=jobs)

# Создадим несколько тестовых вакансий
def create_sample_data():
    if not Job.query.first():
        jobs = [
            Job(
                title='Разнорабочий на стройку',
                description='Требуется разнорабочий для помощи на строительном объекте. Работа в команде, ответственность.',
                city='Москва',
                wage=1500
            ),
            Job(
                title='Маляр-штукатур',
                description='Нужен опытный маляр для отделочных работ в новостройке. Опыт работы от 1 года.',
                city='Санкт-Петербург', 
                wage=2000
            ),
            Job(
                title='Укладчик плитки',
                description='Требуется специалист по укладке керамической плитки. Собственные инструменты приветствуются.',
                city='Казань',
                wage=1800
            )
        ]
        db.session.add_all(jobs)
        db.session.commit()
        print("Созданы тестовые вакансии")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    
    print("Сервер запущен: http://localhost:5000")
    app.run(debug=True, port=5000)
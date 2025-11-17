from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint
import os, datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'  # поменяй на свой
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'time_jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='worker')  # worker, employer, moderator
    phone = db.Column(db.String(50))
    education = db.Column(db.String(255))
    exp_years = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(255))


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    city = db.Column(db.String(120))
    specialization = db.Column(db.String(120))
    wage = db.Column(db.Float, default=0)
    pay_type = db.Column(db.String(20), default='shift')  # shift, hourly
    duration_days = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    employer = db.relationship('User', backref='jobs')


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text)
    status = db.Column(db.String(20), default='applied')  # applied, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    job = db.relationship('Job', backref='applications')
    worker = db.relationship('User')

    __table_args__ = (
        UniqueConstraint('job_id', 'worker_id', name='uq_job_worker'),
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_globals():
    import urllib.parse
    def default_avatar(name):
        n = urllib.parse.quote_plus(name or "U")
        return f"https://ui-avatars.com/api/?background=4CFA00&color=fff&name={n}"
    return dict(current_user=current_user, default_avatar=default_avatar)


@app.route('/')
def index():
    active_jobs = Job.query.filter_by(status='approved').count()
    workers = User.query.filter_by(role='worker').count()
    employers = User.query.filter_by(role='employer').count()
    stats = dict(active_jobs=active_jobs, workers=workers, employers=employers)

    last_jobs = Job.query.filter_by(status='approved') \
                         .order_by(Job.created_at.desc()).limit(6).all()
    return render_template('index.html', stats=stats, last_jobs=last_jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'worker')

        if not name or not email or not password:
            flash('Заполните все поля', 'error')
        else:
            if User.query.filter_by(email=email).first():
                flash('Пользователь с такой почтой уже существует', 'error')
            else:
                user = User(
                    name=name,
                    email=email,
                    password_hash=generate_password_hash(password),
                    role=role if role in ['worker', 'employer', 'moderator'] else 'worker'
                )
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Вы успешно зарегистрированы', 'success')
                return redirect(url_for('index'))

    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Вы вошли в аккаунт', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверная почта или пароль', 'error')

    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('index'))


@app.route('/vacancies')
def vacancies():
    search = request.args.get('search', '').strip()
    query = Job.query.filter_by(status='approved')
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Job.title.ilike(like),
                Job.city.ilike(like),
                Job.specialization.ilike(like),
                Job.description.ilike(like)
            )
        )
    jobs = query.order_by(Job.created_at.desc()).all()
    return render_template('vacancies/list.html', jobs=jobs)


@app.route('/vacancies/<int:job_id>')
def vacancy_detail(job_id):
    job = Job.query.get_or_404(job_id)
    if job.status != 'approved':
        # показываем неопубликованную только её владельцу-работодателю
        if not (current_user.is_authenticated and
                current_user.role == 'employer' and
                job.employer_id == current_user.id):
            flash('Вакансия ещё не опубликована', 'error')
            return redirect(url_for('vacancies'))
    return render_template('vacancies/detail.html', job=job)


@app.route('/vacancies/<int:job_id>/apply', methods=['POST'])
@login_required
def apply(job_id):
    if current_user.role != 'worker':
        flash('Только соискатели могут откликаться на вакансии', 'error')
        return redirect(url_for('vacancy_detail', job_id=job_id))

    job = Job.query.get_or_404(job_id)

    # проверка: профиль должен быть заполнен (хотя бы телефон)
    if not current_user.phone:
        flash('Заполните профиль (укажите телефон), прежде чем откликаться', 'error')
        return redirect(url_for('profile'))

    # проверка на повторный отклик
    if Application.query.filter_by(job_id=job.id, worker_id=current_user.id).first():
        flash('Вы уже откликались на эту вакансию', 'error')
        return redirect(url_for('vacancy_detail', job_id=job_id))

    note = request.form.get('note', '').strip()
    app_obj = Application(job_id=job.id, worker_id=current_user.id, note=note)
    db.session.add(app_obj)
    db.session.commit()
    flash('Отклик отправлен', 'success')
    return redirect(url_for('vacancy_detail', job_id=job_id))


@app.route('/vacancies/create', methods=['GET', 'POST'])
@login_required
def create_vacancy():
    if current_user.role != 'employer':
        flash('Только компания может размещать вакансии', 'error')
        return redirect(url_for('vacancies'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Название обязательно', 'error')
        else:
            job = Job(
                employer_id=current_user.id,
                title=title,
                description=request.form.get('description') or '',
                city=request.form.get('city') or '',
                specialization=request.form.get('specialization') or '',
                wage=float(request.form.get('wage') or 0),
                pay_type=request.form.get('pay_type') or 'shift',
                duration_days=int(request.form.get('duration_days') or 1),
                status='pending'  # сначала на модерацию
            )
            db.session.add(job)
            db.session.commit()
            flash('Вакансия отправлена на модерацию', 'success')
            return redirect(url_for('vacancies'))

    return render_template('vacancies/create.html')


@app.route('/manage')
@login_required
def manage():
    if current_user.role not in ('employer', 'moderator'):
        flash('Недостаточно прав', 'error')
        return redirect(url_for('index'))

    if current_user.role == 'employer':
        jobs = Job.query.filter_by(employer_id=current_user.id) \
                        .order_by(Job.created_at.desc()).all()
    else:
        # модератор видит все pending
        jobs = Job.query.filter_by(status='pending') \
                        .order_by(Job.created_at.desc()).all()

    return render_template('manage.html', jobs=jobs)


@app.route('/manage/job/<int:job_id>/status/<string:action>', methods=['POST'])
@login_required
def change_job_status(job_id, action):
    job = Job.query.get_or_404(job_id)

    if current_user.role == 'employer':
        if job.employer_id != current_user.id:
            flash('Вы не можете менять эту вакансию', 'error')
            return redirect(url_for('manage'))
        if action == 'close':
            job.status = 'rejected'
        else:
            flash('Неверное действие', 'error')
            return redirect(url_for('manage'))

    elif current_user.role == 'moderator':
        if action == 'approve':
            job.status = 'approved'
        elif action == 'reject':
            job.status = 'rejected'
        else:
            flash('Неверное действие', 'error')
            return redirect(url_for('manage'))
    else:
        flash('Недостаточно прав', 'error')
        return redirect(url_for('index'))

    db.session.commit()
    flash('Статус вакансии обновлён', 'success')
    return redirect(url_for('manage'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.phone = request.form.get('phone') or None
        current_user.education = request.form.get('education') or None
        current_user.exp_years = int(request.form.get('exp_years') or 0)
        db.session.commit()
        flash('Профиль обновлён', 'success')
        return redirect(url_for('profile'))
    return render_template('profile/index.html')


@app.route('/my-applications')
@login_required
def my_applications():
    if current_user.role != 'worker':
        flash('Страница доступна только соискателям', 'error')
        return redirect(url_for('index'))

    apps = Application.query.filter_by(worker_id=current_user.id) \
                            .order_by(Application.created_at.desc()).all()
    return render_template('my_applications.html', applications=apps)


def init_db():
    db.create_all()
    # создаём модератора по умолчанию
    if not User.query.filter_by(email='admin@tj.local').first():
        admin = User(
            name='Модератор',
            email='admin@tj.local',
            password_hash=generate_password_hash('admin'),
            role='moderator'
        )
        db.session.add(admin)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

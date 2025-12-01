<<<<<<< ours
﻿from flask import Flask, render_template, redirect, url_for, request, flash
=======
from flask import Flask, render_template, redirect, url_for, request, flash, session
>>>>>>> theirs
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user, UserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
<<<<<<< ours
from sqlalchemy import UniqueConstraint
=======
from sqlalchemy import UniqueConstraint, inspect, text
>>>>>>> theirs
import os, datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
<<<<<<< ours
app.config['SECRET_KEY'] = 'change-this-secret-key' 
=======
app.config['SECRET_KEY'] = 'change-this-secret-key'  # Р В РЎвЂ”Р В РЎвЂўР В РЎР В Р’ВµР В Р вЂ¦Р РЋР РЏР В РІвЂћвЂ“ Р В Р вЂ¦Р В Р’В° Р РЋР С“Р В Р вЂ Р В РЎвЂўР В РІвЂћвЂ“
>>>>>>> theirs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'time_jobs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


<<<<<<< ours
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
=======
def redirect_back(default_endpoint):
    target = request.referrer
    try:
        if target:
            return redirect(target)
    except Exception:
        pass
    return redirect(url_for(default_endpoint))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    middle_name = db.Column(db.String(120))
    gender = db.Column(db.String(20))
    city = db.Column(db.String(120))
    birth_date = db.Column(db.Date)
>>>>>>> theirs
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='worker')  # worker, employer, moderator
    phone = db.Column(db.String(50))
    education = db.Column(db.String(255))
    exp_years = db.Column(db.Integer, default=0)
    avatar_url = db.Column(db.String(255))
<<<<<<< ours
    rating = db.Column(db.Float, default=0)
=======
    deposit = db.Column(db.Float, default=0)
    rating = db.Column(db.Float, default=0)
    educations = db.relationship('WorkerEducation', backref='user', lazy=True, cascade='all, delete-orphan')
    experiences = db.relationship('WorkerExperience', backref='user', lazy=True, cascade='all, delete-orphan')
    skills = db.relationship('WorkerSkill', backref='user', lazy=True, cascade='all, delete-orphan')
>>>>>>> theirs


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
<<<<<<< ours
=======
    view_count = db.Column(db.Integer, default=0)
    experience_level = db.Column(db.String(50))
    employment_type = db.Column(db.String(50))
    tariff = db.Column(db.String(50))
>>>>>>> theirs

    employer = db.relationship('User', backref='jobs')


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text)
    status = db.Column(db.String(20), default='applied')  # applied, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
<<<<<<< ours

    job = db.relationship('Job', backref='applications')
    worker = db.relationship('User')
=======
    frozen_amount = db.Column(db.Float, default=0)
    work_units = db.Column(db.Integer, default=0)

    job = db.relationship('Job', backref='applications')
    worker = db.relationship('User')
    messages = db.relationship(
        'ChatMessage',
        backref='application',
        lazy=True,
        cascade='all, delete-orphan'
    )
>>>>>>> theirs

    __table_args__ = (
        UniqueConstraint('job_id', 'worker_id', name='uq_job_worker'),
    )


<<<<<<< ours
=======
class ChatMessage(db.Model):
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_system = db.Column(db.Boolean, default=False)

    sender = db.relationship('User')


def add_chat_message(application_obj, text, is_system=False, sender=None):
    """Utility to append a chat message, used for system notifications."""
    sender_id = None
    if sender:
        sender_id = sender.id
    elif current_user and getattr(current_user, 'is_authenticated', False):
        sender_id = current_user.id
    else:
        sender_id = application_obj.job.employer_id if application_obj.job else application_obj.worker_id

    msg = ChatMessage(
        application_id=application_obj.id,
        sender_id=sender_id,
        text=text,
        is_system=is_system
    )
    db.session.add(msg)
    return msg


class WorkerEducation(db.Model):
    __tablename__ = 'worker_education'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.String(120))
    institution = db.Column(db.String(255))
    faculty = db.Column(db.String(255))
    specialization = db.Column(db.String(255))
    graduation_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class WorkerExperience(db.Model):
    __tablename__ = 'worker_experience'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(255))
    title = db.Column(db.String(255))
    duties = db.Column(db.Text)
    start_month = db.Column(db.String(20))
    start_year = db.Column(db.Integer)
    end_month = db.Column(db.String(20))
    end_year = db.Column(db.Integer)
    is_current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class WorkerSkill(db.Model):
    __tablename__ = 'worker_skill'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    is_key = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


>>>>>>> theirs
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_globals():
    import urllib.parse
    from flask import request, url_for

    def default_avatar(name):
        n = urllib.parse.quote_plus(name or "U")
        return f"https://ui-avatars.com/api/?background=4CFA00&color=fff&name={n}"

<<<<<<< ours
=======
    # Р В РЎвЂўР В РЎвЂ”Р РЋР вЂљР В Р’ВµР В РўвЂР В Р’ВµР В Р’В»Р РЋР РЏР В Р’ВµР В РЎ, Р В РЎвЂќР В Р’В°Р В РЎвЂќР В РЎвЂўР В РІвЂћвЂ“ Р В РЎвЂ”Р РЋРЎвЂњР В Р вЂ¦Р В РЎвЂќР РЋРІР‚С™ Р В РЎР В Р’ВµР В Р вЂ¦Р РЋР вЂ№ Р В Р’В°Р В РЎвЂќР РЋРІР‚С™Р В РЎвЂР В Р вЂ Р В Р’ВµР В Р вЂ¦
>>>>>>> theirs
    def get_active_page():
        path = request.path

        if path == url_for('index'):
            return 'index'
<<<<<<< ours
        # /vacancies ╨╕ /vacancies/123
        if path.startswith(url_for('vacancies')):
            return 'vacancies'
        if path.startswith(url_for('my_applications')):
            return 'my_applications'
=======
        # /vacancies Р В РЎвЂ /vacancies/123
        if path.startswith(url_for('vacancies')):
            return 'vacancies'
        if path.startswith('/applications/'):
            if current_user.is_authenticated and current_user.role == 'worker':
                return 'my_applications'
            if current_user.is_authenticated and current_user.role == 'employer':
                return 'manage'
        if path.startswith(url_for('my_applications')):
            return 'my_applications'
        if path.startswith(url_for('worker_cabinet')):
            return 'worker_cabinet'
>>>>>>> theirs
        if path.startswith(url_for('manage')):
            return 'manage'
        if path.startswith(url_for('post_job')) or path.startswith('/vacancies/create'):
            return 'post_job'
        if path.startswith(url_for('support')):
            return 'support'
        return ''

    return dict(
        current_user=current_user,
        default_avatar=default_avatar,
        active_page=get_active_page()
    )



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
<<<<<<< ours
            flash('', 'error')
        else:
            if User.query.filter_by(email=email).first():
                flash('', 'error')
=======
            flash('Please fill name, email and password.', 'error')
        else:
            if User.query.filter_by(email=email).first():
                flash('User with this email already exists.', 'error')
>>>>>>> theirs
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
<<<<<<< ours
                flash('', 'success')
=======
                flash('Registration successful. Welcome!', 'success')
>>>>>>> theirs
                return redirect(url_for('index'))

    return render_template('auth/register.html')

<<<<<<< ours

=======
>>>>>>> theirs
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
<<<<<<< ours
            flash('╨Т╤Л ╨▓╨╛╤И╨╗╨╕ ╨▓ ╨░╨║╨║╨░╤Г╨╜╤В', 'success')
            return redirect(url_for('index'))
        else:
            flash('╨Э╨╡╨▓╨╡╤А╨╜╨░╤П ╨┐╨╛╤З╤В╨░ ╨╕╨╗╨╕ ╨┐╨░╤А╨╛╨╗╤М', 'error')

    return render_template('auth/login.html')


=======
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect email or password.', 'error')

    return render_template('auth/login.html')

>>>>>>> theirs
@app.route('/logout')
@login_required
def logout():
    logout_user()
<<<<<<< ours
    flash('╨Т╤Л ╨▓╤Л╤И╨╗╨╕ ╨╕╨╖ ╨░╨║╨║╨░╤Г╨╜╤В╨░', 'success')
    return redirect(url_for('index'))


@app.route('/vacancies')
def vacancies():
    search = request.args.get('search', '').strip()
=======
    flash('Logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/vacancies')
def vacancies():
    search = request.args.get('search', '').strip()
    city = request.args.get('city', '').strip()
    pay_type = request.args.get('pay_type', '').strip()
    specialization = request.args.get('specialization', '').strip()

>>>>>>> theirs
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
<<<<<<< ours
    jobs = query.order_by(Job.created_at.desc()).all()
    return render_template('vacancies/list.html', jobs=jobs)
=======
    if city:
        query = query.filter(Job.city.ilike(f"%{city}%"))
    if specialization:
        query = query.filter(Job.specialization.ilike(f"%{specialization}%"))
    if pay_type in ('shift', 'hourly'):
        query = query.filter_by(pay_type=pay_type)
    jobs = query.order_by(Job.created_at.desc()).all()
    return render_template('vacancies/list.html', jobs=jobs, search=search, city=city, pay_type=pay_type, specialization=specialization)
>>>>>>> theirs


@app.route('/vacancies/<int:job_id>')
def vacancy_detail(job_id):
    job = Job.query.get_or_404(job_id)
    if job.status != 'approved':
<<<<<<< ours
        # ╨┐╨╛╨║╨░╨╖╤Л╨▓╨░╨╡╨╝ ╨╜╨╡╨╛╨┐╤Г╨▒╨╗╨╕╨║╨╛╨▓╨░╨╜╨╜╤Г╤О ╤В╨╛╨╗╤М╨║╨╛ ╨╡╤С ╨▓╨╗╨░╨┤╨╡╨╗╤М╤Ж╤Г-╤А╨░╨▒╨╛╤В╨╛╨┤╨░╤В╨╡╨╗╤О
        if not (current_user.is_authenticated and
                current_user.role == 'employer' and
                job.employer_id == current_user.id):
            flash('╨Т╨░╨║╨░╨╜╤Б╨╕╤П ╨╡╤Й╤С ╨╜╨╡ ╨╛╨┐╤Г╨▒╨╗╨╕╨║╨╛╨▓╨░╨╜╨░', 'error')
            return redirect(url_for('vacancies'))
=======
        # ?????????? ???????????????? ?????? ?? ?????????-????????????
        if not (current_user.is_authenticated and
                current_user.role == 'employer' and
                job.employer_id == current_user.id):
            flash('Something went wrong.', 'error')
            return redirect(url_for('vacancies'))
    # ??????? ????????: ???? ??? ? ???? ?? ????????
    today = datetime.date.today().isoformat()
    viewed = session.get('viewed_jobs', {})
    last_view = viewed.get(str(job.id))
    if last_view != today:
        job.view_count = (job.view_count or 0) + 1
        viewed[str(job.id)] = today
        session['viewed_jobs'] = viewed
        db.session.commit()
>>>>>>> theirs
    return render_template('vacancies/detail.html', job=job)


@app.route('/vacancies/<int:job_id>/apply', methods=['POST'])
@login_required
def apply(job_id):
    if current_user.role != 'worker':
<<<<<<< ours
        flash('╨в╨╛╨╗╤М╨║╨╛ ╤Б╨╛╨╕╤Б╨║╨░╤В╨╡╨╗╨╕ ╨╝╨╛╨│╤Г╤В ╨╛╤В╨║╨╗╨╕╨║╨░╤В╤М╤Б╤П ╨╜╨░ ╨▓╨░╨║╨░╨╜╤Б╨╕╨╕', 'error')
=======
        flash('Only workers can apply.', 'error')
>>>>>>> theirs
        return redirect(url_for('vacancy_detail', job_id=job_id))

    job = Job.query.get_or_404(job_id)

<<<<<<< ours
    # ╨┐╤А╨╛╨▓╨╡╤А╨║╨░: ╨┐╤А╨╛╤Д╨╕╨╗╤М ╨┤╨╛╨╗╨╢╨╡╨╜ ╨▒╤Л╤В╤М ╨╖╨░╨┐╨╛╨╗╨╜╨╡╨╜ (╤Е╨╛╤В╤П ╨▒╤Л ╤В╨╡╨╗╨╡╤Д╨╛╨╜)
    if not current_user.phone or str(current_user.phone).strip() == "":
        flash('╨Ч╨░╨┐╨╛╨╗╨╜╨╕╤В╨╡ ╨┐╤А╨╛╤Д╨╕╨╗╤М (╤Г╨║╨░╨╢╨╕╤В╨╡ ╤В╨╡╨╗╨╡╤Д╨╛╨╜), ╨┐╤А╨╡╨╢╨┤╨╡ ╤З╨╡╨╝ ╨╛╤В╨║╨╗╨╕╨║╨░╤В╤М╤Б╤П', 'error')
        return redirect(url_for('profile'))

    # ╨┐╤А╨╛╨▓╨╡╤А╨║╨░ ╨╜╨░ ╨┐╨╛╨▓╤В╨╛╤А╨╜╤Л╨╣ ╨╛╤В╨║╨╗╨╕╨║
    if Application.query.filter_by(job_id=job.id, worker_id=current_user.id).first():
        flash('╨Т╤Л ╤Г╨╢╨╡ ╨╛╤В╨║╨╗╨╕╨║╨░╨╗╨╕╤Б╤М ╨╜╨░ ╤Н╤В╤Г ╨▓╨░╨║╨░╨╜╤Б╨╕╤О', 'error')
=======
    if not current_user.phone or str(current_user.phone).strip() == "":
        flash('Add a phone number in your profile before applying.', 'error')
        return redirect(url_for('profile'))

    if Application.query.filter_by(job_id=job.id, worker_id=current_user.id).first():
        flash('You already applied to this vacancy.', 'error')
>>>>>>> theirs
        return redirect(url_for('vacancy_detail', job_id=job_id))

    note = request.form.get('note', '').strip()
    app_obj = Application(job_id=job.id, worker_id=current_user.id, note=note)
    db.session.add(app_obj)
    db.session.commit()
<<<<<<< ours
    flash('╨Ю╤В╨║╨╗╨╕╨║ ╨╛╤В╨┐╤А╨░╨▓╨╗╨╡╨╜', 'success')
    return redirect(url_for('vacancy_detail', job_id=job_id))


=======
    flash('Application sent.', 'success')
    return redirect(url_for('vacancy_detail', job_id=job_id))

>>>>>>> theirs
@app.route('/vacancies/create', methods=['GET', 'POST'])
@login_required
def create_vacancy():
    if current_user.role != 'employer':
<<<<<<< ours
        flash('╨в╨╛╨╗╤М╨║╨╛ ╨║╨╛╨╝╨┐╨░╨╜╨╕╤П ╨╝╨╛╨╢╨╡╤В ╤А╨░╨╖╨╝╨╡╤Й╨░╤В╤М ╨▓╨░╨║╨░╨╜╤Б╨╕╨╕', 'error')
=======
        flash('Something went wrong.', 'error')
>>>>>>> theirs
        return redirect(url_for('vacancies'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
<<<<<<< ours
            flash('╨Э╨░╨╖╨▓╨░╨╜╨╕╨╡ ╨╛╨▒╤П╨╖╨░╤В╨╡╨╗╤М╨╜╨╛', 'error')
        else:
=======
            flash('Something went wrong.', 'error')
        else:
            submit_action = request.form.get('submit_action', 'publish')
            new_status = 'draft' if submit_action == 'draft' else 'pending'
>>>>>>> theirs
            job = Job(
                employer_id=current_user.id,
                title=title,
                description=request.form.get('description') or '',
                city=request.form.get('city') or '',
                specialization=request.form.get('specialization') or '',
                wage=float(request.form.get('wage') or 0),
                pay_type=request.form.get('pay_type') or 'shift',
                duration_days=int(request.form.get('duration_days') or 1),
<<<<<<< ours
                status='pending'  # ╤Б╨╜╨░╤З╨░╨╗╨░ ╨╜╨░ ╨╝╨╛╨┤╨╡╤А╨░╤Ж╨╕╤О
            )
            db.session.add(job)
            db.session.commit()
            flash('╨Т╨░╨║╨░╨╜╤Б╨╕╤П ╨╛╤В╨┐╤А╨░╨▓╨╗╨╡╨╜╨░ ╨╜╨░ ╨╝╨╛╨┤╨╡╤А╨░╤Ж╨╕╤О', 'success')
            return redirect(url_for('vacancies'))

    return render_template('vacancies/create.html')

@app.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    # ╨╕╤Б╨┐╨╛╨╗╤М╨╖╤Г╨╡╨╝ ╤В╤Г ╨╢╨╡ ╨╗╨╛╨│╨╕╨║╤Г, ╤З╤В╨╛ ╨╕ ╨▓ create_vacancy
=======
                experience_level=request.form.get('experience_level') or None,
                employment_type=request.form.get('employment_type') or None,
                tariff=request.form.get('tariff') or None,
                status=new_status
            )
            db.session.add(job)
            db.session.commit()
            if new_status == 'draft':
                flash('Success.', 'success')
                return redirect(url_for('manage', tab='draft'))
            flash('Success.', 'success')
            return redirect(url_for('manage'))

    return render_template('vacancies/create.html')


@app.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    # Р В РЎвЂР РЋР С“Р В РЎвЂ”Р В РЎвЂўР В Р’В»Р РЋР Р‰Р В Р’В·Р РЋРЎвЂњР В Р’ВµР В РЎ Р РЋРІР‚С™Р РЋРЎвЂњ Р В Р’В¶Р В Р’Вµ Р В Р’В»Р В РЎвЂўР В РЎвЂ“Р В РЎвЂР В РЎвЂќР РЋРЎвЂњ, Р РЋРІР‚РЋР РЋРІР‚С™Р В РЎвЂў Р В РЎвЂ Р В Р вЂ  create_vacancy
>>>>>>> theirs
    return create_vacancy()
    

    
@app.route('/support')
@login_required
def support():
<<<<<<< ours
    # ╨┤╨╛╤Б╤В╤Г╨┐ ╤В╨╛╨╗╤М╨║╨╛ ╨╝╨╛╨┤╨╡╤А╨░╤В╨╛╤А╤Г
    if current_user.role != 'moderator':
        flash('╨б╤В╤А╨░╨╜╨╕╤Ж╨░ ╨┤╨╛╤Б╤В╤Г╨┐╨╜╨░ ╤В╨╛╨╗╤М╨║╨╛ ╨╝╨╛╨┤╨╡╤А╨░╤В╨╛╤А╨░╨╝', 'error')
        return redirect(url_for('index'))

    # ╨┐╨╛╨║╨░ ╨╖╨░╨│╨╗╤Г╤И╨║╨░ тАФ ╨┐╤А╨╛╤Б╤В╨╛ ╤А╨╡╨╜╨┤╨╡╤А ╤Б╤В╤А╨░╨╜╨╕╤Ж╤Л ╨┐╨╛╨┤╨┤╨╡╤А╨╢╨║╨╕
    # ╨┐╨╛╨╖╨╢╨╡ ╤Б╤О╨┤╨░ ╨╝╨╛╨╢╨╜╨╛ ╨┤╨╛╨▒╨░╨▓╨╕╤В╤М ╤Б╨┐╨╕╤Б╨╛╨║ ╤Б╨┐╨╛╤А╨╛╨▓/╨┤╨╡╨┐╨╛╨╖╨╕╤В╨╛╨▓ ╨╕ ╤В.╨┐.
=======
    # Р В РўвЂР В РЎвЂўР РЋР С“Р РЋРІР‚С™Р РЋРЎвЂњР В РЎвЂ” Р РЋРІР‚С™Р В РЎвЂўР В Р’В»Р РЋР Р‰Р В РЎвЂќР В РЎвЂў Р В РЎР В РЎвЂўР В РўвЂР В Р’ВµР РЋР вЂљР В Р’В°Р РЋРІР‚С™Р В РЎвЂўР РЋР вЂљР РЋРЎвЂњ
    if current_user.role != 'moderator':
        flash('Something went wrong.', 'error')
        return redirect(url_for('index'))

    # Р В РЎвЂ”Р В РЎвЂўР В РЎвЂќР В Р’В° Р В Р’В·Р В Р’В°Р В РЎвЂ“Р В Р’В»Р РЋРЎвЂњР РЋРІвЂљВ¬Р В РЎвЂќР В Р’В° Р Р†Р вЂљРІР‚Сњ Р В РЎвЂ”Р РЋР вЂљР В РЎвЂўР РЋР С“Р РЋРІР‚С™Р В РЎвЂў Р РЋР вЂљР В Р’ВµР В Р вЂ¦Р В РўвЂР В Р’ВµР РЋР вЂљ Р РЋР С“Р РЋРІР‚С™Р РЋР вЂљР В Р’В°Р В Р вЂ¦Р В РЎвЂР РЋРІР‚В Р РЋРІР‚в„– Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В РўвЂР В Р’ВµР РЋР вЂљР В Р’В¶Р В РЎвЂќР В РЎвЂ
    # Р В РЎвЂ”Р В РЎвЂўР В Р’В·Р В Р’В¶Р В Р’Вµ Р РЋР С“Р РЋР вЂ№Р В РўвЂР В Р’В° Р В РЎР В РЎвЂўР В Р’В¶Р В Р вЂ¦Р В РЎвЂў Р В РўвЂР В РЎвЂўР В Р’В±Р В Р’В°Р В Р вЂ Р В РЎвЂР РЋРІР‚С™Р РЋР Р‰ Р РЋР С“Р В РЎвЂ”Р В РЎвЂР РЋР С“Р В РЎвЂўР В РЎвЂќ Р РЋР С“Р В РЎвЂ”Р В РЎвЂўР РЋР вЂљР В РЎвЂўР В Р вЂ /Р В РўвЂР В Р’ВµР В РЎвЂ”Р В РЎвЂўР В Р’В·Р В РЎвЂР РЋРІР‚С™Р В РЎвЂўР В Р вЂ  Р В РЎвЂ Р РЋРІР‚С™.Р В РЎвЂ”.
>>>>>>> theirs
    return render_template('support/index.html')
    
@app.route('/manage')
@login_required
def manage():
<<<<<<< ours
    if current_user.role not in ('employer', 'moderator'):
        flash('╨Э╨╡╨┤╨╛╤Б╤В╨░╤В╨╛╤З╨╜╨╛ ╨┐╤А╨░╨▓', 'error')
        return redirect(url_for('index'))

    if current_user.role == 'employer':
        jobs = Job.query.filter_by(employer_id=current_user.id) \
                        .order_by(Job.created_at.desc()).all()
    else:
        # ╨╝╨╛╨┤╨╡╤А╨░╤В╨╛╤А ╨▓╨╕╨┤╨╕╤В ╨▓╤Б╨╡ pending
        jobs = Job.query.filter_by(status='pending') \
                        .order_by(Job.created_at.desc()).all()

    # ╨Ф╨╛╨▒╨░╨▓╨╗╤П╨╡╨╝ top_apps (╤В╨╛╨┐-3) ╨┤╨╗╤П ╤А╨░╨▒╨╛╤В╨╛╨┤╨░╤В╨╡╨╗╤П
    for job in jobs:
        # ╤Б╨╛╤А╤В╨╕╤А╤Г╨╡╨╝ ╨╛╤В╨║╨╗╨╕╨║╨╕ ╨┐╨╛ ╤А╨╡╨╣╤В╨╕╨╜╨│╤Г ╤А╨░╨▒╨╛╤З╨╡╨│╨╛ (╨╡╤Б╨╗╨╕ ╨╜╨╡╤В ╤А╨╡╨╣╤В╨╕╨╜╨│╨░ тАФ 0)
        sorted_apps = sorted(job.applications, key=lambda a: (a.worker.rating or 0), reverse=True)
        job.top_apps = sorted_apps[:3]

    return render_template('manage.html', jobs=jobs)
=======
    search = request.args.get('search', '').strip()
    active_tab = request.args.get('tab', 'approved')
    if current_user.role not in ('employer', 'moderator'):
        flash('Something went wrong.', 'error')
        return redirect(url_for('index'))

    if current_user.role == 'employer':
        query = Job.query.filter_by(employer_id=current_user.id)
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
    else:
        # ?????????? ????? ?????? pending
        jobs = Job.query.filter_by(status='pending')                         .order_by(Job.created_at.desc()).all()

    # ??????? ???-??????? ?? ???????? ?????????? (?? 3)
    for job in jobs:
        sorted_apps = sorted(job.applications, key=lambda a: (a.worker.rating or 0), reverse=True)
        job.top_apps = sorted_apps[:3]

        job.responses_total = len(job.applications)
        job.responses_in_work = len([a for a in job.applications if a.status == 'accepted'])
        job.responses_new = len([a for a in job.applications if a.status == 'applied'])
        job.view_count = getattr(job, 'view_count', 0) or 0
        if job.duration_days:
            job.expires_at = (job.created_at or datetime.datetime.utcnow()) + datetime.timedelta(days=job.duration_days)
        else:
            job.expires_at = None

    status_tabs = [
        dict(key='approved', label='Активные'),
        dict(key='draft', label='Черновики'),
        dict(key='pending', label='На модерации'),
        dict(key='rejected', label='Архивированные'),
    ]
    status_groups = {tab['key']: [] for tab in status_tabs}

    if current_user.role == 'employer':
        for job in jobs:
            status_key = job.status if job.status in status_groups else 'pending'
            status_groups.setdefault(status_key, []).append(job)

        for tab in status_tabs:
            tab['count'] = len(status_groups.get(tab['key'], []))

        if active_tab not in status_groups:
            active_tab = 'approved'
        elif not status_groups.get(active_tab):
            for tab in status_tabs:
                if status_groups.get(tab['key']):
                    active_tab = tab['key']
                    break

    return render_template(
        'manage.html',
        jobs=jobs,
        status_groups=status_groups if current_user.role == 'employer' else None,
        status_tabs=status_tabs if current_user.role == 'employer' else None,
        active_tab=active_tab if current_user.role == 'employer' else None,
        search=search if current_user.role == 'employer' else None,
    )
>>>>>>> theirs


@app.route('/manage/job/<int:job_id>/status/<string:action>', methods=['POST'])
@login_required
def change_job_status(job_id, action):
    job = Job.query.get_or_404(job_id)

    if current_user.role == 'employer':
        if job.employer_id != current_user.id:
<<<<<<< ours
            flash('╨Т╤Л ╨╜╨╡ ╨╝╨╛╨╢╨╡╤В╨╡ ╨╝╨╡╨╜╤П╤В╤М ╤Н╤В╤Г ╨▓╨░╨║╨░╨╜╤Б╨╕╤О', 'error')
            return redirect(url_for('manage'))
        if action == 'close':
            job.status = 'rejected'
        else:
            flash('╨Э╨╡╨▓╨╡╤А╨╜╨╛╨╡ ╨┤╨╡╨╣╤Б╤В╨▓╨╕╨╡', 'error')
=======
            flash('Something went wrong.', 'error')
            return redirect(url_for('manage'))
        if action == 'close':
            job.status = 'rejected'
        elif action == 'publish':
            job.status = 'pending'
        elif action == 'draft':
            job.status = 'draft'
        else:
            flash('Something went wrong.', 'error')
>>>>>>> theirs
            return redirect(url_for('manage'))

    elif current_user.role == 'moderator':
        if action == 'approve':
            job.status = 'approved'
        elif action == 'reject':
            job.status = 'rejected'
        else:
<<<<<<< ours
            flash('╨Э╨╡╨▓╨╡╤А╨╜╨╛╨╡ ╨┤╨╡╨╣╤Б╤В╨▓╨╕╨╡', 'error')
            return redirect(url_for('manage'))
    else:
        flash('╨Э╨╡╨┤╨╛╤Б╤В╨░╤В╨╛╤З╨╜╨╛ ╨┐╤А╨░╨▓', 'error')
        return redirect(url_for('index'))

    db.session.commit()
    flash('╨б╤В╨░╤В╤Г╤Б ╨▓╨░╨║╨░╨╜╤Б╨╕╨╕ ╨╛╨▒╨╜╨╛╨▓╨╗╤С╨╜', 'success')
=======
            flash('Something went wrong.', 'error')
            return redirect(url_for('manage'))
    else:
        flash('Something went wrong.', 'error')
        return redirect(url_for('index'))

    db.session.commit()
    flash('Success.', 'success')
>>>>>>> theirs
    return redirect(url_for('manage'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.phone = request.form.get('phone') or None
        current_user.education = request.form.get('education') or None
        current_user.exp_years = int(request.form.get('exp_years') or 0)

<<<<<<< ours
        # ╤Б╤В╤А╨░╤Е╨╛╨▓╨╛╨╣ ╨▓╨╖╨╜╨╛╤Б ╤В╨╛╨╗╤М╨║╨╛ ╨┤╨╗╤П ╤Б╨╛╨╕╤Б╨║╨░╤В╨╡╨╗╤П
=======
        # Р РЋР С“Р РЋРІР‚С™Р РЋР вЂљР В Р’В°Р РЋРІР‚В¦Р В РЎвЂўР В Р вЂ Р В РЎвЂўР В РІвЂћвЂ“ Р В Р вЂ Р В Р’В·Р В Р вЂ¦Р В РЎвЂўР РЋР С“ Р РЋРІР‚С™Р В РЎвЂўР В Р’В»Р РЋР Р‰Р В РЎвЂќР В РЎвЂў Р В РўвЂР В Р’В»Р РЋР РЏ Р РЋР С“Р В РЎвЂўР В РЎвЂР РЋР С“Р В РЎвЂќР В Р’В°Р РЋРІР‚С™Р В Р’ВµР В Р’В»Р РЋР РЏ
>>>>>>> theirs
        if current_user.role == 'worker':
            dep_raw = request.form.get('deposit')
            try:
                current_user.deposit = float(dep_raw or 0)
            except (TypeError, ValueError):
                current_user.deposit = 0

        db.session.commit()
<<<<<<< ours
        flash('╨Я╤А╨╛╤Д╨╕╨╗╤М ╨╛╨▒╨╜╨╛╨▓╨╗╤С╨╜', 'success')
        return redirect(url_for('profile'))

    # --- ╨б╤В╨░╤В╨╕╤Б╤В╨╕╨║╨░ ╨┐╤А╨╛╤Д╨╕╨╗╤П ---
=======
        flash('Success.', 'success')
        return redirect(url_for('profile'))

    # --- Р В Р Р‹Р РЋРІР‚С™Р В Р’В°Р РЋРІР‚С™Р В РЎвЂР РЋР С“Р РЋРІР‚С™Р В РЎвЂР В РЎвЂќР В Р’В° Р В РЎвЂ”Р РЋР вЂљР В РЎвЂўР РЋРІР‚С›Р В РЎвЂР В Р’В»Р РЋР РЏ ---
>>>>>>> theirs
    rating = getattr(current_user, 'rating', 0) or 0

    if current_user.role == 'employer':
        jobs_count = Job.query.filter_by(employer_id=current_user.id).count()
        responses_count = (
            Application.query
            .join(Job, Application.job_id == Job.id)
            .filter(Job.employer_id == current_user.id)
            .count()
        )
    elif current_user.role == 'worker':
        jobs_count = 0
        responses_count = Application.query.filter_by(worker_id=current_user.id).count()
    else:
        jobs_count = Job.query.filter_by(employer_id=current_user.id).count()
        responses_count = Application.query.filter_by(worker_id=current_user.id).count()

    class Stats:
        def __init__(self, rating, jobs, responses):
            self.rating = rating
            self.jobs = jobs
            self.responses = responses

    profile_stats = Stats(rating, jobs_count, responses_count)

<<<<<<< ours
    return render_template('profile/index.html', profile_stats=profile_stats)
=======
    educations = []
    experiences = []
    key_skills = []
    other_skills = []
    months = []
    education_levels = []
    years = []
    review_targets = []
    received_reviews = []
    if current_user.role == 'worker':
        educations = WorkerEducation.query.filter_by(user_id=current_user.id)                                     .order_by(WorkerEducation.created_at.desc()).all()
        experiences = WorkerExperience.query.filter_by(user_id=current_user.id)                                     .order_by(WorkerExperience.created_at.desc()).all()
        skills = WorkerSkill.query.filter_by(user_id=current_user.id)                                     .order_by(WorkerSkill.created_at.desc()).all()
        key_skills = [s for s in skills if s.is_key]
        other_skills = [s for s in skills if not s.is_key]
        accepted_apps = Application.query.join(Job, Application.job_id == Job.id) \
            .filter(Application.worker_id == current_user.id,
                    Application.status == 'accepted').all()
        seen = set()
        for app_obj in accepted_apps:
            emp = app_obj.job.employer if app_obj.job else None
            if emp and emp.id not in seen:
                review_targets.append(emp)
                seen.add(emp.id)
        months = [
            ('1', 'Январь'),
            ('2', 'Февраль'),
            ('3', 'Март'),
            ('4', 'Апрель'),
            ('5', 'Май'),
            ('6', 'Июнь'),
            ('7', 'Июль'),
            ('8', 'Август'),
            ('9', 'Сентябрь'),
            ('10', 'Октябрь'),
            ('11', 'Ноябрь'),
            ('12', 'Декабрь'),
        ]
        education_levels = [
            'Среднее',
            'Среднее специальное',
            'Неоконченное высшее',
            'Высшее',
            'Бакалавр',
            'Магистр',
            'Кандидат наук',
            'Доктор наук',
        ]
        years = list(range(datetime.date.today().year, 1939, -1))
    elif current_user.role == 'employer':
        accepted_apps = Application.query.join(Job, Application.job_id == Job.id) \
            .filter(Job.employer_id == current_user.id,
                    Application.status == 'accepted').all()
        seen = set()
        for app_obj in accepted_apps:
            worker = app_obj.worker
            if worker and worker.id not in seen:
                review_targets.append(worker)
                seen.add(worker.id)

    received_reviews = Review.query.filter_by(target_id=current_user.id) \
        .order_by(Review.created_at.desc()).all()
    return render_template(
        'profile/index.html',
        profile_stats=profile_stats,
        educations=educations,
        experiences=experiences,
        key_skills=key_skills,
        other_skills=other_skills,
        months=months,
        education_levels=education_levels,
        years=years,
        review_targets=review_targets,
        received_reviews=received_reviews
    )
>>>>>>> theirs


@app.route('/my-applications')
@login_required
def my_applications():
    if current_user.role != 'worker':
<<<<<<< ours
        flash('╨б╤В╤А╨░╨╜╨╕╤Ж╨░ ╨┤╨╛╤Б╤В╤Г╨┐╨╜╨░ ╤В╨╛╨╗╤М╨║╨╛ ╤Б╨╛╨╕╤Б╨║╨░╤В╨╡╨╗╤П╨╝', 'error')
        return redirect(url_for('index'))

    apps = Application.query.filter_by(worker_id=current_user.id) \
                            .order_by(Application.created_at.desc()).all()
    return render_template('my_applications.html', applications=apps)

=======
        flash('Only workers can view their applications.', 'error')
        return redirect(url_for('index'))

    filter_key = request.args.get('filter', 'all')

    apps = Application.query.filter_by(worker_id=current_user.id) \
                            .order_by(Application.created_at.desc()).all()

    waiting_apps = [app for app in apps if app.status == 'applied']
    approval_apps = [app for app in apps if app.status == 'awaiting_approval']
    offer_apps = [app for app in apps if app.status == 'work_offer']
    in_work_apps = [app for app in apps if app.status == 'in_work']
    completed_apps = [app for app in apps if app.status == 'completed']
    rejected_apps = [app for app in apps if app.status == 'rejected']

    filter_options = [
        dict(key='all', label='Все', count=len(apps)),
        dict(key='waiting', label='Новые', count=len(waiting_apps)),
        dict(key='approval', label='На согласовании', count=len(approval_apps)),
        dict(key='offer', label='Предложение', count=len(offer_apps)),
        dict(key='in_work', label='В работе', count=len(in_work_apps)),
        dict(key='completed', label='Завершено', count=len(completed_apps)),
        dict(key='rejected', label='Отклонено', count=len(rejected_apps)),
    ]
    total_count = len(apps)
    invited_count = len(in_work_apps)

    filtered = apps
    if filter_key == 'waiting':
        filtered = waiting_apps
    elif filter_key == 'approval':
        filtered = approval_apps
    elif filter_key == 'offer':
        filtered = offer_apps
    elif filter_key == 'in_work':
        filtered = in_work_apps
    elif filter_key == 'completed':
        filtered = completed_apps
    elif filter_key == 'rejected':
        filtered = rejected_apps
    elif filter_key not in ('all',):
        filter_key = 'all'

    status_labels = {
        'applied': dict(label='В ожидании', css='waiting'),
        'awaiting_approval': dict(label='На согласовании', css='warning'),
        'work_offer': dict(label='Предложение работы', css='info'),
        'in_work': dict(label='В работе', css='success'),
        'completed': dict(label='Завершено', css='muted'),
        'rejected': dict(label='Отклонено', css='danger'),
    }


    chat_meta = {}
    filtered_ids = [a.id for a in filtered]
    if filtered_ids:
        msgs = ChatMessage.query.filter(ChatMessage.application_id.in_(filtered_ids)) \
            .order_by(ChatMessage.created_at.desc()).all()
        for msg in msgs:
            meta = chat_meta.setdefault(msg.application_id, {'count': 0, 'last': None})
            meta['count'] += 1
            if meta['last'] is None:
                meta['last'] = msg

    return render_template(
        'my_applications.html',
        applications=filtered,
        filter_options=filter_options,
        active_filter=filter_key,
        status_labels=status_labels,
        total_count=total_count,
        invited_count=invited_count,
        chat_meta=chat_meta
    )


@app.route('/worker/cabinet')
@login_required
def worker_cabinet():
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    apps = Application.query.filter_by(worker_id=current_user.id)                             .order_by(Application.created_at.desc()).all()

    educations = WorkerEducation.query.filter_by(user_id=current_user.id)                                 .order_by(WorkerEducation.created_at.desc()).all()
    experiences = WorkerExperience.query.filter_by(user_id=current_user.id)                                 .order_by(WorkerExperience.created_at.desc()).all()
    skills = WorkerSkill.query.filter_by(user_id=current_user.id)                                 .order_by(WorkerSkill.created_at.desc()).all()
    key_skills = [s for s in skills if s.is_key]
    other_skills = [s for s in skills if not s.is_key]

    resumes_count = 1  # showcase stub for now
    applied_count = len(apps)
    accepted_count = len([a for a in apps if a.status in ('in_work', 'work_offer')])
    last_app = apps[0] if apps else None

    completed_sections = 0
    sections_total = 5
    if current_user.first_name and current_user.last_name and current_user.phone:
        completed_sections += 1
    if current_user.city:
        completed_sections += 1
    if current_user.birth_date:
        completed_sections += 1
    if educations:
        completed_sections += 1
    if experiences or skills:
        completed_sections += 1
    progress = int((completed_sections / sections_total) * 100) if sections_total else 0

    missing_fields = []
    if not (current_user.first_name and current_user.last_name):
        missing_fields.append('ФИО')
    if not current_user.phone:
        missing_fields.append('Телефон')
    if not current_user.city:
        missing_fields.append('Город')
    if not current_user.birth_date:
        missing_fields.append('Дата рождения')
    if not educations:
        missing_fields.append('Образование')
    if not experiences:
        missing_fields.append('Опыт работы')
    if not skills:
        missing_fields.append('Навыки')

    months = [
        ('1', '�������?'),
        ('2', '������?��?'),
        ('3', '�?�?��?'),
        ('4', '����?�?'),
        ('5', '���?�?'),
        ('6', '���?'),
        ('7', '���?'),
        ('8', '���?��?'),
        ('9', '�?�?����'),
        ('10', '�������?'),
        ('11', '�?�?�?��?'),
        ('12', '�?�?�?�?��?'),
    ]

    education_levels = [
        '������?��',
        '������?�� ����?�?��?��?�?�?',
        '�?�?�������?��� ��������',
        '������?��',
        '���?�?���?',
        '�?�?�?��?',
        '�?�?�?�? ��?�?',
        '����?�? ��?�?',
    ]
    years = list(range(datetime.date.today().year, 1939, -1))

    return render_template(
        'worker_cabinet.html',
        resumes_count=resumes_count,
        applied_count=applied_count,
        accepted_count=accepted_count,
        last_app=last_app,
        apps=apps[:3],
        educations=educations,
        experiences=experiences,
        key_skills=key_skills,
        other_skills=other_skills,
        months=months,
        education_levels=education_levels,
        missing_fields=missing_fields,
        years=years,
        progress=progress
    )


@app.route('/worker/cabinet/profile', methods=['POST'])
@login_required
def update_worker_profile():
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    current_user.last_name = (request.form.get('last_name') or '').strip() or None
    current_user.first_name = (request.form.get('first_name') or '').strip() or None
    current_user.middle_name = (request.form.get('middle_name') or '').strip() or None
    current_user.gender = (request.form.get('gender') or '').strip() or None
    current_user.city = (request.form.get('city') or '').strip() or None
    phone = (request.form.get('phone') or '').strip()
    current_user.phone = phone or None
    try:
        current_user.exp_years = int(request.form.get('exp_years') or 0)
    except (TypeError, ValueError):
        current_user.exp_years = 0

    day = request.form.get('birth_day')
    month = request.form.get('birth_month')
    year = request.form.get('birth_year')
    try:
        if day and month and year:
            current_user.birth_date = datetime.date(int(year), int(month), int(day))
        else:
            current_user.birth_date = None
    except (TypeError, ValueError):
        current_user.birth_date = None

    fio_parts = [current_user.last_name, current_user.first_name, current_user.middle_name]
    new_name = " ".join([p for p in fio_parts if p]).strip()
    if new_name:
        current_user.name = new_name

    db.session.commit()
    flash('Профиль обновлен.', 'success')
    return redirect_back('profile')


@app.route('/worker/cabinet/education', methods=['POST'])
@login_required
def save_worker_education():
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    edu_id = request.form.get('education_id')
    if edu_id:
        education = WorkerEducation.query.filter_by(id=edu_id, user_id=current_user.id).first()
        if not education:
            flash('Education record not found.', 'error')
            return redirect(url_for('worker_cabinet'))
    else:
        education = WorkerEducation(user_id=current_user.id)

    education.level = (request.form.get('level') or '').strip() or None
    education.institution = (request.form.get('institution') or '').strip() or None
    education.faculty = (request.form.get('faculty') or '').strip() or None
    education.specialization = (request.form.get('specialization') or '').strip() or None
    year_raw = (request.form.get('graduation_year') or '').strip()
    try:
        education.graduation_year = int(year_raw) if year_raw else None
    except ValueError:
        education.graduation_year = None

    db.session.add(education)
    db.session.commit()
    flash('Education saved.', 'success')
    return redirect_back('worker_cabinet')


@app.route('/worker/cabinet/education/<int:education_id>/delete', methods=['POST'])
@login_required
def delete_worker_education(education_id):
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    education = WorkerEducation.query.filter_by(id=education_id, user_id=current_user.id).first()
    if not education:
        flash('Education not found.', 'error')
        return redirect(url_for('worker_cabinet'))

    db.session.delete(education)
    db.session.commit()
    flash('Education entry removed.', 'success')
    return redirect_back('worker_cabinet')


@app.route('/worker/cabinet/experience', methods=['POST'])
@login_required
def save_worker_experience():
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    exp_id = request.form.get('experience_id')
    if exp_id:
        experience = WorkerExperience.query.filter_by(id=exp_id, user_id=current_user.id).first()
        if not experience:
            flash('Experience record not found.', 'error')
            return redirect(url_for('worker_cabinet'))
    else:
        experience = WorkerExperience(user_id=current_user.id)

    experience.company = (request.form.get('company') or '').strip() or None
    experience.title = (request.form.get('title') or '').strip() or None
    experience.duties = (request.form.get('duties') or '').strip() or None
    experience.start_month = (request.form.get('start_month') or '').strip() or None
    try:
        experience.start_year = int(request.form.get('start_year')) if request.form.get('start_year') else None
    except ValueError:
        experience.start_year = None

    experience.is_current = bool(request.form.get('is_current'))
    if experience.is_current:
        experience.end_month = None
        experience.end_year = None
    else:
        experience.end_month = (request.form.get('end_month') or '').strip() or None
        try:
            experience.end_year = int(request.form.get('end_year')) if request.form.get('end_year') else None
        except ValueError:
            experience.end_year = None

    db.session.add(experience)
    db.session.commit()
    flash('Experience saved.', 'success')
    return redirect_back('worker_cabinet')


@app.route('/worker/cabinet/experience/<int:experience_id>/delete', methods=['POST'])
@login_required
def delete_worker_experience(experience_id):
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    experience = WorkerExperience.query.filter_by(id=experience_id, user_id=current_user.id).first()
    if not experience:
        flash('Experience not found.', 'error')
        return redirect(url_for('worker_cabinet'))

    db.session.delete(experience)
    db.session.commit()
    flash('Experience entry removed.', 'success')
    return redirect_back('worker_cabinet')


@app.route('/worker/cabinet/skill', methods=['POST'])
@login_required
def add_worker_skill():
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    name = (request.form.get('skill_name') or '').strip()
    if not name:
        flash('Введите название навыка.', 'error')
        return redirect(url_for('worker_cabinet'))

    skill = WorkerSkill(
        user_id=current_user.id,
        name=name,
        is_key=bool(request.form.get('is_key'))
    )
    db.session.add(skill)
    db.session.commit()
    flash('Skill saved.', 'success')
    return redirect_back('worker_cabinet')


@app.route('/worker/cabinet/skill/<int:skill_id>/toggle', methods=['POST'])
@login_required
def toggle_worker_skill(skill_id):
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    skill = WorkerSkill.query.filter_by(id=skill_id, user_id=current_user.id).first()
    if not skill:
        flash('Skill not found.', 'error')
        return redirect(url_for('worker_cabinet'))

    skill.is_key = not bool(skill.is_key)
    db.session.commit()
    flash('Skill updated.', 'success')
    return redirect_back('worker_cabinet')


@app.route('/worker/cabinet/skill/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_worker_skill(skill_id):
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    skill = WorkerSkill.query.filter_by(id=skill_id, user_id=current_user.id).first()
    if not skill:
        flash('Skill not found.', 'error')
        return redirect(url_for('worker_cabinet'))

    db.session.delete(skill)
    db.session.commit()
    flash('Skill removed.', 'success')
    return redirect_back('worker_cabinet')


@app.route('/reviews', methods=['POST'])
@login_required
def leave_review():
    try:
        target_id = int(request.form.get('target_id') or 0)
    except ValueError:
        target_id = 0
    rating_raw = request.form.get('rating') or ''
    text = (request.form.get('text') or '').strip()
    try:
        rating = int(rating_raw)
    except ValueError:
        rating = 0

    target_user = User.query.get(target_id)
    if not target_user or target_user.id == current_user.id:
        flash('Некорректный получатель отзыва.', 'error')
        return redirect_back('profile')

    if rating < 1 or rating > 5:
        flash('Оценка должна быть от 1 до 5.', 'error')
        return redirect_back('profile')

    allowed = False
    if current_user.role == 'worker':
        allowed = Application.query.join(Job, Application.job_id == Job.id) \
            .filter(Application.worker_id == current_user.id,
                    Job.employer_id == target_user.id,
                    Application.status == 'accepted').first()
    elif current_user.role == 'employer':
        allowed = Application.query.join(Job, Application.job_id == Job.id) \
            .filter(Job.employer_id == current_user.id,
                    Application.worker_id == target_user.id,
                    Application.status == 'accepted').first()

    if not allowed:
        flash('Отзыв можно оставить только после завершенной сделки.', 'error')
        return redirect_back('profile')

    review = Review(
        reviewer_id=current_user.id,
        target_id=target_user.id,
        rating=rating,
        text=text
    )
    db.session.add(review)
    db.session.commit()
    flash('Отзыв отправлен.', 'success')
    return redirect_back('profile')


@app.route('/worker/deposit', methods=['POST'])
@login_required
def worker_deposit():
    if current_user.role != 'worker':
        flash('Worker cabinet is available only for workers.', 'error')
        return redirect(url_for('index'))

    amount_raw = request.form.get('deposit_amount', '').strip()
    try:
        amount = float(amount_raw) if amount_raw else 0
    except ValueError:
        amount = 0

    if amount <= 0:
        flash('Please enter a positive amount.', 'error')
        return redirect(url_for('worker_cabinet'))

    current_user.deposit = (current_user.deposit or 0) + amount
    db.session.commit()
    flash('Deposit topped up successfully.', 'success')
    return redirect(url_for('worker_cabinet'))
>>>>>>> theirs

@app.route('/job/<int:job_id>/applications')
@login_required
def view_job_applications(job_id):
    if not current_user.is_authenticated or current_user.role != 'employer':
<<<<<<< ours
        flash('╨Ф╨╛╤Б╤В╤Г╨┐ ╤В╨╛╨╗╤М╨║╨╛ ╨┤╨╗╤П ╤А╨░╨▒╨╛╤В╨╛╨┤╨░╤В╨╡╨╗╨╡╨╣', 'error')
=======
        flash('Only employers can view responses.', 'error')
>>>>>>> theirs
        return redirect(url_for('index'))

    job = Job.query.filter_by(id=job_id, employer_id=current_user.id).first()

    if not job:
<<<<<<< ours
        flash('╨Т╨░╨║╨░╨╜╤Б╨╕╤П ╨╜╨╡ ╨╜╨░╨╣╨┤╨╡╨╜╨░', 'error')
        return redirect(url_for('manage'))

    apps = Application.query.filter_by(job_id=job.id) \
                            .order_by(Application.created_at.desc()).all()

    return render_template('applications_for_job.html', job=job, apps=apps)



def init_db():
    db.create_all()
    # ╤Б╨╛╨╖╨┤╨░╤С╨╝ ╨╝╨╛╨┤╨╡╤А╨░╤В╨╛╤А╨░ ╨┐╨╛ ╤Г╨╝╨╛╨╗╤З╨░╨╜╨╕╤О
    if not User.query.filter_by(email='admin@tj.local').first():
        admin = User(
            name='╨Ь╨╛╨┤╨╡╤А╨░╤В╨╛╤А',
=======
        flash('Vacancy not found or does not belong to you.', 'error')
        return redirect(url_for('manage'))

    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', 'all')

    base_query = Application.query.filter_by(job_id=job.id)
    apps_for_stats = base_query.order_by(Application.created_at.desc()).all()

    apps_query = Application.query.filter_by(job_id=job.id)
    if search:
        like = f"%{search}%"
        apps_query = apps_query.join(User, Application.worker_id == User.id)                                .filter(
                                   db.or_(
                                       User.name.ilike(like),
                                       User.email.ilike(like),
                                       User.phone.ilike(like),
                                       Application.note.ilike(like)
                                   )
                               )
    allowed_filters = ('applied', 'awaiting_approval', 'work_offer', 'in_work', 'completed', 'rejected')
    if status_filter in allowed_filters:
        apps_query = apps_query.filter(Application.status == status_filter)
    else:
        status_filter = 'all'

    apps = apps_query.order_by(Application.created_at.desc()).all()

    now = datetime.datetime.utcnow()
    for app_obj in apps:
        created_at = app_obj.created_at or now
        app_obj.waiting_days = max((now - created_at).days, 0)

    status_metrics = dict(
        total=len(apps_for_stats),
        applied=len([a for a in apps_for_stats if a.status == 'applied']),
        approval=len([a for a in apps_for_stats if a.status == 'awaiting_approval']),
        offers=len([a for a in apps_for_stats if a.status == 'work_offer']),
        in_work=len([a for a in apps_for_stats if a.status == 'in_work']),
        completed=len([a for a in apps_for_stats if a.status == 'completed']),
        rejected=len([a for a in apps_for_stats if a.status == 'rejected']),
    )

    chat_meta = {}
    app_ids = [a.id for a in apps]
    if app_ids:
        msgs = ChatMessage.query.filter(ChatMessage.application_id.in_(app_ids)) \
            .order_by(ChatMessage.created_at.desc()).all()
        for msg in msgs:
            meta = chat_meta.setdefault(msg.application_id, {'count': 0, 'last': None})
            meta['count'] += 1
            if meta['last'] is None:
                meta['last'] = msg

    return render_template(
        'applications_for_job.html',
        job=job,
        apps=apps,
        search=search,
        status_filter=status_filter,
        status_metrics=status_metrics,
        chat_meta=chat_meta
    )


@app.route('/applications/<int:app_id>/status', methods=['POST'])
@login_required
def update_application_status(app_id):
    app_obj = Application.query.get_or_404(app_id)
    job = app_obj.job
    is_employer = current_user.role == 'employer' and job and job.employer_id == current_user.id
    is_worker = current_user.role == 'worker' and app_obj.worker_id == current_user.id
    if not (is_employer or is_worker):
        flash('Not allowed.', 'error')
        return redirect(url_for('index'))

    action = (request.form.get('action') or '').strip().lower()
    next_url = request.form.get('next') or (
        url_for('view_job_applications', job_id=job.id) if job else url_for('index')
    )
    if not next_url.startswith('/'):
        next_url = url_for('index')

    if action == 'send_to_approval' and is_employer:
        if app_obj.status != 'applied':
            flash('Этот отклик уже отправлен на согласование или обработан.', 'error')
            return redirect(next_url)
        app_obj.status = 'awaiting_approval'
        add_chat_message(app_obj, 'Система: работодатель отправил отклик на согласование.', is_system=True, sender=current_user)
        db.session.commit()
        flash('Отправлено на согласование.', 'success')
        return redirect(next_url)

    if action == 'start_work' and is_employer:
        try:
            units = int(request.form.get('units') or 0)
        except ValueError:
            units = 0
        if units <= 0:
            flash('Укажите количество смен или часов.', 'error')
            return redirect(next_url)
        wage = job.wage or 0
        amount = wage * units
        if amount <= 0:
            flash('Не задана ставка для вакансии.', 'error')
            return redirect(next_url)
        employer_balance = job.employer.deposit or 0
        if employer_balance < amount:
            flash('Недостаточно средств у работодателя.', 'error')
            return redirect(next_url)
        job.employer.deposit = employer_balance - amount
        app_obj.frozen_amount = amount
        app_obj.work_units = units
        app_obj.status = 'work_offer'
        add_chat_message(
            app_obj,
            f"Система: предложено {units} ед. работы на сумму {amount:.2f}.",
            is_system=True,
            sender=current_user
        )
        db.session.commit()
        flash('Предложение отправлено и сумма заморожена.', 'success')
        return redirect(next_url)

    if action == 'worker_accept' and is_worker:
        if app_obj.status != 'work_offer':
            flash('Нельзя принять это предложение.', 'error')
            return redirect(next_url)
        app_obj.status = 'in_work'
        add_chat_message(app_obj, 'Система: кандидат принял предложение и приступает к работе.', is_system=True, sender=current_user)
        db.session.commit()
        flash('Вы приняли предложение.', 'success')
        return redirect(next_url)

    if action == 'worker_decline' and is_worker:
        if app_obj.status != 'work_offer':
            flash('Нельзя отклонить это предложение.', 'error')
            return redirect(next_url)
        employer = job.employer if job else None
        if employer:
            employer.deposit = (employer.deposit or 0) + (app_obj.frozen_amount or 0)
        add_chat_message(app_obj, 'Система: кандидат отклонил предложение. Средства возвращены работодателю.', is_system=True, sender=current_user)
        app_obj.status = 'rejected'
        app_obj.frozen_amount = 0
        db.session.commit()
        flash('Предложение отклонено.', 'success')
        return redirect(next_url)

    if action == 'complete_work' and is_employer:
        if app_obj.status != 'in_work':
            flash('Работа ещё не в процессе.', 'error')
            return redirect(next_url)
        payout = app_obj.frozen_amount or 0
        worker = app_obj.worker
        if worker:
            worker.deposit = (worker.deposit or 0) + payout
        app_obj.frozen_amount = 0
        app_obj.status = 'completed'
        add_chat_message(app_obj, f'Система: работа завершена, выплата {payout:.2f} переведена кандидату.', is_system=True, sender=current_user)
        db.session.commit()
        flash('Работа подтверждена и оплачена.', 'success')
        return redirect(next_url)

    if action == 'reject' and is_employer:
        if app_obj.frozen_amount:
            job.employer.deposit = (job.employer.deposit or 0) + app_obj.frozen_amount
            app_obj.frozen_amount = 0
        app_obj.status = 'rejected'
        add_chat_message(app_obj, 'Система: отклик отклонён.', is_system=True, sender=current_user)
        db.session.commit()
        flash('Отклик отклонён.', 'success')
        return redirect(next_url)

    flash('Неизвестное действие или нет прав.', 'error')
    return redirect(next_url)



@app.route('/applications/<int:app_id>/withdraw', methods=['POST'])
@login_required
def withdraw_application(app_id):
    app_obj = Application.query.get_or_404(app_id)
    if current_user.role != 'worker' or app_obj.worker_id != current_user.id:
        flash('Not allowed.', 'error')
        return redirect(url_for('index'))

    job_id = app_obj.job_id
    db.session.delete(app_obj)
    db.session.commit()
    flash('Отклик отменен.', 'success')
    return redirect(url_for('my_applications'))


@app.route('/applications/<int:app_id>/chat', methods=['GET', 'POST'])
@login_required
def application_chat(app_id):
    app_obj = Application.query.get_or_404(app_id)
    job = app_obj.job
    is_worker = current_user.role == 'worker' and app_obj.worker_id == current_user.id
    is_employer = current_user.role == 'employer' and job and job.employer_id == current_user.id

    back_url = url_for('my_applications') if is_worker else (
        url_for('view_job_applications', job_id=job.id) if job else url_for('manage')
    )
    if not (is_worker or is_employer):
        flash('??? ??????? ? ????? ????.', 'error')
        return redirect(back_url)

    allowed_chat_statuses = {'awaiting_approval', 'work_offer', 'in_work', 'completed'}
    if app_obj.status not in allowed_chat_statuses:
        flash('??? ?????? ???????? ????? ???????? ?? ????????????.', 'error')
        return redirect(back_url)

    if request.method == 'POST':
        message_text = (request.form.get('message') or '').strip()
        if not message_text:
            flash('??????? ?????????.', 'error')
        else:
            add_chat_message(app_obj, message_text, is_system=False, sender=current_user)
            db.session.commit()
            flash('????????? ??????????.', 'success')
            return redirect(url_for('application_chat', app_id=app_obj.id) + '#last')

    messages = ChatMessage.query.filter_by(application_id=app_obj.id)         .order_by(ChatMessage.created_at.asc()).all()
    chat_partner = app_obj.job.employer if is_worker else app_obj.worker
    status_labels = {
        'applied': 'В ожидании',
        'awaiting_approval': 'На согласовании',
        'work_offer': 'Предложение',
        'in_work': 'В работе',
        'completed': 'Завершено',
        'rejected': 'Отклонено'
    }
    status_label = status_labels.get(app_obj.status, 'Без статуса')
    return render_template(
        'application_chat.html',
        app_obj=app_obj,
        job=job,
        chat_partner=chat_partner,
        messages=messages,
        back_url=back_url,
        is_worker=is_worker,
        is_employer=is_employer,
        status_label=status_label,
        worker=app_obj.worker,
        employer=job.employer if job else None
    )

def init_db():
    db.create_all()
    ensure_user_columns()
    ensure_job_columns()
    ensure_application_columns()
    ensure_chat_message_columns()
    ensure_review_table()
    # создаём модератора по умолчанию
    if not User.query.filter_by(email='admin@tj.local').first():
        admin = User(
            name='Администратор',
>>>>>>> theirs
            email='admin@tj.local',
            password_hash=generate_password_hash('admin'),
            role='moderator'
        )
        db.session.add(admin)
        db.session.commit()

<<<<<<< ours
=======
def ensure_user_columns():
    """Add new worker profile columns to existing DB without migrations."""
    insp = inspect(db.engine)
    cols = {c['name'] for c in insp.get_columns('user')}
    ddl = []
    if 'first_name' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN first_name VARCHAR(120)")
    if 'last_name' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN last_name VARCHAR(120)")
    if 'middle_name' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN middle_name VARCHAR(120)")
    if 'gender' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN gender VARCHAR(20)")
    if 'city' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN city VARCHAR(120)")
    if 'birth_date' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN birth_date DATE")
    if 'deposit' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN deposit REAL DEFAULT 0")
    if 'rating' not in cols:
        ddl.append("ALTER TABLE user ADD COLUMN rating REAL DEFAULT 0")

    with db.engine.begin() as conn:
        for stmt in ddl:
            try:
                conn.execute(text(stmt))
            except Exception:
                pass

def ensure_job_columns():
    """Добавляет недостающие колонки для тегов вакансий (без миграций)."""
    insp = inspect(db.engine)
    cols = {c['name'] for c in insp.get_columns('job')}
    ddl = []
    if 'view_count' not in cols:
        ddl.append("ALTER TABLE job ADD COLUMN view_count INTEGER DEFAULT 0")
    if 'experience_level' not in cols:
        ddl.append("ALTER TABLE job ADD COLUMN experience_level VARCHAR(50)")
    if 'employment_type' not in cols:
        ddl.append("ALTER TABLE job ADD COLUMN employment_type VARCHAR(50)")
    if 'tariff' not in cols:
        ddl.append("ALTER TABLE job ADD COLUMN tariff VARCHAR(50)")
    with db.engine.begin() as conn:
        for stmt in ddl:
            try:
                conn.execute(text(stmt))
            except Exception:
                pass



def ensure_application_columns():
    # Add new application workflow columns.
    insp = inspect(db.engine)
    cols = {c['name'] for c in insp.get_columns('application')}
    ddl = []
    if 'frozen_amount' not in cols:
        ddl.append("ALTER TABLE application ADD COLUMN frozen_amount REAL DEFAULT 0")
    if 'work_units' not in cols:
        ddl.append("ALTER TABLE application ADD COLUMN work_units INTEGER DEFAULT 0")

    with db.engine.begin() as conn:
        for stmt in ddl:
            try:
                conn.execute(text(stmt))
            except Exception:
                pass

def ensure_chat_message_columns():
    # Add system flag to chat messages.
    insp = inspect(db.engine)
    cols = {c['name'] for c in insp.get_columns('chat_message')}
    if 'is_system' not in cols:
        with db.engine.begin() as conn:
            try:
                conn.execute(text("ALTER TABLE chat_message ADD COLUMN is_system BOOLEAN DEFAULT 0"))
            except Exception:
                pass
_db_initialized = False

@app.before_request
def _ensure_db_initialized():
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True




def ensure_review_table():
    insp = inspect(db.engine)
    tables = set(insp.get_table_names())
    if 'review' not in tables:
        with db.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE review (
                    id INTEGER PRIMARY KEY,
                    reviewer_id INTEGER NOT NULL,
                    target_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    text TEXT,
                    created_at DATETIME
                )
            """))
>>>>>>> theirs
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

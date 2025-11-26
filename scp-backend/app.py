from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Camera, ObjectItem, Event
from forms import RegisterForm, LoginForm, CameraForm, ObjectForm, EventForm, AdminUserForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Camera type -> default security level mapping
    CAMERA_SECURITY_MAP = {
        'Containment': 5,
        'SecureVault': 5,
        'Keter': 5,
        'Euclid': 4,
        'Surveillance': 2,
        'Laboratory': 3,
        'Mobile': 1,
        'External': 1,
    }

    # Routes

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = RegisterForm()
        if form.validate_on_submit():
            # check existing
            if User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first():
                flash("Користувач з таким іменем або електронною адресою вже існує.", 'warning')
                return render_template('register.html', form=form)
            user = User(username=form.username.data, email=form.email.data, role='user')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Реєстрація успішна. Тепер ви можете увійти.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            # allow login by username or email
            credential = form.username.data
            user = User.query.filter((User.username == credential) | (User.email == credential)).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Успішний вхід.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            flash('Невірні дані для входу.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Ви вийшли з системи.', 'info')
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))

    # ADMIN ROUTES
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if current_user.role != 'admin':
            flash('Доступ заборонено.', 'danger')
            return redirect(url_for('user_dashboard'))
        cameras = Camera.query.all()
        objects = ObjectItem.query.all()
        events = Event.query.all()
        return render_template('dashboard_admin.html', cameras=cameras, objects=objects, events=events)

    # Camera Management
    @app.route('/admin/camera/add', methods=['GET', 'POST'])
    @login_required
    def add_camera():
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        form = CameraForm()
        if form.validate_on_submit():
            sec = CAMERA_SECURITY_MAP.get(form.type.data, form.security_level.data)
            camera = Camera(
                name=form.name.data,
                type=form.type.data,
                max_capacity=form.max_capacity.data,
                security_level=sec,
                equipment_list=form.equipment_list.data,
                cleaning_schedule=form.cleaning_schedule.data,
                maintenance_schedule=form.maintenance_schedule.data
            )
            db.session.add(camera)
            db.session.commit()
            flash('Підрозділ створено успішно!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_camera.html', form=form)

    @app.route('/admin/camera/edit/<int:camera_id>', methods=['GET', 'POST'])
    @login_required
    def edit_camera(camera_id):
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        camera = Camera.query.get_or_404(camera_id)
        form = CameraForm()
        if form.validate_on_submit():
            camera.name = form.name.data
            camera.type = form.type.data
            camera.max_capacity = form.max_capacity.data
            camera.security_level = CAMERA_SECURITY_MAP.get(form.type.data, form.security_level.data)
            camera.equipment_list = form.equipment_list.data
            camera.cleaning_schedule = form.cleaning_schedule.data
            camera.maintenance_schedule = form.maintenance_schedule.data
            db.session.commit()
            flash('Підрозділ оновлено!', 'success')
            return redirect(url_for('admin_dashboard'))
        elif request.method == 'GET':
            form.name.data = camera.name
            form.type.data = camera.type
            form.max_capacity.data = camera.max_capacity
            form.security_level.data = camera.security_level
            form.equipment_list.data = camera.equipment_list
            form.cleaning_schedule.data = camera.cleaning_schedule
            form.maintenance_schedule.data = camera.maintenance_schedule
        return render_template('edit_camera.html', form=form, camera=camera)

    @app.route('/admin/camera/delete/<int:camera_id>')
    @login_required
    def delete_camera(camera_id):
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        camera = Camera.query.get_or_404(camera_id)
        db.session.delete(camera)
        db.session.commit()
        flash('Підрозділ видалено!', 'success')
        return redirect(url_for('admin_dashboard'))

    # Object Management
    @app.route('/admin/object/add', methods=['GET', 'POST'])
    @login_required
    def add_object():
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        form = ObjectForm()
        cameras = Camera.query.all()
        form.camera_id.choices = [(0, '-- Виберіть підрозділ --')] + [(c.id, c.name) for c in cameras]
        if form.validate_on_submit():
            obj = ObjectItem(
                name=form.name.data,
                classification=form.classification.data,
                description=form.description.data,
                storage_requirements=form.storage_requirements.data,
                camera_id=form.camera_id.data if form.camera_id.data and form.camera_id.data != 0 else None
            )
            db.session.add(obj)
            db.session.commit()
            flash('Об\'єкт створено успішно!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_object.html', form=form)

    @app.route('/admin/object/edit/<int:object_id>', methods=['GET', 'POST'])
    @login_required
    def edit_object(object_id):
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        obj = ObjectItem.query.get_or_404(object_id)
        form = ObjectForm()
        cameras = Camera.query.all()
        form.camera_id.choices = [(0, '-- Select Camera --')] + [(c.id, c.name) for c in cameras]
        if form.validate_on_submit():
            obj.name = form.name.data
            obj.classification = form.classification.data
            obj.description = form.description.data
            obj.storage_requirements = form.storage_requirements.data
            obj.camera_id = form.camera_id.data if form.camera_id.data and form.camera_id.data != 0 else None
            db.session.commit()
            flash('Об\'єкт оновлено!', 'success')
            return redirect(url_for('admin_dashboard'))
        elif request.method == 'GET':
            form.name.data = obj.name
            form.classification.data = obj.classification
            form.description.data = obj.description
            form.storage_requirements.data = obj.storage_requirements
            form.camera_id.data = obj.camera_id if obj.camera_id else 0
        return render_template('edit_object.html', form=form, obj=obj)

    @app.route('/admin/object/delete/<int:object_id>')
    @login_required
    def delete_object(object_id):
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        obj = ObjectItem.query.get_or_404(object_id)
        db.session.delete(obj)
        db.session.commit()
        flash('Об\'єкт видалено!', 'success')
        return redirect(url_for('admin_dashboard'))

    # Event Logging
    @app.route('/admin/event/add', methods=['GET', 'POST'])
    @login_required
    def add_event():
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        form = EventForm()
        if form.validate_on_submit():
            event = Event(
                type=form.type.data,
                notes=form.notes.data,
                user_id=current_user.id
            )
            db.session.add(event)
            db.session.commit()
            flash('Подію зареєстровано!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_event.html', form=form)

    # USER ROUTES
    @app.route('/user/dashboard')
    @login_required
    def user_dashboard():
        cameras = Camera.query.all()
        objects = ObjectItem.query.all()
        events = Event.query.all()
        return render_template('dashboard_user.html', cameras=cameras, objects=objects, events=events)

    @app.route('/user/camera/<int:camera_id>')
    @login_required
    def view_camera(camera_id):
        camera = Camera.query.get_or_404(camera_id)
        objects = ObjectItem.query.filter_by(camera_id=camera_id).all()
        return render_template('view_camera.html', camera=camera, objects=objects)

    @app.route('/user/object/add', methods=['GET', 'POST'])
    @login_required
    def user_add_object():
        form = ObjectForm()
        cameras = Camera.query.all()
        form.camera_id.choices = [(0, '-- Виберіть підрозділ --')] + [(c.id, c.name) for c in cameras]
        if form.validate_on_submit():
            obj = ObjectItem(
                name=form.name.data,
                classification=form.classification.data,
                description=form.description.data,
                storage_requirements=form.storage_requirements.data,
                camera_id=form.camera_id.data if form.camera_id.data and form.camera_id.data != 0 else None
            )
            db.session.add(obj)
            db.session.commit()
            flash('Об\'єкт додано успішно!', 'success')
            return redirect(url_for('user_dashboard'))
        return render_template('user_add_object.html', form=form)

    # Admin creation helper (only when run directly) - optional
    @app.cli.command('create-admin')
    def create_admin():
        """Create an admin user: flask create-admin"""
        username = os.environ.get('ADMIN_USER', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASS', 'adminpass')
        if User.query.filter_by(username=username).first():
            print('Адміністратор вже існує.')
            return
        admin = User(username=username, email=email, role='admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print('Адміністратора створено.')

    # Admin: edit user (role + access_level)
    @app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def edit_user(user_id):
        if current_user.role != 'admin':
            flash('?????? ??????????.', 'danger')
            return redirect(url_for('user_dashboard'))
        user = User.query.get_or_404(user_id)
        form = AdminUserForm()
        if form.validate_on_submit():
            user.role = form.role.data
            try:
                user.access_level = int(form.access_level.data)
            except Exception:
                user.access_level = 0
            db.session.commit()
            flash('Користувача оновлено.', 'success')
            return redirect(url_for('admin_dashboard'))
        elif request.method == 'GET':
            form.role.data = user.role
            form.access_level.data = user.access_level
        return render_template('edit_user.html', form=form, user=user)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

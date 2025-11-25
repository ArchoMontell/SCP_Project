# SCP Project — Архітектура й розбір коду

## Змістовна таблиця
1. [Огляд проєкту](#огляд-проєкту)
2. [Предметна область (SCP Foundation)](#предметна-область-scp-foundation)
3. [Технічний стек](#технічний-стек)
4. [Архітектура додатку](#архітектура-додатку)
5. [Структура БД](#структура-бд)
6. [Ключові модулі й функції](#ключові-модулі--функції)
7. [Потік роботи (User Stories)](#потік-роботи-user-stories)
8. [Міграції БД (Alembic)](#міграції-бд-alembic)

---

## Огляд проєкту

**SCP Project** — це web-додаток для управління аномальними об'єктами за мотивами **SCP Foundation** (вигадана таємна організація).

**Основна мета:**
- Адміністратори можуть створювати й редагувати камери (контейнери) й об'єкти з класифікацією.
- Користувачі можуть переглядати камери й додавати об'єкти до контейнерів.
- Система розрізняє ролі (admin vs user) й рівні доступу (access_level 0–5).
- Усі операції логуються як события (events).

**Статус:**
- **v0.1**: MVP з базовим CRUD для камер й об'єктів, аутентифікація, ролі.
- **v0.2**: SelectField для вибору камер, українські мітки класів SCP, Alembic для версіювання БД, автоматичне встановлення security_level за типом камери.

---

## Предметна область (SCP Foundation)

### Класифікація об'єктів SCP

Кожному аномальному об'єкту присвоюється **клас** (classification) зі стандартизованою кольоровою позначкою:

| Клас | Колір | Опис | Приклад |
|------|-------|------|---------|
| **Unspecified** (Непозначений) | Сірий | Вплив невідомий або об'єкт нейтралізований | SCP-407 (пісня з ростом клітин) |
| **Safe** (Безпечний) | Зелений | Не становить загрози за дотримання правил | SCP-500 (пігулки від усіх недуг) |
| **Euclid** (Евклід) | Жовтий | Поведінку неможливо передбачити | SCP-173 (скульптура, убиває без спостереження) |
| **Keter** (Кетер) | Червоний | Активна ворожість, велика небезпека | SCP-682 (рептилія, що не гине й атакує) |
| **Thaumiel** (Тауміель) | Чорний | Секретні об'єкти проти інших аномалій | SCP-1968 (тор, переписує минуле) |
| **Exotic** (Екзотичний) | Синій | Нестандартні класи, рідко трапляються | SCP-001 (можливо Земля) |
| **Metaclass** (Метаклас) | Рожевий | Самі змінюють свій клас й документацію | SCP-4780 (невідомо, що це) |

### Рівні доступу

Персонал Фонду має рівні допуску (access_level), що визначають доступ до інформації:

| Рівень | Назва | Опис |
|--------|-------|------|
| **0** | Для загального користування | Персонал обслуговування |
| **1** | Для службового користування | Помічники, охорона, не з прямим доступом |
| **2** | Для обмеженого користування | Дослідники, спеціалісти утримання |
| **3** | Таємно | Старші науковці, керівники проектів |
| **4** | Цілком таємно | Керівники зон, командири операцій |
| **5** | Тауміель (найвищий) | Члени Ради O5, гарантує доступ до всього |

### Типи камер утримання

Проєкт використовує умовні типи камер (не офіційні SCP-канон):

- **Containment Unit** — спеціалізована комора з високим security_level (5)
- **Surveillance** — контроль через камери, low security_level (2)
- **Laboratory** — дослідницька установка, medium security_level (3)
- **Mobile Camera** — мобільна система, low security_level (1)
- **External/Perimeter** — зовнішня охорона, low security_level (1)
- **Secure Vault Camera** — максимум захисту, high security_level (5)

---

## Технічний стек

### Backend (Python 3.14)

| Технологія | Версія | Назначение |
|------------|--------|-----------|
| **Flask** | 2.3.3 | Мікрофреймворк для web-додатку |
| **Flask-Login** | — | Управління сесіями й аутентифікацією користувачів |
| **Flask-WTF** | — | CSRF захист і інтеграція WTForms |
| **WTForms** | — | Валідація й рендеринг форм на HTML |
| **Flask-SQLAlchemy** | 3.x | ORM (Object-Relational Mapping) для роботи з БД |
| **SQLAlchemy** | 2.x | Core + ORM для управління схемою й запитами |
| **Alembic** | 1.x+ | Версіювання й миграції схеми БД |
| **Werkzeug** | — | Утиліти для WSGI, хешування паролів |

### БД

- **SQLite** — локальна реляційна БД, простота розгортання, файл `scp.db` у проєкті.
- Альтернатива: PostgreSQL/MySQL для production.

### Frontend

- **HTML 5** + **Jinja2** шаблони (Flask built-in).
- **CSS 3** — базовий стиль у `base.html`.
- **JavaScript** — мінімально; можна розширити для валідації на клієнті.

### Контроль версій

- **Git** + **GitHub** (репозиторій `ArchoMontell/SCP_Project`).
- Теги версій: `v0.1`, `v0.2`.

---

## Архітектура додатку

### Структура папок

```
scp-backend/
├── app.py                          # Точка входу, app factory, маршрути (routes)
├── config.py                       # Конфіґурація (SECRET_KEY, DB URI, REMEMBER_COOKIE_DURATION)
├── models.py                       # SQLAlchemy моделі (User, Camera, ObjectItem, Event)
├── forms.py                        # WTForms для аутентифікації й CRUD
├── scp.db                          # SQLite база даних
├── requirements.txt                # Залежності (pip freeze)
├── view_db.py                      # Утиліта для перегляду вмісту БД
│
├── alembic/                        # Alembic для версіювання БД
│   ├── env.py                      # Конфіґурація середовища для Alembic
│   ├── script.py.mako              # Шаблон для генерування нових мігрецій
│   └── versions/                   # Вже створені міграції
│       └── 52716868fb41_initial_schema_with_enum_classification_.py
│
├── migrations/                     # Ручні SQL-міграції (для специфічних змін)
│   └── migrate_classification_enum.py
│
└── templates/                      # Jinja2 шаблони HTML
    ├── base.html                   # Основний layout (nav, head, footer)
    ├── index.html                  # Головна сторінка
    ├── login.html                  # Форма входу
    ├── register.html               # Форма реєстрації
    ├── dashboard_admin.html        # Адмін-панель
    ├── dashboard_user.html         # Користувацька панель
    ├── add_camera.html             # Форма для створення камери
    ├── edit_camera.html            # Форма для редагування камери
    ├── add_object.html             # Форма для створення об'єкта (адмін)
    ├── edit_object.html            # Форма для редагування об'єкта
    ├── user_add_object.html        # Форма для додавання об'єкта (користувач)
    ├── view_camera.html            # Перегляд деталей камери й об'єктів
    ├── add_event.html              # Логування события
    ├── edit_user.html              # Редагування користувача (адмін)
    └── dashboard_admin.html        # (архаїчний дубль, можна видалити)
```

### Application Factory Pattern

```python
# app.py
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 1. Ініціалізація розширень
    db.init_app(app)
    login_manager.init_app(app)
    
    # 2. Реєстрація маршрутів
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        ...
    
    # 3. Іншаї конфіґурація
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Автоматичне створення таблиць
    app.run(debug=True)
```

**Переваги:**
- Розділення конфіґурації від логіки.
- Легко тестувати (можна передати різні конфіґи).
- Можна створити кілька інстансів додатку для різних цілей.

---

## Структура БД

### Таблиця: `users`

Зберігає облікові дані й ролі користувачів.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(120) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(64) DEFAULT 'user',          -- 'user' або 'admin'
    access_level INTEGER DEFAULT 0,           -- 0..5, рівень доступу
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Приклад:**
```
id=1, username='maksym', email='test@gmail.com', role='user', access_level=1
id=2, username='admin', email='admin@example.com', role='admin', access_level=5
```

---

### Таблиця: `cameras`

Контейнери для утримання об'єктів.

```sql
CREATE TABLE cameras (
    id INTEGER PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    type VARCHAR(64),                         -- 'Containment', 'Surveillance', 'Laboratory' і т.д.
    max_capacity INTEGER DEFAULT 0,
    current_capacity INTEGER DEFAULT 0,
    security_level INTEGER DEFAULT 1,         -- Встановлюється автоматично за типом
    equipment_list TEXT,                      -- JSON або текстовий опис обладнання
    cleaning_schedule TEXT,                   -- Розклад чистіння
    maintenance_schedule TEXT,                -- Розклад техніки
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Приклад:**
```
id=1, name='Containment Cell-01', type='Containment', max_capacity=5, security_level=5
id=2, name='Lab-Observation', type='Laboratory', max_capacity=10, security_level=3
```

---

### Таблиця: `objects` (ObjectItem)

Аномальні об'єкти утримання.

```sql
CREATE TABLE objects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    classification VARCHAR(64) NOT NULL     -- Enum: 'Unspecified', 'Safe', 'Euclid', 'Keter', 'Thaumiel', 'Exotic', 'Metaclass'
                                             -- CHECK (classification IN ('Unspecified', 'Safe', ...))
    description TEXT,
    storage_requirements TEXT,
    camera_id INTEGER FOREIGN KEY,           -- Посилання на cameras.id
    status VARCHAR(64) DEFAULT 'stored',
    history_of_movements TEXT,               -- JSON історія переміщення
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Приклад:**
```
id=1, name='SCP-173', classification='Euclid', camera_id=1, status='stored'
id=2, name='SCP-500', classification='Safe', camera_id=2, status='stored'
```

---

### Таблиця: `events`

Логування подій (створення, редагування, видалення об'єктів).

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    type VARCHAR(64),                        -- 'create', 'update', 'delete', 'access'
    camera_id INTEGER FOREIGN KEY,
    object_id INTEGER FOREIGN KEY,
    user_id INTEGER FOREIGN KEY,             -- Хто виконав дію
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
```

**Приклад:**
```
id=1, type='create', object_id=1, user_id=2, timestamp='2025-11-26 01:43:00'
id=2, type='update', camera_id=1, user_id=2, timestamp='2025-11-26 01:44:00'
```

---

### Зв'язки між таблицями

```
users (1) ──── (N) events
           user_id

cameras (1) ──── (N) objects
            camera_id

cameras (1) ──── (N) events
            camera_id

objects (1) ──── (N) events
            object_id
```

---

## Ключові модулі й функції

### 1. **config.py** — Конфіґурація

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///scp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
```

**Що робить:**
- Зберігає налаштування додатку (база даних, секретний ключ).
- Використовується `app.config.from_object(Config)` у `create_app()`.

---

### 2. **models.py** — SQLAlchemy ORM Моделі

#### Клас: `User`

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(64), default='user')        # 'admin' або 'user'
    access_level = db.Column(db.Integer, default=0)       # 0..5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Хешує пароль за допомогою werkzeug"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Перевіряє пароль"""
        return check_password_hash(self.password_hash, password)
```

**Наслідується від:**
- `UserMixin` (Flask-Login) — дає методи `is_authenticated`, `is_active`, `is_anonymous`, `get_id()`.

**Методи:**
- `set_password(pwd)` — безпечно зберігає пароль у хешованому вигляді.
- `check_password(pwd)` — перевіряє введений пароль.

---

#### Клас: `Camera`

```python
class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))                    # SelectField у формі
    max_capacity = db.Column(db.Integer, default=0)
    current_capacity = db.Column(db.Integer, default=0)
    security_level = db.Column(db.Integer, default=1)  # Встановл. автоматично
    equipment_list = db.Column(db.Text)
    cleaning_schedule = db.Column(db.Text)
    maintenance_schedule = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Зав'язок:**
- `objects` — кількісний зв'язок (1 камера : N об'єктів).

---

#### Клас: `ObjectItem`

```python
class ObjectItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    classification = db.Column(
        db.Enum('Unspecified','Safe','Euclid','Keter','Thaumiel','Exotic','Metaclass', 
                name='scp_class'), 
        nullable=False, 
        default='Unspecified'
    )  # DB-level Enum
    description = db.Column(db.Text)
    storage_requirements = db.Column(db.Text)
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'), nullable=True)
    status = db.Column(db.String(64), default='stored')
    history_of_movements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Enum поле:**
- `classification` — DB-level Enum, гарантує що тільки допустимі значення можна вставити.
- На SQLite зберігається як TEXT із CHECK constraint.

---

#### Клас: `Event`

```python
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))                  # 'create', 'update', 'delete' і т.д.
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'), nullable=True)
    object_id = db.Column(db.Integer, db.ForeignKey('objects.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
```

**Логування:**
- Кожна значна операція створює запис у цій таблиці.
- Зв'язує користувача, камеру й об'єкт до операції.

---

### 3. **forms.py** — WTForms Схеми

#### Клас: `RegisterForm`

```python
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
```

**Валідатори:**
- `DataRequired()` — поле обов'язкове.
- `Length(3, 120)` — від 3 до 120 символів.
- `Email()` — перевіряє формат email.
- `EqualTo('password')` — пароль повинен збігатися з підтвердженням.

---

#### Клас: `ObjectForm`

```python
SCP_CLASS_CHOICES = [
    ('Unspecified', 'Непозначений (сірий)'),
    ('Safe', 'Безпечний (зелений)'),
    ('Euclid', 'Евклід (жовтий)'),
    ('Keter', 'Кетер (червоний)'),
    ('Thaumiel', 'Тауміель (чорний)'),
    ('Exotic', 'Екзотичний (синій)'),
    ('Metaclass', 'Метаклас (рожевий)'),
]

class ObjectForm(FlaskForm):
    name = StringField('Object Name', validators=[DataRequired(), Length(1, 256)])
    classification = SelectField('Classification', choices=SCP_CLASS_CHOICES, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    storage_requirements = TextAreaField('Storage Requirements', validators=[Optional()])
    camera_id = SelectField('Camera/Containment Unit', choices=[], validators=[Optional()], coerce=int)
    submit = SubmitField('Save Object')
```

**Поля:**
- `classification` — `SelectField` з українськими мітками (перекладено в v0.2).
- `camera_id` — `SelectField` з динамічним наповненням у маршрутах (`choices` встановлюється на GET/POST).
- `coerce=int` — конвертує значення SELECT у integer.

---

#### Клас: `CameraForm`

```python
CAMERA_TYPE_CHOICES = [
    ('Surveillance', 'Surveillance'),
    ('Containment', 'Containment Unit'),
    ('Laboratory', 'Laboratory'),
    ('Mobile', 'Mobile Camera'),
    ('External', 'External/Perimeter'),
    ('SecureVault', 'Secure Vault Camera'),
]

class CameraForm(FlaskForm):
    name = StringField('Camera Name', validators=[DataRequired(), Length(1, 128)])
    type = SelectField('Type', choices=CAMERA_TYPE_CHOICES, validators=[Optional()])
    max_capacity = IntegerField('Max Capacity', validators=[DataRequired()])
    security_level = IntegerField('Security Level', validators=[DataRequired()])
    equipment_list = TextAreaField('Equipment List', validators=[Optional()])
    cleaning_schedule = TextAreaField('Cleaning Schedule', validators=[Optional()])
    maintenance_schedule = TextAreaField('Maintenance Schedule', validators=[Optional()])
    submit = SubmitField('Save Camera')
```

**Поля:**
- `type` — `SelectField` для вибору типу камери.
- `security_level` — встановлюється автоматично за типом (у маршруті).

---

#### Клас: `AdminUserForm`

```python
class AdminUserForm(FlaskForm):
    role = SelectField('Role', choices=[('user','User'), ('admin','Admin')], validators=[DataRequired()])
    access_level = IntegerField('Access Level (0-5)', validators=[DataRequired()])
    submit = SubmitField('Save User')
```

**Назначение:**
- Адмін редагує роль і рівень доступу користувача.

---

### 4. **app.py** — Маршрути й бізнес-логіка

#### Структура маршрутів

```
/                                   → index()
/register                           → register() [GET, POST]
/login                             → login() [GET, POST]
/logout                            → logout() [GET]
/dashboard                         → dashboard() [перенаправляє]

/admin/dashboard                   → admin_dashboard()
/admin/camera/add                  → add_camera() [GET, POST]
/admin/camera/edit/<id>            → edit_camera() [GET, POST]
/admin/camera/delete/<id>          → delete_camera() [GET]
/admin/object/add                  → add_object() [GET, POST]
/admin/object/edit/<id>            → edit_object() [GET, POST]
/admin/object/delete/<id>          → delete_object() [GET]
/admin/event/add                   → add_event() [GET, POST]
/admin/user/edit/<id>              → edit_user() [GET, POST]

/user/dashboard                    → user_dashboard()
/user/camera/<id>                  → view_camera()
/user/object/add                   → user_add_object() [GET, POST]
```

---

#### Приклад маршруту: `add_object()`

```python
@app.route('/admin/object/add', methods=['GET', 'POST'])
@login_required
def add_object():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    form = ObjectForm()
    cameras = Camera.query.all()
    form.camera_id.choices = [(0, '-- Select Camera --')] + [(c.id, c.name) for c in cameras]
    
    if form.validate_on_submit():
        obj = ObjectItem(
            name=form.name.data,
            classification=form.classification.data,           # Із SelectField
            description=form.description.data,
            storage_requirements=form.storage_requirements.data,
            camera_id=form.camera_id.data if form.camera_id.data and form.camera_id.data != 0 else None
        )
        db.session.add(obj)
        db.session.commit()
        flash('Object created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_object.html', form=form)
```

**Логіка:**
1. Перевіряє логін (`@login_required`).
2. Перевіряє роль (тільки адмін може додавати об'єкти).
3. Динамічно заповнює `form.camera_id.choices` доступними камерами.
4. При валідному POST — створює `ObjectItem` та зберігає в БД.
5. Переводить на dashboard з повідомленням про успіх.

---

#### Приклад маршруту: `add_camera()`

```python
CAMERA_SECURITY_MAP = {
    'Containment': 5,
    'SecureVault': 5,
    'Laboratory': 3,
    'Surveillance': 2,
    'Mobile': 1,
    'External': 1,
}

@app.route('/admin/camera/add', methods=['GET', 'POST'])
@login_required
def add_camera():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    form = CameraForm()
    if form.validate_on_submit():
        sec = CAMERA_SECURITY_MAP.get(form.type.data, form.security_level.data)
        camera = Camera(
            name=form.name.data,
            type=form.type.data,
            max_capacity=form.max_capacity.data,
            security_level=sec,  # Автоматично встановлено за типом
            equipment_list=form.equipment_list.data,
            cleaning_schedule=form.cleaning_schedule.data,
            maintenance_schedule=form.maintenance_schedule.data
        )
        db.session.add(camera)
        db.session.commit()
        flash('Camera created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_camera.html', form=form)
```

**Автоматичне встановлення security_level:**
- Якщо користувач обере тип камери, `security_level` встановлюється автоматично.
- `CAMERA_SECURITY_MAP` містить маппінг типів на рівні безпеки.

---

#### Аутентифікація: `login()`

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        credential = form.username.data  # може бути username або email
        user = User.query.filter(
            (User.username == credential) | (User.email == credential)
        ).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)  # Flask-Login управління сесією
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Invalid credentials.', 'danger')
    
    return render_template('login.html', form=form)
```

**Особливості:**
- Можна входити за username АБО email.
- `login_user(user)` — Flask-Login встановлює сесію.
- `next_page` — перенаправляє на попередню сторінку (якщо була).

---

### 5. **templates/** — Jinja2 шаблони

#### `base.html` — Макет

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}SCP Foundation Management{% endblock %}</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        nav { border-bottom: 2px solid #333; padding: 10px 0; }
        .card { border: 1px solid #ccc; padding: 15px; margin: 10px 0; }
        .form { max-width: 600px; }
    </style>
</head>
<body>
    <nav>
        {% if current_user.is_authenticated %}
            Welcome, {{ current_user.username }} ({{ current_user.role }})
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
            <a href="{{ url_for('register') }}">Register</a>
        {% endif %}
    </nav>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    {% block content %}{% endblock %}
</body>
</html>
```

**Особливості:**
- `{% block content %}` — місце для специфічного вмісту сторінки.
- `current_user` — об'єкт авторизованого користувача (Flask-Login).
- `get_flashed_messages()` — виводить flash-повідомлення.

---

#### `add_object.html` — Форма додавання об'єкта

```html
{% extends "base.html" %}
{% block content %}
<div class="card form">
  <h2>Add Object</h2>
  <form method="POST">
    {{ form.hidden_tag() }}  <!-- CSRF токен -->
    
    {{ form.name.label }}
    {{ form.name(style="width:100%; padding:10px;") }}
    
    {{ form.classification.label }}
    {{ form.classification(style="width:100%; padding:10px;") }}  <!-- SelectField -->
    
    {{ form.description.label }}
    {{ form.description() }}
    
    {{ form.storage_requirements.label }}
    {{ form.storage_requirements() }}
    
    {{ form.camera_id.label }}
    {{ form.camera_id(style="width:100%; padding:10px;") }}  <!-- SelectField із динамічними choices -->
    
    {{ form.submit() }}
  </form>
</div>
{% endblock %}
```

**WTForms рендеринг:**
- `form.hidden_tag()` — вставляє CSRF токен.
- `form.field.label` — виводить мітку поля.
- `form.field()` — виводить HTML-елемент введення (input/select/textarea).

---

### 6. **view_db.py** — Утиліта для перевірки БД

```python
from app import create_app, db
from models import User, Camera, ObjectItem, Event

app = create_app()
with app.app_context():
    print("=== USERS ===")
    for u in User.query.all():
        print(f"ID: {u.id}, Username: {u.username}, Role: {u.role}, Access: {u.access_level}")
    
    print("\n=== CAMERAS ===")
    for c in Camera.query.all():
        print(f"ID: {c.id}, Name: {c.name}, Type: {c.type}, Security: {c.security_level}")
    
    print("\n=== OBJECTS ===")
    for o in ObjectItem.query.all():
        print(f"ID: {o.id}, Name: {o.name}, Classification: {o.classification}, Camera: {o.camera_id}")
    
    print("\n=== EVENTS ===")
    for e in Event.query.all():
        print(f"ID: {e.id}, Type: {e.type}, User: {e.user_id}, Time: {e.timestamp}")
```

**Використання:**
```bash
python view_db.py
```

---

## Потік роботи (User Stories)

### 1. Реєстрація нового користувача

1. Користувач відвідує `/register`.
2. Заповнює форму (username, email, password).
3. Flask валідує дані.
4. Пароль хешується за допомогою werkzeug.
5. Новий `User` об'єкт додається в БД (роль за замовчуванням: 'user').
6. Користувач перенаправляється на `/login`.

```python
# У forms.py валідація
username = StringField('Username', validators=[DataRequired(), Length(3, 120)])
```

---

### 2. Логін користувача

1. Користувач вводить username/email і пароль.
2. Flask-Login перевіряє креденціали.
3. `check_password()` порівнює введений пароль з хешем.
4. Якщо вірно — `login_user()` встановлює сесію.
5. Користувач перенаправляється на `/dashboard`.

```python
if user and user.check_password(form.password.data):
    login_user(user)
```

---

### 3. Адмін створює камеру

1. Адмін входить з роллю `admin`.
2. Переходить на `/admin/camera/add`.
3. Заповнює форму (name, type, max_capacity).
4. Тип обирається зі `SelectField`.
5. `security_level` встановлюється автоматично за `CAMERA_SECURITY_MAP`.
6. Камера додається в БД, адмін перенаправляється на dashboard.

```python
sec = CAMERA_SECURITY_MAP.get(form.type.data, form.security_level.data)
camera.security_level = sec
```

---

### 4. Адмін додає об'єкт

1. Адмін переходить на `/admin/object/add`.
2. Форма містить SelectField з українськими класами SCP.
3. Адмін обирає класифікацію (зелено позначений "Безпечний", червоно "Кетер" і т.д.).
4. Обирає камеру з динамічного `SelectField`.
5. Об'єкт зберігається з `classification` значенням.

```python
form.camera_id.choices = [(0, '-- Select Camera --')] + [(c.id, c.name) for c in cameras]
obj.classification = form.classification.data  # Із SelectField
```

---

### 5. Користувач переглядає камери й додає об'єкт

1. Користувач входить з роллю `user`.
2. Переходить на `/user/dashboard`, бачить список камер.
3. Клацає на камеру → переходить на `/user/camera/<id>`.
4. Бачить деталі камери й об'єкти всередині.
5. Клацає "Add Object" → `/user/object/add`.
6. Вибирає класифікацію й камеру, додає об'єкт.
7. Об'єкт додається з `camera_id` посиланням на обрану камеру.

---

## Міграції БД (Alembic)

### Що таке Alembic?

**Alembic** — інструмент для версіювання й автоматизації змін схеми БД.

### Ініціалізація

```bash
alembic init -t generic alembic
```

Створює структуру:
```
alembic/
├── env.py              # Конфіґурація для роботи з БД
├── script.py.mako      # Шаблон для нових мігрецій
└── versions/           # Папка для файлів мігрецій
```

### Конфіґурація (`alembic.ini`)

```ini
sqlalchemy.url = sqlite:///scp.db
```

---

### Конфіґурація середовища (`alembic/env.py`)

```python
from models import db
target_metadata = db.metadata  # Метаинформація про таблиці з SQLAlchemy
```

---

### Автогенерація першої міграції

```bash
alembic revision --autogenerate -m "Initial schema with Enum classification and access_level"
```

Створює файл `alembic/versions/52716868fb41_initial_schema_with_enum_classification_.py`:

```python
def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('objects', 'classification',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               nullable=True)
    op.create_foreign_key(None, 'objects', 'cameras', ['camera_id'], ['id'])

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'objects', type_='foreignkey')
    op.alter_column('objects', 'classification',
               existing_type=sa.String(length=64),
               type_=sa.TEXT())
```

---

### Застосування міграції

```bash
alembic upgrade head
```

Запускає `upgrade()` функцію й оновлює схему БД.

---

### Відкат міграції

```bash
alembic downgrade -1
```

Запускає `downgrade()` функцію й повертає БД на попередню версію.

---

### Добавлення нової міграції після змін у models.py

```bash
# 1. Змінити models.py, наприклад додати нове поле
class User(db.Model):
    seniority = db.Column(db.Integer, default=1)

# 2. Автогенерувати міграцію
alembic revision --autogenerate -m "Add seniority to users"

# 3. Переглянути згенерований файл
# vim alembic/versions/xxx_add_seniority_to_users.py

# 4. Застосувати
alembic upgrade head
```

---

## Резюме технічного стеку

| Компонент | Технологія | Призначення |
|-----------|-----------|-----------|
| **Backend** | Flask 2.3.3 | HTTP сервер, маршрутизація |
| **Authentication** | Flask-Login | Сесії, @login_required |
| **ORM** | SQLAlchemy 2.x | Модели, запити |
| **Валідація форм** | WTForms + Flask-WTF | SelectField, CSRF |
| **БД** | SQLite | Локальна база (розробка) |
| **Версіювання БД** | Alembic | Міграції, rollback |
| **Хеширування** | Werkzeug | bcrypt для паролів |
| **Frontend** | Jinja2 + HTML/CSS | Шаблони, стилізація |
| **VCS** | Git + GitHub | Репозиторій, теги |

---

## Безпека

### Реалізовані заходи

1. **CSRF захист** — `form.hidden_tag()` у кожній формі.
2. **Хеширування паролів** — werkzeug `generate_password_hash()`.
3. **Аутентифікація** — Flask-Login сесії.
4. **Авторизація** — перевірка `current_user.role` в маршрутах.
5. **Enum в БД** — CHECK constraint на `classification`.
6. **SQL Injection** — SQLAlchemy параметризовані запити.

---

## Запуск проєкту

```bash
# 1. Активувати virtualenv
.\venv\Scripts\Activate.ps1

# 2. Встановити залежності
pip install -r requirements.txt

# 3. Запустити додаток
cd scp-backend
python app.py

# 4. Відвідати http://127.0.0.1:5000
```

---

## Статус v0.2

✅ Базова аутентифікація й ролі (admin/user)  
✅ CRUD для камер й об'єктів  
✅ Українські мітки класів SCP  
✅ SelectField для вибору камер  
✅ Автоматичне встановлення security_level  
✅ DB-level Enum для classification  
✅ Alembic для версіювання БД  
✅ Git + теги (v0.1, v0.2)  

---

## Можливі розширення (v0.3+)

- [ ] Веб-інтерфейс для Alembic міграцій.
- [ ] API (REST/GraphQL) для мобільних клієнтів.
- [ ] Пошук й фільтрація об'єктів.
- [ ] Завантаження файлів (фото, документи).
- [ ] Email повідомлення.
- [ ] Ролі з детальнішим перекладом на українську.
- [ ] Unit-тести й интеграційні тести.
- [ ] Production deployment (Gunicorn, Nginx, PostgreSQL).

---

## Контакти & Репозиторій

- **GitHub**: https://github.com/ArchoMontell/SCP_Project
- **Tags**: v0.1, v0.2
- **Branch**: main

---

**Документ створено**: 26 листопада 2025 р.
**Версія**: v0.2

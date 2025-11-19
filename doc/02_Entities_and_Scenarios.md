| Entity     | Attributes                                                                                                   | Description                                      |
|------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| **Camera** | `id`, `name`, `type`, `max_capacity`, `current_capacity`, `cleaning_schedule`, `maintenance_schedule`, `security_level`, `equipment_list` | Storage chamber containing anomalous objects     |
| **Object** | `id`, `name`, `classification (Safe / Dangerous / Paranormal)`, `description`, `storage_requirements`, `camera_id`, `history_of_movements` | Anomalous item stored in a chamber               |
| **User**   | `id`, `name`, `role (Admin / Security / Researcher)`, `access_rights`, `login`, `password`                   | System user with specific permissions            |
| **Event**  | `id`, `type (Access / Maintenance / Alarm)`, `camera_id`, `object_id`, `user_id`, `timestamp`, `notes`        | Logged event related to cameras or objects       |
| **Equipment** | `id`, `name`, `type`, `status`, `camera_id`                                                               | Devices installed in storage chambers (sensors)  |




3. Основні сценарії використання
Сценарії:

Адміністратор

Створення/редагування камер;

Призначення об’єктів у камери;

Перегляд заповненості та стану камер;

Планування прибирання та обслуговування.

Охоронець

Перевірка доступу до камер;

Фіксація подій доступу/тревоги;


Дослідник

Перегляд стану об’єктів;

Подання запиту на доступ до об’єктів;

Ведення журналу взаємодій з об’єктом.

Етапи реалізації:

Початковий – базова landing page, структура репозиторію, документація.

Середній – розробка сутностей, бази даних, API (без складного фронтенду).

Повний – інтерактивний дашборд, система подій та сповіщень, розширена аналітика.

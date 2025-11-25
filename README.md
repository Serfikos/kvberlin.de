# KV Berlin Parser

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## 🇺🇸 English

### Overview
**KV Berlin Parser** is a Python-based web scraping tool designed to extract detailed information about doctors and psychotherapists from the [KV Berlin (Kassenärztliche Vereinigung Berlin)](https://www.kvberlin.de/fuer-patienten/arzt-und-psychotherapeutensuche) directory.

The application navigates through the search results, handles pagination, expands detailed views (accordions), parses the data, and saves it into a **PostgreSQL** database via **Django ORM**.

### Features
*   **Selenium Automation:** Handles cookie consents, switches tabs to "Doctors", and manages dynamic content loading.
*   **Robust Parsing:** Uses BeautifulSoup to extract names, addresses, contact details, specializations, languages, and opening hours.
*   **Database Integration:** Stores data in a structured PostgreSQL database using Django models.
*   **Upsert Logic:** Uses `update_or_create` to prevent duplicates and update existing records based on a unique hash ID.
*   **Pagination Handling:** Automatically detects and clicks the "Next" button until all pages are processed.

### Tech Stack
*   **Python 3.10+**
*   **Django 5.1** (ORM & Models)
*   **Selenium** (Web Browser Automation)
*   **BeautifulSoup4** (HTML Parsing)
*   **PostgreSQL** (Database)

### Prerequisites
1.  **Google Chrome** installed.
2.  **PostgreSQL** installed and running.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/kv-berlin-parser.git
    cd kv-berlin-parser
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django selenium webdriver-manager beautifulsoup4 psycopg2-binary
    ```

4.  **Database Configuration:**
    *   Ensure PostgreSQL is running.
    *   Create a database and user matching `KVBerlinParser_project/settings.py` (or update the settings file):
        *   **DB Name:** `kvberlin_db`
        *   **User:** `kv_user`
        *   **Password:** `111`
    
    *   *SQL command example:*
        ```sql
        CREATE DATABASE kvberlin_db;
        CREATE USER kv_user WITH PASSWORD '111';
        ALTER ROLE kv_user SET client_encoding TO 'utf8';
        ALTER ROLE kv_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE kv_user SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE kvberlin_db TO kv_user;
        -- Grant schema usage for Postgres 15+
        \c kvberlin_db
        GRANT ALL ON SCHEMA public TO kv_user;
        ```

5.  **Apply Migrations:**
    Initialize the database schema.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Usage

To start the scraping process, run the `main.py` script. It will open a browser window and start collecting data.

```bash
python main.py
```

*Note: The script initializes a headless-ready structure, but currently runs with the browser visible (`--start-maximized`).*

### Data Structure (Model)
The `Doctor` model includes:
*   `kv_id`: Unique hash based on name and address.
*   `name`, `title`: Doctor's name and academic title.
*   `street`, `zip_code`, `city`: Address details.
*   `contact`: Phone, Fax, Email, Website.
*   `languages`: List of languages spoken (ArrayField).
*   `specializations`: List of medical fields (ArrayField).
*   `opening_hours`: JSON object containing the weekly schedule.

---

<a name="russian"></a>
## 🇷🇺 Русский

### Описание
**KV Berlin Parser** — это инструмент для веб-скрейпинга на Python, предназначенный для сбора подробной информации о врачах и психотерапевтах из справочника [KV Berlin (Kassenärztliche Vereinigung Berlin)](https://www.kvberlin.de/fuer-patienten/arzt-und-psychotherapeutensuche).

Приложение проходит по страницам результатов поиска, управляет пагинацией, раскрывает блоки с подробной информацией (аккордеоны), парсит данные и сохраняет их в базу данных **PostgreSQL** через **Django ORM**.

### Возможности
*   **Автоматизация Selenium:** Автоматически принимает cookies, переключает вкладку на "Врачи" и обрабатывает динамический контент.
*   **Детальный парсинг:** Использует BeautifulSoup для извлечения имен, адресов, контактов, специализаций, языков и часов работы.
*   **Интеграция с БД:** Сохраняет данные в структурированную базу PostgreSQL, используя модели Django.
*   **Обновление данных:** Использует логику `update_or_create` для предотвращения дубликатов (на основе хеша уникальных данных).
*   **Обработка пагинации:** Автоматически находит кнопку "Далее" и проходит все страницы до конца списка.

### Стек технологий
*   **Python 3.10+**
*   **Django 5.1** (ORM и Модели)
*   **Selenium** (Автоматизация браузера)
*   **BeautifulSoup4** (Парсинг HTML)
*   **PostgreSQL** (База данных)

### Требования
1.  Установленный браузер **Google Chrome**.
2.  Установленная и запущенная СУБД **PostgreSQL**.

### Установка

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/your-username/kv-berlin-parser.git
    cd kv-berlin-parser
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install django selenium webdriver-manager beautifulsoup4 psycopg2-binary
    ```

4.  **Настройка базы данных:**
    *   Убедитесь, что PostgreSQL запущен.
    *   Создайте базу данных и пользователя, соответствующих настройкам в `KVBerlinParser_project/settings.py` (или измените файл настроек):
        *   **Имя БД:** `kvberlin_db`
        *   **Пользователь:** `kv_user`
        *   **Пароль:** `111`
    
    *   *Пример SQL команд:*
        ```sql
        CREATE DATABASE kvberlin_db;
        CREATE USER kv_user WITH PASSWORD '111';
        ALTER ROLE kv_user SET client_encoding TO 'utf8';
        ALTER ROLE kv_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE kv_user SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE kvberlin_db TO kv_user;
        -- Для Postgres 15+
        \c kvberlin_db
        GRANT ALL ON SCHEMA public TO kv_user;
        ```

5.  **Примените миграции:**
    Инициализация схемы базы данных.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Использование

Для запуска процесса сбора данных выполните скрипт `main.py`. Откроется окно браузера, и начнется сбор информации.

```bash
python main.py
```

### Структура данных (Модель)
Модель `Doctor` содержит:
*   `kv_id`: Уникальный хеш на основе имени и адреса.
*   `name`, `title`: Имя врача и ученая степень.
*   `street`, `zip_code`, `city`: Адресные данные.
*   `contact`: Телефон, Факс, Email, Веб-сайт.
*   `languages`: Список языков, на которых говорит врач (ArrayField).
*   `specializations`: Список специализаций (ArrayField).
*   `opening_hours`: JSON-объект с расписанием работы.

---

### Disclaimer / Отказ от ответственности
*English:* This tool is for educational purposes only. Please respect the website's `robots.txt` and Terms of Service. Do not overload the server with rapid requests.

*Русский:* Этот инструмент создан исключительно в образовательных целях. Пожалуйста, соблюдайте правила `robots.txt` и Условия использования целевого сайта. Не перегружайте сервер частыми запросами.

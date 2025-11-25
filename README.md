================================================================================
KV Berlin Parser
================================================================================
[English Section below]
[Русская версия ниже]

================================================================================
ENGLISH 🇺🇸
================================================================================

1. OVERVIEW
-----------
KV Berlin Parser is a Python-based web scraping tool designed to extract detailed 
information about doctors and psychotherapists from the KV Berlin directory 
(Kassenärztliche Vereinigung Berlin).

It saves data into a PostgreSQL database using Django ORM.

2. FEATURES
-----------
- Selenium Automation: Handles cookies, tabs, and dynamic content.
- Robust Parsing: Extracts names, addresses, contacts, specializations, etc.
- Database Integration: PostgreSQL + Django Models.
- Upsert Logic: Prevents duplicates using unique ID hashing.
- Pagination: Automatically processes all pages.

3. TECH STACK
-------------
- Python 3.10+
- Django 5.1
- Selenium
- BeautifulSoup4
- PostgreSQL

4. INSTALLATION
---------------
a. Clone the repository:
   git clone https://github.com/your-username/kv-berlin-parser.git
   cd kv-berlin-parser

b. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  (or venv\Scripts\activate on Windows)

c. Install dependencies:
   pip install django selenium webdriver-manager beautifulsoup4 psycopg2-binary

d. Database Setup (PostgreSQL):
   Create a database named 'kvberlin_db' and user 'kv_user' with password '111'.
   (See settings.py for details)

e. Migrations:
   python manage.py makemigrations
   python manage.py migrate

5. USAGE
--------
Run the main script to start scraping:
python main.py

The browser will open and begin collecting data automatically.

================================================================================
РУССКИЙ 🇷🇺
================================================================================

1. ОПИСАНИЕ
-----------
KV Berlin Parser — это инструмент на Python для сбора информации о врачах 
из справочника KV Berlin. Данные сохраняются в базу PostgreSQL.

2. ВОЗМОЖНОСТИ
--------------
- Автоматизация Selenium: работа с cookies, вкладками и динамическим контентом.
- Парсинг: сбор имен, адресов, контактов, часов работы и специализаций.
- База данных: Интеграция с PostgreSQL через Django.
- Дедупликация: Обновление существующих записей вместо создания дублей.
- Пагинация: Полный проход по всем страницам поиска.

3. ТЕХНОЛОГИИ
-------------
- Python 3.10+
- Django 5.1
- Selenium
- BeautifulSoup4
- PostgreSQL

4. УСТАНОВКА
------------
а. Склонируйте репозиторий:
   git clone https://github.com/your-username/kv-berlin-parser.git
   cd kv-berlin-parser

б. Создайте виртуальное окружение:
   python -m venv venv
   source venv/bin/activate  (или venv\Scripts\activate на Windows)

в. Установите зависимости:
   pip install django selenium webdriver-manager beautifulsoup4 psycopg2-binary

г. Настройка БД (PostgreSQL):
   Создайте БД 'kvberlin_db' и пользователя 'kv_user' с паролем '111'.

д. Миграции:
   python manage.py makemigrations
   python manage.py migrate

5. ИСПОЛЬЗОВАНИЕ
----------------
Запустите скрипт для начала сбора данных:
python main.py

================================================================================
DISCLAIMER
================================================================================
This tool is for educational purposes only. Respect robots.txt and TOS.
Этот инструмент создан в образовательных целях. Соблюдайте правила сайта.

# 👕 نظام إدارة متجر الملابس (Clothing Management System)

تطبيق ويب متكامل لإدارة حجوزات ومبيعات متجر ملابس، مبني باستخدام **Flask** و **SQLAlchemy** (مع نظام Migrations لتحديث الجداول).

---

## 🚀 طريقة التشغيل المحلية (Local Setup)

اتبع الخطوات التالية بالترتيب لتشغيل المشروع على جهازك الشخصي:

### 📋 المتطلبات الأساسية (Prerequisites)
تأكد من تثبيت الإصدارات التالية أو أحدث على جهازك:
* Python 3.9+
* Git

### 🛠️ خطوات التشغيل

**1. استنساخ المشروع (Clone the Repository):**
افتح الـ Terminal أو الـ CMD ونفذ الأمر التالي:
```bash
git clone [https://github.com/your-username/Clothing_Flask.git](https://github.com/your-username/Clothing_Flask.git)
cd Clothing_Flask
```
2. إنشاء وتفعيل البيئة الافتراضية (Virtual Environment):
لحماية مشروعك وعزل المكاتب الخاصة به عن بقية مكاتب الجهاز:

على نظام Windows:

```Bash
python -m venv venv
venv\Scripts\activate
```
على نظام Mac/Linux:

```Bash
python3 -m venv venv
source venv/bin/activate
```
3. تثبيت المكاتب الاعتمادية (Install Dependencies):
قم بتثبيت المكاتب المذكورة في ملف requirements.txt دفعة واحدة:

```Bash
pip install -r requirements.txt
```
4. تهيئة قاعدة البيانات والتحديثات (Database Initialization):
تأكد من إنشاء ملف قاعدة البيانات وتطبيق الجداول الجديدة (بناءً على الـ ERD المحدث):

```Bash
flask db init
flask db migrate -m "Initial database schema"
flask db upgrade
```
5. تشغيل سيرفر المطورين (Run the Application):
شغل السيرفر المحلي الآن:

```Bash
python run.py
```
أو عبر أمر فلاسك الصريح:

```Bash
flask run
```
6. تصفح التطبيق:
افتح متصفحك وتوجه إلى الرابط التالي:
```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)
📂 هيكلية المجلدات الأساسية (Project Structure)
Plaintext
Clothing_Flask/
│
├── Flask_app/             # المجلد الرئيسي للتطبيق (Package)
│   ├── __init__.py        # تهيئة فلاسك وقاعدة البيانات والـ Login Manager
│   ├── models.py          # جداول قاعدة البيانات (User, Booking, Product...)
│   ├── routes.py          # الـ Routes والـ Views الخاصة بالنظام
│   ├── static/            # الملفات الثابتة (CSS, JS, Images_Product)
│   └── templates/         # ملفات الـ HTML والـ Jinja (Admin / Client)
│
├── migrations/            # ملفات هجرة وتحديثات قاعدة البيانات (Alembic)
├── run.py                 # ملف نقطة الانطلاق لتشغيل السيرفر الرئيسي
└── requirements.txt       # ملف المكاتب البرمجية المطلوبة 
```

💻 التقنيات المستخدمة (Tech Stack)
Backend: Flask (Python 3)

Database ORM: Flask-SQLAlchemy (SQLite)

Migrations: Flask-Migrate (Alembic)

UI Design: Bootstrap 5 & Bootstrap Icons

---

### 💡 نصيحة سريعة ليك يا بهاء قبل ما ترفع المشروع:
تأكد إنك عامل ملف اسمه **`.gitignore`** في الفولدر الرئيسي للمشروع، وكاتب جواه السطرين دول:
```text
venv/
instance/
*.db
__pycache__/
```
ده فايدته إنه بيمنع الـ Git إنه يرفع فولدر البيئة الافتراضية أو ملف الداتا بيز التجريبية بتاعتك على الـ GitHub، وده بيخلي الـ Repository بتاعك نظيف ومحترف جداً.

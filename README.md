# Django Stripe Shop

Тестовый проект интернет-магазина с интеграцией Stripe Payment Intents API.


### Основные URL для тестирования  
- Товары: `/item/<id>/`  
- Оплата товара: `/item/<id>/payment/`  
- Заказы: `/order/<id>/`  
- Оплата заказа: `/order/<id>/payment/`

---

## Запуск локально

### 1. Клонирование репозитория
```bash
git clone https://github.com/IlHope/Stripe.git
cd repo

### 2. Создание виртуального окружения и установка зависимостей
python -m venv venv
source venv/bin/activate   # для Linux/Mac
venv\Scripts\activate      # для Windows

pip install -r requirements.txt

### 3. Настройка переменных окружения
Скопируйте .env.example в .env и заполните значениями
cp .env.example .env

### 4. Применение миграций
python manage.py migrate

### 5. Создание суперпользователя
python manage.py createsuperuser

### 6. Запуск сервера
python manage.py runserver

---

## Демо-версия на Railway
Проект задеплоен на Railway.
URL: https://yourproject.railway.app
Админка: https://yourproject.railway.app/admin
Логин/пароль: admin/admin
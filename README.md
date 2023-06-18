Тестовое задание rishat:  
===========
Задание
-----------
- Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
- Django Модель `Item` с полями `(name, description, price) `
- API с двумя методами:
    - GET `/buy/{id}`, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос` stripe.checkout.Session.create(...)` и полученный session.id выдаваться в результате запроса
    - GET `/item/{id}`, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном `Item` и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на `/buy/{id}`, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму `stripe.redirectToCheckout(sessionId=session_id)`
- Залить решение на Github, описать запуск в Readme.md
- Запуск используя `Docker`
- Использование `environment variables`
- Просмотр Django Моделей в Django Admin панели
- Добавить поле Item.currency, созадть 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте 
***

Подготовка перед запуском
-----------
Перед тем как запустить проект необходимо внести свой SECRET_KEY и PUBLISH_KEY из Stripe в файл docker-compose.yml в соответствующие поля.
***

Quickstart для Docker
----
```bash
git clone https://github.com/Enotlis/django_stripe.git
cd django_stripe
docker-compose build
docker-compose up -d
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser (создаете своего superuser)
```
***

Сервис
----------------------------
- `http://0.0.0.0:8000/admin/` - админ панель
- `http://0.0.0.0:8000/buy/<item_id>` - купить товар
- `http://0.0.0.0:8000/item/<item_id>` - страница товара
***

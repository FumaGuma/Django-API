# Django API

A simple college admission API written with Django and Django REST Framework.
You can test it out using the attached Postman collection.

### Technical info

API uses a Postgres database and JWT token authorization. To be able to access the
protected views with Postman first send a Get Token request with the email and password 
of previously created admin.

### Tests
Run the tests via `python manage.py test`
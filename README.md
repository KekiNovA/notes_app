# Notes App

This drf-based app is used to create, update and see version-history of notes.

## Installation (For local)

Clone the repository and follow the setups.

```bash
  cd notes_app
  python -m venv venv
```

Activate venv

```bash
  source ./venv/bin/activate #For Linux
  myenv\Scripts\activate #For Windows
```

Install Requirements

```bash
  pip install -r requirements.txt
```

Once done, start by running the migrations

```bash
  python manage.py migrate
```

You can create superuser (admin), just follow along the prompted steps -

```bash
  python manage.py createsuperuser
```

Done now you can start the server and test the apis on localhost:8000

```bash
  python manage.py runserver
```

## Documentation

For Documentation of apis you can visit localhost:8000/swagger or localhost:8000/redoc.
Have also included doctrings.

## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```

## Postman Collection

https://elements.getpostman.com/redirect?entityId=33036163-2eadca7d-52ea-43af-8548-5a8ff5fc672b&entityType=collection

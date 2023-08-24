# ClientSphere
## Customer and Order management system using Django

This guide will help you create an Order Management System with Create, Read, Update, and Delete (CRUD) functionality, user authentication and authorization, and search filtering using the Django web framework. We'll use Python, Django, and PostgreSQL for the project.
## Features

- Login and Registration
- Automated group assignment to customers after registration(using Signals)
- Efficient filtering and viewing of customers according to date or manually added notes
- Password reset functionality enhancing user convenience.
- Dedicated user profile pages
- AWS bucket to store static files and user PFP
## Installation
```sh
git clone https://github.com/abhavgoel/ClientSphere
cd ClientSphere
```
Create a new virtual environment to run the project. It is always a good practice to to make a dedicated virtual environment. I personally use conda for the same.
```sh
conda create --name clientsphere python=3.10
conda activate clientsphere
```

Download the necessary packages required to run the projects
```sh
pip install -r requirements.txt
```

Now to migrate the tables to the database you have to setup the database. I used PostgreSQL as the database.
Firstly make a .env file so that t stores all the keys required for the project

```sh
touch .env
```
The .env file should look like this 
```
EMAIL = <your email address>
EMAIL_PASS = <email password>
AWS_ACCESS_KEY = <aws access key>
AWS_SECRET_KEY = <aws secret key>
AWS_BUCKET_NAME = <aws bucket name>
DB_NAME = <data base name>
DB_USER = <database username>
DB_PASS = <database password>
DB_HOST = <database host>
DB_PORT = <database port>
DJANGO_SECRET_KEY = <django secret key>
```
Now navigate to settings.py file and under the DATABASES section, copy paste the below code to link your Postgres database
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER':config('DB_USER'),
        'PASSWORD':config('DB_PASS'),
        'HOST':config('DB_HOST'),
        'PORT':config('DB_PORT')
    }
}
```
I used python-decouple library to load ENV variables.
Now migrate the tables to the database by running the following command - 
```sh
python manage.py migrate
```
Now it is time to run the app, but firstly you have to make a superuser which will act as the admin for the app.
```sh
python manage.py createsuperuser
```
Enter the username and password for the superuser. Now run the app using - 
```
python manage.py runserver
```
Login using the superuser credentials or register as new user. As the superuser you can list the products to be displayed in the admin panel. Navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access the admin panel and customize according to your needs.
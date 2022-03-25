# PlerkServices
## Development Enviroment for Plerk services


This is just a development envrioment for Plerk services project. Please follow the install instructions.


## Prerequisites
- python
- pip
- virtualenv


## Install

1. Clone this repo:
```sh
git clone git@github.com:joseasantacruz/PlerkServices.git
```

2. Activate the virtual environment:
```sh
cd PlerkServices
virtualenv venv
source venv/bin/activate
```

3. From the new directory run the requirements install:
```sh
pip install -r requirements.txt
```

4. Execute the query to create user and database:
```sh
database.sql
```

5. Restore the database:
```sh
psql -h localhost -p 5432 -U plerkuser -d plerk < db
```

6. Create a superuser for the Django Admin:
```sh
cd plerkservices
python manage.py createsuperuser
```


7. Create a superuser for the Django Admin:
```sh
python manage.py runserver
```
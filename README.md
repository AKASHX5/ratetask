# ratetask

###setup database
``` psql -h localhost -d <DATABASE_NAME> -U <DATABASE_USER> -f /path/to/rates.sql ```
####to create a .env file in the same directory as the settings.py file and provide
            -SECRET_KEY=AlongRandomString
            -DATABASE_NAME=<DATABASE_NAME>
            -DATABASE_USER=<DATABASE_USER>
            -DATABASE_HOST=localhost
            -DATABASE_PORT=5432

####install virtualenv if not already installed
```pip install virtualenv```
```python3 -m venv venv```
```source venv/bin/activate```

####install djanog and necessary packages
```pip install -r requirements.txt```

####run django
```python manage.py runserver```

####run test cases
```python manage.py test```

####sample request
```http://127.0.0.1:8000/api/v1/task/price?date_from=2016-01-01&date_to=2016-01-26&orig_code=CNCWN&dest_code=FIKTK```
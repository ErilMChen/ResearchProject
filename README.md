1. run server 
    Execute the command : python manage.py runserver
    url : http://127.0.0.1:8000/map/

2. Database 
    This project is connected to the dublinbus database
    The database for a Django project is maintained uniformly through models.py
    If you need to create a new table, do not create it directly by accessing MySQL server

3. create tables in database
    Create the data model in models.py
        for example
            class weather(models.Model):
                id = models.IntegerField(primary_key = True)
                city = models.CharFied(unique = True, max_length = 45, null = False)
    Execute the command : python manage.py makemigrations map  (map can be replaced by other models like login)
    Execute the command : python manage.py migrate
    
    then Then you can scrape the data into the tables

4. html pages are in templates

5. The implementation of the GET/POST function needs to create functions in map/views.py, include path in map/urls.py

6. more information: https://docs.djangoproject.com/en/3.2/
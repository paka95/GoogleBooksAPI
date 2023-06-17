# GoogleBooksAPI

Simple API project to connect to Google Books API, get some data and then work with it from your database.

# Setup
* Download the project onto your system
* First you need to build containers. Go to root folder in the command line and enter "docker build ." in the command line
* Then you need to enter the command "docker-compose up -d --build" to create both containers
* Turn on the containers if they are not on yet and then go to https://localhost:8000/ to see if it works
* Swap the secret key for your own secret key in settings.py file (in googlebooks folder)
* Perform migrations - enter the command "docker-compose exec web python manage.py makemigrations" and then "docker-compose exec web python manage.py migrate"
* After that you should be able to create a new superuser in the command line (you need to do this in the container - using "docker-compose exec web python manage.py createsuperuser" command

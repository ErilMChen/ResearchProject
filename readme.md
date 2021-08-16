Welcome to the No Fuss Bus Application!

This project was developed as part of the Msc Computer Science (Conversion) course, from June 2021 - August 2021. The four team members involved in the planning, development and testing of the application are Michelle Duggan, Meng Chen, Jane Slevin and Kai Xu. 
This application aims to provide Dublin Bus passengers with accurate travel time estimates by training models on 2018 historical bus data, and 2018 weather data.
Other features have also been developed as means to provide passengers with real time information, saved preferences and locatioon services.

This repository contains the code required to set up and run the application locally. The live version of the application is deployed on a heroku server ( dublinbus.herokuapp.com ).


<img width="1262" alt="Screenshot 2021-08-16 at 13 09 34" src="https://user-images.githubusercontent.com/71897640/129561509-abfda508-6ba0-4909-9678-f55a0f134954.png">




Run the app locally 

1. Create a conda environment
2. Git clone this repo into a folder
3. Navigate to the downloaded file and check there is a requirements.txt file
4. Run pip install -r requirements.txt
5. Execute the command : 'python manage.py runserver' (url : http://127.0.0.1:8000/map/)
6. If you wish to add the cron scripts to your own system, 'run python manage.py crontab add' (contact us for the database information required to use these)
7. Enable location services

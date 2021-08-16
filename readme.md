<h2>Welcome to the No Fuss Bus Application!</h2>

This project was developed as part of the Msc Computer Science (Conversion) course, from June 2021 - August 2021. The four team members involved in the planning, development and testing of the application are Michelle Duggan, Meng Chen, Jane Slevin and Kai Xu. 
This application aims to provide Dublin Bus passengers with accurate travel time estimates by training models on 2018 historical bus data, and 2018 weather data.
Other features have also been developed as means to provide passengers with real time information, saved preferences and relavent travel information based on users' location.

This repository contains the code required to set up and host the application locally, but does not have the database credentials required to run the application. Create a dbinfo.py file in the mysite directory and fill in your own database info to have a working project.
The file must look like this:

myhost="...." <br>
mypasswd="..." <br>
myuser="..." <br>
mydatabase="..." <br>
mycharset="utf8mb4" <br>

engine = f"mysql+mysqlconnector://{myuser}:{mypasswd}@{myhost}:3306/{mydatabase}"




The live version of the application is deployed on a heroku server ( dublinbus.herokuapp.com ).


Basic functionality:
- Input of origin and destination address
- Input of date and time
- Map representation of the route
- Route detail
- Predicted travel time estimate

<img width="1262" alt="Screenshot 2021-08-16 at 13 09 34" src="https://user-images.githubusercontent.com/71897640/129561509-abfda508-6ba0-4909-9678-f55a0f134954.png">


Additional Functionality:
- User account creation
- Saving of favourite stations
- Live bus tweets
- Live traffic updates
- Live bus schedule for saved stations
- Saving of plans

<img width="461" alt="Screenshot 2021-08-16 at 13 13 33" src="https://user-images.githubusercontent.com/71897640/129562010-baf07af2-44ea-4698-a615-9f1333d6cd66.png">

<img width="1287" alt="Screenshot 2021-08-16 at 13 12 17" src="https://user-images.githubusercontent.com/71897640/129561887-bca5b33e-eeb8-4a0c-ae6e-f86fdc63c0cb.png">


<img width="646" alt="Screenshot 2021-08-16 at 13 13 57" src="https://user-images.githubusercontent.com/71897640/129562066-1d4e9945-1ec9-4637-a5af-d07da35addca.png">


<img width="771" alt="Screenshot 2021-08-16 at 13 14 39" src="https://user-images.githubusercontent.com/71897640/129562156-14b8defe-0509-4944-9e8b-b4b86c2210c8.png">



Navigate to the 'Wiki' panel to read about the development process.



Run the app locally 

1. Create a conda environment
2. Git clone this repo into a folder
3. Navigate to the downloaded file and check there is a requirements.txt file
4. Run pip install -r requirements.txt
5. Execute the command : 'python manage.py runserver' (url : http://127.0.0.1:8000/map/)
6. If you wish to add the cron scripts to your own system, 'run python manage.py crontab add' (contact us for the database information required to use these)
7. Enable location services

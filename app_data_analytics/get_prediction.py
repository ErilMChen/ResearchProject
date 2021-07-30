import pandas as pd
import pickle
from datetime import datetime
import mysql.connector

# Connect to database
myhost = "dubbusdb.cayveqvorwmz.eu-west-1.rds.amazonaws.com"
myuser = "admin"
mypasswd = "t8dubbus"
mydatabase = "dubbusdb"

db = mysql.connector.connect(
    host=myhost,
    user=myuser,
    password=mypasswd,
    database=mydatabase
)

cur = db.cursor()

def get_datetime(date, time):
    """Accepts date and time strings and returns correctly formatted datetime object"""

    datetime_string = date + " " + time
    datetime_object = datetime.strptime(datetime_string, "%d/%m/%Y %H:%M")

    return datetime_object


def get_weather(datetime_object):
    """Accepts datetime object and queries database for most recent weather data corresponding to datetime passed"""

    datetime_string = str(datetime_object)

    cur.reset()
    cur.execute(
        "SELECT * FROM weather_test WHERE weather_forecast.fdate < %s ORDER BY weather_forecast.fdate DESC LIMIT 1;",
        (datetime_string,))
    result = cur.fetchone()

    if result:
        return result

    else:
        print("No weather data available")


def get_hour_weekday_month(datetime_object):
    """Accepts datetime object and pulls hour, weekday and month from datetime object"""

    hour = datetime_object.hour
    weekday = datetime_object.isoweekday()
    month = datetime_object.month

    return hour, weekday, month


def get_cat_features(df):
    """Accepts dataframe of categorical features and returns list of features for which dummy value should equal 1"""

    cat_features = []

    for column in df:
        cat_features.append(column + "_" + str(df.iloc[0][column]))

    print(cat_features)


def create_dataframe(date, time):
    """Creates dataframe from user input and weather forecast data to pass to prediction model"""

    datetime_object = get_datetime(date, time)

    hour, weekday, month = get_hour_weekday_month(datetime_object)

    weather_result = get_weather(datetime_object)
    humidity, weather_main, wind_speed, pressure, feels_like, temp, temp_max, temp_min, wind_deg = weather_result[2], \
                                                                                                   weather_result[3], \
                                                                                                   weather_result[4], \
                                                                                                   weather_result[5], \
                                                                                                   weather_result[6], \
                                                                                                   weather_result[7], \
                                                                                                   weather_result[8], \
                                                                                                   weather_result[9], \
                                                                                                   weather_result[10]

    user_data = pd.DataFrame(columns=["temp", "feels_like", "humidity", "wind_speed", "wind_deg", "weather_main_Clouds",
                                      "weather_main_Drizzle", "weather_main_Fog", "weather_main_Mist",
                                      "weather_main_Rain", "weather_main_Smoke", "weather_main_Snow", "MONTH_2",
                                      "MONTH_3", "MONTH_4", "MONTH_5", "MONTH_6", "MONTH_7", "MONTH_8", "MONTH_9",
                                      "MONTH_10", "MONTH_11", "MONTH_12", "WEEKDAY_2", "WEEKDAY_3", "WEEKDAY_4",
                                      "WEEKDAY_5", "WEEKDAY_6", "WEEKDAY_7", "HOUR_3", "HOUR_4", "HOUR_5", "HOUR_6",
                                      "HOUR_7", "HOUR_8", "HOUR_9", "HOUR_10", "HOUR_11", "HOUR_12", "HOUR_13",
                                      "HOUR_14", "HOUR_15", "HOUR_16", "HOUR_17", "HOUR_18", "HOUR_19", "HOUR_20",
                                      "HOUR_21", "HOUR_22", "HOUR_23"])

    row = [0] * user_data.shape[1]
    series = pd.Series(row, index=user_data.columns)
    user_data = user_data.append(series, ignore_index=True)

    cat_features = {"weather_main": weather_main, "MONTH": month, "WEEKDAY": weekday, "HOUR": hour}
    cat_df = pd.DataFrame(cat_features)

    cat_feature_values = [[weather_main, month, weekday, hour]]
    cat_df = pd.DataFrame(cat_feature_values, columns=["weather_main", "MONTH", "WEEKDAY", "HOUR"])

    current_cat_features = get_cat_features(cat_df)

    for column, row in user_data.items():
        if column in current_cat_features:
            user_data.at[0, column] = 1

    user_data.at[0, "temp"] = temp
    user_data.at[0, "feels_like"] = feels_like
    user_data.at[0, "humidity"] = humidity
    user_data.at[0, "wind_speed"] = wind_speed
    user_data.at[0, "wind_deg"] = wind_deg

    return cat_df


def get_direction(line, headsign):
    """Accepts bus-line number and headsign and queries database for direction of journey"""

    cur.reset()
    cur.execute(
        "SELECT lines_for_plotting.direction_id FROM lines_for_plotting WHERE lines_for_plotting.line=%s AND lines_for_plotting.route_endpoint=%s LIMIT 1;",
        (line, headsign))
    result = cur.fetchone()

    return result[0]


def get_proportion(total_time, bus_line, direction, origin_stop, dest_stop):
    """Returns proportion of total journey-time that falls between user selected stops"""

    cur.reset()
    cur.execute(
        "SELECT stop_proportions.STOP_PERCENT FROM stop_proportions WHERE stop_proportions.LINEID=%s AND stop_proportions.DIRECTION=%s AND stop_proportions.STOPPOINTID=%s;",
        (bus_line, direction, origin_stop))
    origin_result = cur.fetchone()
    origin_pc = origin_result[0]

    cur.reset()
    cur.execute(
        "SELECT stop_proportions.STOP_PERCENT FROM stop_proportions WHERE stop_proportions.LINEID=%s AND stop_proportions.DIRECTION=%s AND stop_proportions.STOPPOINTID=%s;",
        (bus_line, direction, dest_stop))
    dest_result = cur.fetchone()
    dest_pc = dest_result[0]

    journey_pc = dest_pc - origin_pc

    journey_time = (journey_pc / 100) * total_time

    return journey_time


def get_prediction(origin_stop, dest_stop, bus_line, headsign, date, time):
    """Fetches pickled model from database and passes dataframe of user input to model, returning prediction.

    This is the main function which should be called from the front end."""

    direction = get_direction(bus_line, headsign)

    route = str(bus_line) + "_" + str(direction) + "RFR.pickle"

    cur.reset()
    cur.execute("SELECT RF_Key.id FROM RF_Key WHERE route=%s", route)
    id_result = cur.fetchone()
    pickle_ID = id_result[0]

    cur.reset()
    cur.execute("SELECT RF.pkl FROM RF WHERE id=%s", pickle_ID)
    pickle_result = cur.fetchone()
    pickle_from_db = pickle_result[0]

    input_dataframe = create_dataframe(date, time)

    model = pickle.loads(pickle_from_db)
    prediction = model.predict(input_dataframe)

    user_journey = get_proportion(prediction, bus_line, direction, origin_stop, dest_stop)

    user_journey_minutes = int(user_journey) // 60

    return user_journey_minutes

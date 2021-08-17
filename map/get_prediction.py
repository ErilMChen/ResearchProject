import pandas as pd
import pickle
from datetime import datetime
import mysql.connector
import bz2
# import time as tm
from mysite import dbinfo
# import sys

# Connect to database
try:
    db = mysql.connector.connect(
        host=dbinfo.myhost,
        user=dbinfo.myuser,
        password=dbinfo.mypasswd,
        database=dbinfo.mydatabase
    )

    cur = db.cursor()

except Exception as e:
    print("Database connection error:", e)


def get_datetime(date, time):
    """Accepts date and time strings and returns correctly formatted datetime object"""

    datetime_string = date + " " + time
    datetime_object = datetime.strptime(datetime_string, "%d/%m/%Y %H:%M")

    return datetime_object


def get_weather(datetime_object):
    """Accepts datetime object and returns most recent weather data from database corresponding to datetime passed"""

    datetime_string = str(datetime_object)

    cur.reset()
    cur.execute(
        "SELECT * FROM weather_forecast WHERE weather_forecast.fdate < %s ORDER BY weather_forecast.fdate DESC LIMIT 1;",
        (datetime_string,))
    result = cur.fetchone()

    if all(result):
        return result

    # If any null values exist take second most recent record
    else:
        cur.reset()
        cur.execute(
            "SELECT * FROM weather_forecast WHERE weather_forecast.fdate < %s ORDER BY weather_forecast.fdate DESC LIMIT 1, 1;")
        result = cur.fetchone()
        return result


def get_hour_weekday_month(datetime_object):
    """Accepts datetime object and pulls hour, weekday and month from datetime object"""

    hour = datetime_object.hour
    weekday = datetime_object.isoweekday() - 1
    month = datetime_object.month - 1

    return hour, weekday, month


def get_cat_features(df):
    """Accepts dataframe of categorical features and returns list of features for which dummy value should equal 1"""

    cat_features = []

    for column in df:
        cat_features.append(column + "_" + str(df.iloc[0][column]))

    return cat_features


def create_dataframe(date, time):
    """Creates dataframe from user input and weather forecast data to pass to prediction model"""

    datetime_object = get_datetime(date, time)

    hour, weekday, month = get_hour_weekday_month(datetime_object)

    weather_result = get_weather(datetime_object)
    humidity, weather_main, wind_speed, pressure, feels_like, temp, temp_max, temp_min, wind_deg = weather_result[2], \
                                                                                                   weather_result[3], \
                                                                                                   weather_result[4], \
                                                                                                   int(weather_result[5]), \
                                                                                                   weather_result[6], \
                                                                                                   weather_result[7], \
                                                                                                   weather_result[8], \
                                                                                                   weather_result[9], \
                                                                                                   weather_result[10]


    user_data = pd.DataFrame(columns=["temp", "feels_like", "temp_min", "temp_max", "pressure", "humidity",
                                      "wind_speed", "wind_deg", "MONTH_1", "MONTH_2", "MONTH_3", "MONTH_4", "MONTH_5",
                                      "MONTH_6", "MONTH_7", "MONTH_8", "MONTH_9", "MONTH_10", "MONTH_11", "WEEKDAY_1",
                                      "WEEKDAY_2", "WEEKDAY_3", "WEEKDAY_4", "WEEKDAY_5", "WEEKDAY_6", "HOUR_1",
                                      "HOUR_2", "HOUR_3", "HOUR_4", "HOUR_5", "HOUR_6", "HOUR_7", "HOUR_8", "HOUR_9",
                                      "HOUR_10", "HOUR_11", "HOUR_12", "HOUR_13", "HOUR_14", "HOUR_15", "HOUR_16",
                                      "HOUR_17", "HOUR_18", "HOUR_19", "HOUR_20", "HOUR_21", "HOUR_22", "HOUR_23",
                                      "weekend_true_1"])

    row = [0] * user_data.shape[1]
    series = pd.Series(row, index=user_data.columns)
    user_data = user_data.append(series, ignore_index=True)

    cat_data = {"MONTH": [month], "WEEKDAY": [weekday], "HOUR": [hour]}
    cat_df = pd.DataFrame(data=cat_data)

    current_cat_features = get_cat_features(cat_df)

    for column, row in user_data.items():
        if column in current_cat_features:
            user_data.at[0, column] = 1

    user_data.at[0, "temp"] = temp
    user_data.at[0, "temp_min"] = temp_min
    user_data.at[0, "temp_max"] = temp_max
    user_data.at[0, "feels_like"] = feels_like
    user_data.at[0, "humidity"] = humidity
    user_data.at[0, "wind_speed"] = wind_speed
    user_data.at[0, "wind_deg"] = wind_deg
    if weekday < 5:
        user_data.at[0, "weekend_true_1"] = 0
    else:
        user_data.at[0, "weekend_true_1"] = 1

    return user_data


def get_direction(origin_stop, dest_stop, bus_line):
    """Accepts bus-line number, origin stop and destination stop and returns direction, based on stop sequence.
    This function is only needed if both stops are in operation for both directions."""

    cur.reset()
    cur.execute(
        "SELECT stop_proportions.PROGRNUMBER FROM stop_proportions WHERE stop_proportions.LINEID=%s AND stop_proportions.STOPPOINTID=%s ORDER BY stop_proportions.ROUTEID, stop_proportions.PROGRNUMBER LIMIT 1;",
        (bus_line, origin_stop)
    )
    origin_seq = cur.fetchone()

    cur.reset()
    cur.execute(
        "SELECT stop_proportions.PROGRNUMBER FROM stop_proportions WHERE stop_proportions.LINEID=%s AND stop_proportions.STOPPOINTID=%s ORDER BY stop_proportions.ROUTEID, stop_proportions.PROGRNUMBER LIMIT 1;",
        (bus_line, dest_stop)
    )
    dest_seq = cur.fetchone()

    if origin_seq < dest_seq:
        direction = 0
    else:
        direction = 1

    return direction


def check_same_direction(origin_stop, dest_stop, bus_line):
    """Accepts origin and destination stops and bus line and verifies that stops share a direction for that line.
    This function returns the direction if the stops share one direction only for the line and otherwise calls get_direction
    to distinguish direction based on stop sequence."""

    cur.reset()
    cur.execute(
        "SELECT stop_proportions.DIRECTION FROM stop_proportions WHERE stop_proportions.LINEID=%s AND stop_proportions.STOPPOINTID=%s ORDER BY stop_proportions.ROUTEID, stop_proportions.PROGRNUMBER;",
        (bus_line, origin_stop)
    )

    origin_direction_result = cur.fetchall()

    origin_directions = []

    for row in origin_direction_result:
        origin_directions.append(row[0])

    cur.reset()
    cur.execute(
        "SELECT stop_proportions.DIRECTION FROM stop_proportions WHERE stop_proportions.LINEID=%s AND stop_proportions.STOPPOINTID=%s ORDER BY stop_proportions.ROUTEID, stop_proportions.PROGRNUMBER;",
        (bus_line, dest_stop)
    )

    dest_direction_result = cur.fetchall()

    dest_directions = []

    for row in dest_direction_result:
        dest_directions.append(row[0])

    shared_direction = [value for value in origin_directions if value in dest_directions]

    if len(shared_direction) > 1:
        direction = get_direction(origin_stop, dest_stop, bus_line)
        return direction

    elif len(shared_direction) == 1:
        direction = shared_direction[0]
        return direction

    else:
        return False


def check_stops_on_same_line(origin_stop, dest_stop, bus_line):
    """Returns boolean value indicating whether both stops exist on the same line"""

    cur.reset()
    cur.execute(
        "SELECT EXISTS (SELECT 1 FROM dubbusdb.stop_proportions WHERE LINEID=%s AND STOPPOINTID=%s);",
        (bus_line, origin_stop))
    origin_result = cur.fetchone()
    origin_true = origin_result[0]

    cur.reset()
    cur.execute(
        "SELECT EXISTS (SELECT 1 FROM dubbusdb.stop_proportions WHERE LINEID=%s AND STOPPOINTID=%s);",
        (bus_line, dest_stop))
    dest_result = cur.fetchone()
    dest_true = dest_result[0]

    if origin_true + dest_true == 2:
        return True
    else:
        return False


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


def get_prediction(origin_stop, dest_stop, bus_line, date, time):
    """Fetches pickled model from database and passes dataframe of user input to model, returning prediction.
    This is the main function which should be called from the front end."""

    # start = tm.perf_counter()

    # Return False if database connection has failed
    if not cur:
        return False

    try:

        bool_stops_on_line = check_stops_on_same_line(origin_stop, dest_stop, bus_line)

        if bool_stops_on_line:

            direction_bool = check_same_direction(origin_stop, dest_stop, bus_line)

            if direction_bool is not False:

                input_dataframe = create_dataframe(date, time)

                file_name = "map/pickled_models/{}_{}.pickle"
                compressed_pickle_file = (file_name.format(str(bus_line), str(direction_bool + 1)))

                pickle_file = bz2.open(compressed_pickle_file, "rb")
                read_pickle = pickle_file.read()

                model = pickle.loads(read_pickle)

                prediction = model.predict(input_dataframe)

                user_journey = get_proportion(prediction[0], bus_line, direction_bool, origin_stop, dest_stop)

                user_journey_minutes = int(user_journey) // 60

                # end = tm.perf_counter()
                # total = end - start
                # print("Time taken:", total)

                return user_journey_minutes

            else:
                return False

        else:
            return False

    except Exception as ex:
        print("Error:", ex)
        return False

import requests
import json
import datetime as dt
import taosrest

def get_weather(location,conn):
    payload = {'Key':'1a9c2effa96c47a1bd3113019242211','q':location,'aqi':'yes'}
    r = requests.get("http://api.weatherapi.com/v1/current.json",params=payload)

    r_string = r.json()
    current = r_string['current']

    origin_time = dt.datetime.strptime(current['last_updated'], '%Y-%m-%d %H:%M')

    current['last_updated'] = origin_time.strftime('%Y-%m-%d %H:%M:%S')
    print(current)

    write_weather(location,current,conn)
    return current

def open_conn():
    try:
        conn=taosrest.connect(url="https://gw.us-east-1.aws.cloud.tdengine.com",
                              token="56ef8a913fb397fb6c242d25d3f2f3f6d5b1057d")
    except taosrest.Error as e:
        print(e)
    return conn

def write_weather(location,weather_js,conn):
    no_whitespaces_location = location.replace(" ","")
    print(no_whitespaces_location)

    conn.query(f"INSERT INTO weather.{no_whitespaces_location} values ('{weather_js['last_updated']}',{weather_js['temp_c']},{weather_js['temp_f']},{weather_js['wind_mph']},{weather_js['wind_kph']})")

def close_conn(conn):
    conn.close()

if __name__=="__main__":

    conn = open_conn()

    get_weather("nairobi",conn)

    get_weather("kisumu",conn)

    close_conn(conn)
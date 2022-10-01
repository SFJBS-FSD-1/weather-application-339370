from flask import Flask, render_template, request
import requests
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def open_weather_city():
    if request.method == "POST":
        city = request.form["city"]
        api_key = "6ad0e17def8d15369d3c72ca88a98aab"
        url = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key+"&units=metric"
        api_response = requests.get(url).json()
        if api_response['cod'] == 200:
            timezone = int(api_response['timezone'])
            sunrise_utc = int(api_response['sys']['sunrise'])
            sunset_utc = int(api_response['sys']['sunset'])
            print_data = {
                'temp': api_response['main']['temp'],
                'city': api_response['name'],
                'longitude': api_response['coord']['lon'],
                'latitude': api_response['coord']['lat'],
                'sunrise': datetime.utcfromtimestamp(sunrise_utc + timezone).strftime('%H:%M:%S'),
                'sunset': datetime.utcfromtimestamp(sunset_utc + timezone).strftime('%H:%M:%S'),
                'status': 200
            }
        elif api_response['cod'] == '404':
            print_data = {'message': api_response['message'], 'status': 404}
        return render_template("index.html", data=print_data)
    else:
        print_data = None
        return render_template("index.html", data=print_data)


port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(port=port)
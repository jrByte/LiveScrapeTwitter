# Developed by JrByte on Github.

import datetime, pyowm, ast


class tweetInfo:

    def __init__(self, key, location, fahrenheit, humidity):
        self.accessOwmKey = key  # 6bf137ded78086566500b5b713d88237
        self.location = location  # Morgantown,US
        self.fahrenheit = fahrenheit  # boolean
        self.humidity = humidity  # needs to be added (boolean)

    @staticmethod
    def parseTweet(rawTweet):
        # This function can be used to parse the tweet.
        # Please keep in mind that you don't want this to take to long because tweepy's stream can get out of sync
        # and cause you to lose some tweets.
        return rawTweet

    @staticmethod
    def time():
        timeStamp = int(datetime.datetime.now().replace(microsecond=0).timestamp())
        print("Current UNIX Timestamp: " + str(timeStamp))
        return timeStamp

    def weather(self):
        # Fetching Weather data
        try:
            # Sending Location
            owm = pyowm.OWM(self.accessOwmKey)
            observation = owm.weather_at_place(self.location)
            weatherAPI = observation.get_weather()

            # Getting weather
            finalWeather = weatherAPI.get_status()

            # Getting temperature
            if self.fahrenheit:
                temperature = str(weatherAPI.get_temperature('fahrenheit'))
                Ctemp = ast.literal_eval(temperature)
                finalTemp = str(Ctemp['temp'])
            else:
                temperature = str(weatherAPI.get_temperature('celsius'))
                Ctemp = ast.literal_eval(temperature)
                finalTemp = str(Ctemp['temp'])

            if self.humidity:
                humidity = weatherAPI.get_humidity()

            return finalWeather, finalTemp, humidity

        except Exception as e:
            print("[✘]: Exception for Weather Data: " + str(e))
            finalTemp = "exception"
            finalWeather = "exception"

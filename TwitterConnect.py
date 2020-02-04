# Developed by JrByte on Github.
from oauthlib.oauth1.rfc5849.endpoints import access_token

from TwitterData import tweetInfo
import boto3
import tweepy
from tweepy import StreamListener, OAuthHandler, Stream

from main import liveConnection


class MyStreamListener(StreamListener):
    def __init__(self, region, tableName, AWS_accessKey, AWS_accessSecret, twitterID, twitterAccess_Token,
                 TwitterAccess_Secret, twitterConsumer_Key, twitterConsumer_Secret, uploadToDataBase, key, location,
                 fahrenheit, humidity):
        super().__init__()
        # DynamoDB Region and table name to add data to:
        self.region = region
        self.tableName = tableName
        # Uploading to the database is set to false by default.
        self.uploadToDataBase = uploadToDataBase
        # AWS Access:
        self.accessKey = AWS_accessKey
        self.accessSecret = AWS_accessSecret
        # Twitter App Login Data:
        self.twitterID = twitterID
        self.access_token = twitterAccess_Token
        self.access_secret = TwitterAccess_Secret
        self.consumer_key = twitterConsumer_Key
        self.consumer_secret = twitterConsumer_Secret
        # OWM Weather input:
        self.weatherKey = key
        self.weatherLocation = location  # bool
        self.weatherFahrenheit = fahrenheit  # bool
        self.weatherHumidity = humidity  # bool

        # Initialization of objects:
        # Weather object:
        self.tweetInfo = tweetInfo(self.weatherKey, self.weatherLocation, self.weatherFahrenheit,
                                   self.weatherHumidity)
        # List for the twitter API credentials:
        self.call = [self.access_secret, self.access_token, self.consumer_key, self.access_token, self.twitterID,
                     self.region, self.accessKey, self.accessSecret, self.tableName]
        # DynamoDB Boto3 object of credentials:
        self.dynamoDB = boto3.resource('dynamodb', region_name=self.region, aws_access_key_id=self.accessKey,
                                       aws_secret_access_key=self.accessSecret)

        # DynamoDB table object.
        self.dbTable = self.dynamoDB.Table(self.tableName)

    # This is a timeout function from Tweepy API.
    # Returns false to restart the connection.
    def on_timeout(self):
        print("\n[!]: Timeout function initiated.")
        return False

    # on_exception is responsible for an exception of something unhandled error from Tweepy occurs.
    # Returns false to restart the connection.
    def on_exception(self, exception):
        print("\n[✘]: Exception was raised...")
        print("[?]: Specific error was: " + str(exception) + ".")
        return False

    # Handles http error response codes. Returns false to restart the connection.
    def on_error(self, status_code):
        print("\n[✘]: Error: " + str(status_code))
        return False

    def get_upload(self):
        return self.uploadToDataBase

    def on_status(self, status):
        print("\n[✔]: on_status triggered")

        # Setting values for database
        time = str(self.tweetInfo.time())
        text = status.text
        weather = str(self.tweetInfo.weather()[0])
        temperature = str(self.tweetInfo.weather()[1])
        humidity = str(self.tweetInfo.weather()[2])

        # Parsing tweet for Database
        parsedTweet = self.tweetInfo.parseTweet(status.text)

        print("\n[TimeStamp]: " + time)
        print("[Tweet]: " + parsedTweet)
        print("[Weather]: " + weather)
        print("[Temp]: " + temperature)
        print("[Humidity]: " + humidity + "%")

        # Sending captured and parsed information to DynamoDB
        # On default it is disabled to prevent unwanted data to the database.
        # This can be changed inside the json file (LoginData.json)

        print(self.get_upload())

        # TODO: Fix this to use the uploadToDatabase variable
        if False:
            print("\n[+]: Uploading to DynamoDB")
            self.dbTable.put_item(
                Item={
                    'Date': time,
                    'PRTStatus': parsedTweet,
                    'Weather': weather,
                    'Temperature': temperature,
                    'Humidity': humidity
                }
            )

        print("\n[✔]: on_status completed")
        print("[✔]: Open Connection Still Active")
        return True

    # function is meant to disconnect user from the open connection. Returns false to restart the connection.
    def disconnect(self):
        print("\n[-]: Disconnecting from Stream...")
        return False

    # Main function that is responsible to connect to twitter.
    def main(self):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        api = tweepy.API(auth)

        print("[+]: Opening Stream...")
        try:
            myStreamListener = MyStreamListener(self.region, self.tableName, self.uploadToDataBase, self.accessKey,
                                                self.accessSecret, self.twitterID, access_token,
                                                self.access_secret, self.consumer_key, self.consumer_secret,
                                                self.weatherKey, self.weatherLocation, self.weatherFahrenheit,
                                                self.weatherHumidity)

            myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
            print("[✔]: Following TwitterID: " + self.twitterID)
            myStream.filter(follow=[self.twitterID], is_async=False)

        except Exception as e:
            print("[✘]: Exception was raised...")
            print("[?]: Specific error was: " + str(e) + ".")

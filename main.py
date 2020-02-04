# Developed by JrByte on Github.
import json
import time
import TwitterConnect


class liveConnection:
    def __init__(self):
        self.jsonValues = []
        self.jsonDataKey = ["dynamoDB_Region", "dynamoDB_tableName", "AWS_accessKey",
                            "AWS_secretAccessKey", "twitterAccountID", "twitter_accessToken", "twitter_accessSecret",
                            "twitter_consumerKey", "twitter_consumerSecret", "uploadToDataBase", "key", "location",
                            "fahrenheit", "humidity"]

    @staticmethod
    def readFileData():
        with open("LoginData.json") as f:
            try:
                data = json.loads(f.read())
            except Exception as e:
                print("[!]: File reading had an exception: " + str(e))
        return data

    @staticmethod
    def writeFileData(dictData):
        print("\n[+]: Writing  new data to LoginData.json...")
        with open("LoginData.json", 'w') as json_file:
            json.dump(dictData, json_file)
            json_file.close
            print("[✔]: Finished.")

    def checkFile(self):
        # Checks if any keys exist
        dictData = self.readFileData()
        if not ("Data" in dictData):
            print("[!]: Key is missing in the jsonfile (LoginData.json).")
            dictData = {'Data': {}}
            for subKey in self.jsonDataKey:
                dictData['Data'][subKey] = None  # or ""
            self.writeFileData(dictData)

    def getFileData(self):
        # Reading and writing to the file.
        print("\n[+]: Reading the file and checking if all the required data is entered...")
        dictData = self.readFileData()
        missingData = False
        # This loop searches for the empty values for keys in the json file. User input is entered to the missing keys.
        for key in self.jsonDataKey:
            if bool(dictData["Data"].get(key)) or type(dictData["Data"].get(key)) is type(True):
                print("[✔]: " + key + " contains: " + str(dictData["Data"].get(key)))
                self.jsonValues.append(dictData["Data"].get(key))

            elif type(dictData["Data"].get(key)) is not type(True):
                print(dictData["Data"].get(key))
                print("\n[!]: Key (" + key + ") is empty...")
                while True:
                    inputData = (input("[+]: For the key (" + key + ") enter in a True or False as a value: "))

                    if inputData.upper() == "TRUE":
                        inputData = True
                        break
                    elif inputData.upper() == "FALSE":
                        inputData = False
                        break
                    else:
                        print("\n[✘]: Wrong input, try again...")
                        continue
                dictData['Data'][key] = inputData
                self.jsonValues.append(inputData)
                missingData = True

            else:
                print(dictData["Data"].get(key))
                print("\n[!]: Key (" + key + ") is empty...")
                inputData = (input("[+]: For the key (" + key + ") enter in value: "))
                dictData['Data'][key] = inputData
                self.jsonValues.append(inputData)
                missingData = True

        # Adding the new data to the jsonfile.
        if missingData:
            self.writeFileData(dictData)

        return self.jsonValues


if __name__ == "__main__":
    print("Developed by JrByte @ Github, last updated 2/4/2020")
    print("Intuitive python program to help you start scrapping twitter with a live connection while working with AWS services.")
    print("This includes other data that can accompany the fetched data like weather conditions and time.")
    print("All the credentials and any other information that dictates the actions of the program by default are ")
    print("empty or set to none. This can be found in the LoginData.json file.")
    main = liveConnection()
    main.checkFile()
    jsonData = main.getFileData()
    Session = TwitterConnect.MyStreamListener(*jsonData)

    # Loops to retry the connection till 500 second timeout.
    timer = 1
    while timer <= 500:
        timer = timer * 2
        print("\n[⏳]: Timer was triggered for: " + str(timer) + " seconds before connecting.")
        time.sleep(timer)
        try:
            print("\n[+]: Starting the session.")
            Session.main()
        except Exception as e:
            print("[!]: Exception was raised... program wasn't able to keep up with the stream in MAIN.")
            print("[?]: Specific error was: " + str(e))
            continue
        except KeyboardInterrupt:
            print("\n[✘]: KeyboardInterrupt from User")
            break

    # Disconnecting from the stream because of the timeout.
    Session.disconnect()

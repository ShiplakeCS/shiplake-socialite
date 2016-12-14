from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, DROPBOX_ACCESS_TOKEN
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import json
import dropbox
from datetime import datetime
from time import sleep
from netifaces import interfaces, ifaddresses, AF_INET
import RPi.GPIO as GPIO


auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
TRIGGER_MESSAGE = open('trigger','r').readline().rstrip("\n")
print("Using", TRIGGER_MESSAGE, "as trigger message")




class LightsController:
    STAR_LIGHTS = 18
    TREE_LIGHTS = 23
    BALL_LIGHTS = 24
    STATUS_LIGHT = 25

    def __init__(self):

        self.lightsBusy = False

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(18, GPIO.OUT)

        GPIO.setup(self.STAR_LIGHTS, GPIO.OUT)
        GPIO.setup(self.TREE_LIGHTS, GPIO.OUT)
        GPIO.setup(self.BALL_LIGHTS, GPIO.OUT)
        # GPIO.setup(self.STATUS_LIGHT, GPIO.OUT)
        print("Initialised GPIO pins")
        self.off()

    def off(self):

        print("**All lights off**")

        GPIO.output(self.STAR_LIGHTS, False)
        GPIO.output(self.TREE_LIGHTS, False)
        GPIO.output(self.BALL_LIGHTS, False)
        # GPIO.output(self.STATUS_LIGHT, False)

    def treeOn(self):

        GPIO.output(self.TREE_LIGHTS, True)

    def treeOff(self):

        GPIO.output(self.TREE_LIGHTS, False)

    def starOn(self):

        GPIO.output(self.STAR_LIGHTS, True)

    def starOff(self):

        GPIO.output(self.STAR_LIGHTS, False)

    def ballsOn(self):

        GPIO.output(self.BALL_LIGHTS, True)

    def ballsOff(self):

        GPIO.output(self.BALL_LIGHTS, False)

    def statusOn(self):

        print("**Status light on**")

        # GPIO.output(self.STATUS_LIGHT, True)

    def statusOff(self):

        print("**Status light off**")

        # GPIO.output(self.STATUS_LIGHT, False)

    def on(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime

        self.lightsBusy = True

        print("**All lights on**")
        for n in range(0, int(numberFlashes)):
            # print("flash number: " + str(n))
            self.treeOn()
            self.starOn()
            self.ballsOn()
            sleep(flashTime)

        self.off()

    def flashTree(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0, int(numberFlashes)):
            # print("flash number: " + str(n))
            self.treeOn()
            sleep(flashTime)
            self.treeOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashBalls(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0, int(numberFlashes)):
            self.ballsOn()
            sleep(flashTime)
            self.ballsOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashStar(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0, int(numberFlashes)):
            self.starOn()
            sleep(flashTime)
            self.starOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashStarAndBalls(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0, int(numberFlashes)):
            self.starOn()
            self.ballsOn()
            sleep(flashTime)
            self.starOff()
            self.ballsOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashAllTogether(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0, int(numberFlashes)):
            self.ballsOn()
            self.treeOn()
            self.starOn()
            sleep(flashTime)
            self.ballsOff()
            self.treeOff()
            self.starOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashAllSequence(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 3.0

        self.lightsBusy = True
        # print (datetime.datetime.now())

        for n in range(0, int(numberFlashes)):
            self.starOff()
            self.treeOn()
            sleep(flashTime)
            self.treeOff()
            self.ballsOn()
            sleep(flashTime)
            self.ballsOff()
            self.starOn()
            sleep(flashTime)

        # print (datetime.datetime.now())
        self.lightsBusy = False


# Set up Twitter listener
class listener(StreamListener):

    def on_data(self, data):
        d = json.loads(data)
        print("trigger message found in tweet: %s" % d['text'])
        return True

    def on_error(self, status):
        print (status)
        return False


def uploadIPtoDropbox():

    # Establish dropbox connection - useful for uploading IP address to DB

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        ip_message = "Socialite Christmas Jumper\n\n"

        # from http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
            ip_message = ip_message +  '%s: %s\n' % (ifaceName, ', '.join(addresses))

        ip_message = ip_message + "Updated: {1}".format("xx.xx.xx.xx", datetime.now())
        dbx.files_upload(ip_message.encode('utf-8'), '/jumper_ip.txt', mode=dropbox.files.WriteMode('overwrite'))
        print("IP address uploaded to Dropbox")

    except:
        print("Dropbox connection error. Attempting again in 10 seconds.")
        sleep(10)
        uploadIPtoDropbox()




def listenForTweets():
    try:
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=[TRIGGER_MESSAGE])
        print("Twitter stream listener started.")

    except:
        print("Twitter connection error. Trying again in 10 seconds.")
        sleep(10)
        listenForTweets()

lc = LightsController()
uploadIPtoDropbox()
lc.on(20)
#listenForTweets()
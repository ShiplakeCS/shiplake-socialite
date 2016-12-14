"""
Christmas Jumper
2015 A W Dimmick
"""

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
#import json
from time import sleep
#import datetime
import RPi.GPIO as GPIO

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
        #GPIO.setup(self.STATUS_LIGHT, GPIO.OUT)
        print("Initialised GPIO pins")
        self.off()

    def off(self):

        print("**All lights off**")

        GPIO.output(self.STAR_LIGHTS, False)
        GPIO.output(self.TREE_LIGHTS, False)
        GPIO.output(self.BALL_LIGHTS, False)
        #GPIO.output(self.STATUS_LIGHT, False)

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

        #GPIO.output(self.STATUS_LIGHT, True)

    def statusOff(self):

        print("**Status light off**")

        #GPIO.output(self.STATUS_LIGHT, False)

    def on(self, duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime

        self.lightsBusy = True

        print("**All lights on**")
        for n in range(0,int(numberFlashes)):
            #print("flash number: " + str(n))
            self.treeOn()
            self.starOn()
            self.ballsOn()
            sleep(flashTime)

        self.off()

    def flashTree(self,duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0,int(numberFlashes)):
            #print("flash number: " + str(n))
            self.treeOn()
            sleep(flashTime)
            self.treeOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashBalls(self,duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0,int(numberFlashes)):
            self.ballsOn()
            sleep(flashTime)
            self.ballsOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashStar(self,duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0,int(numberFlashes)):
            self.starOn()
            sleep(flashTime)
            self.starOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashStarAndBalls(self,duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0,int(numberFlashes)):
            self.starOn()
            self.ballsOn()
            sleep(flashTime)
            self.starOff()
            self.ballsOff()
            sleep(flashTime)

        self.lightsBusy = False        

    def flashAllTogether(self,duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 2.0

        self.lightsBusy = True

        for n in range(0,int(numberFlashes)):
            self.ballsOn()
            self.treeOn()
            self.starOn()
            sleep(flashTime)
            self.ballsOff()
            self.treeOff()
            self.starOff()
            sleep(flashTime)

        self.lightsBusy = False

    def flashAllSequence(self,duration):

        flashTime = 0.2
        numberFlashes = duration / flashTime / 3.0

        self.lightsBusy = True
        #print (datetime.datetime.now())

        for n in range(0,int(numberFlashes)):
            self.starOff()
            self.treeOn()
            sleep(flashTime)
            self.treeOff()
            self.ballsOn()
            sleep(flashTime)
            self.ballsOff()
            self.starOn()
            sleep(flashTime)

        #print (datetime.datetime.now())
        self.lightsBusy = False
        

def showReady():
	
	global lc
	
	lc.flashAllTogether(2)

def showError():
	
	global lc
	
	for n in range(1,5):
	
		lc.starOn()
		sleep(0.2)
		lc.starOff()
		sleep(0.2)
		lc.starOn()
		sleep(0.2)
		lc.starOff()
		sleep(0.2)
		lc.starOn()
		sleep(2)
		lc.starOff()


def getDummyTweets():
    dummy = ['@shiplake_comp jumper on #testing','@shiplake_comp jumper flash #testing','@shiplake_comp jumper balls flash #testing','@shiplake_comp jumper balls on #testing']
    return dummy

# Twitter authentication constants
ACCESS_TOKEN = '4227530309-shKHCCLlDDuqFwhLqSTt4dDojH0THfARZ68X1Eu'
ACCESS_SECRET = 'A0dUHykLXpPSWeaOcYoYjQeaCdFCzgfmNlv9pg2kbsTcQ'
CONSUMER_KEY = 'gTJZFUWHMxdR5NARO7ZdJ1S40'
CONSUMER_SECRET = 'cy5FeX7GqcrBhnY0fE6bVHDVEUjrAqeqyPlnVlH7wtVyOs7i2C'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Preference constants
ACTIVITY_TIME = 20
TRIGGER_TEXT = "@shiplake_comp jumper"

lc = LightsController()

def realTweets():
	
	global lc
	
	try:

		stream = TwitterStream(auth=oauth)
		tweets = stream.statuses.filter(track=TRIGGER_TEXT)
		twitterInterface = Twitter(auth=oauth)
		
		showReady()
		print("Ready! Listening for tweets...")
		
		for tweet in tweets:

			print("Trigger tweet received: " + tweet['text'] + " - " + tweet['user']['name'])
			messageBack = "Hey @" + tweet['user']['screen_name'] + "! Thanks for your tweet. You made my "
			if "jumper flash" in tweet['text'].lower():
				messageBack = messageBack + "whole jumper flash! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.flashAllTogether(ACTIVITY_TIME)
			elif "jumper chase" in tweet['text'].lower():
				messageBack = messageBack + "lights flash up and down! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.flashAllSequence(ACTIVITY_TIME)
			elif "balls flash" in tweet['text'].lower():
				messageBack = messageBack + "bauble lights flash! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.flashBalls(ACTIVITY_TIME)
			elif "star flash" in tweet['text'].lower():
				messageBack = messageBack + "star lights flash! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.flashStar(ACTIVITY_TIME)
			elif "tree flash" in tweet['text'].lower():
				messageBack = messageBack + "tree flash! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.flashTree(ACTIVITY_TIME)
			elif "lights flash" in tweet['text'].lower():
				messageBack = messageBack + "tree flash! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.flashTree(ACTIVITY_TIME)
			elif "jumper on" in tweet['text'].lower():
				messageBack = messageBack + "whole jumper light up! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.on(ACTIVITY_TIME)
			elif "balls on" in tweet['text'].lower():
				messageBack = messageBack + "bauble lights light up! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.ballsOn()
				sleep(ACTIVITY_TIME)
				lc.ballsOff()
			elif "lights on" in tweet['text'].lower():
				messageBack = messageBack + "tree lights turn on! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.treeOn()
				sleep(ACTIVITY_TIME)
				lc.treeOff()
			elif "tree on" in tweet['text'].lower():
				messageBack = messageBack + "tree lights turn on! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.treeOn()
				sleep(ACTIVITY_TIME)
				lc.treeOff()
			elif "star on" in tweet['text'].lower():
				messageBack = messageBack + "star light up! #ChristmasJumper #Shiplake7 #Creative"
				#twitterInterface.statuses.update(status=messageBack)
				lc.starOn()
				sleep(ACTIVITY_TIME)
				lc.starOff()        
	

	except:		
		showError()
		print("Error connecting to Twitter. Trying again in 10 seconds.")
		sleep(10)
		realTweets()


def testTweets():
    for tweet in getDummyTweets():
        if "jumper flash" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.flashAllTogether(ACTIVITY_TIME)
        elif "jumper chase" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.flashAllSequence(ACTIVITY_TIME)
        elif "balls flash" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.flashBalls(ACTIVITY_TIME)
        elif "star flash" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.flashStar(ACTIVITY_TIME)
        elif "tree flash" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.flashTree(ACTIVITY_TIME)
        elif "jumper on" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.on(ACTIVITY_TIME)
        elif "balls on" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.ballsOn()
            sleep(ACTIVITY_TIME)
            lc.ballsOff()
        elif "tree on" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.treeOn()
            sleep(ACTIVITY_TIME)
            lc.treeOff()
        elif "star on" in tweet.lower():
            print ("Trigger tweet received: " + tweet)
            lc.starOn()
            sleep(ACTIVITY_TIME)
            lc.starOff()            
        sleep(2)

def simpleMode():
    print("Running in Simple Mode")
    lc.treeOn()
    while True:
        lc.flashStar(10)
        lc.starOn()
        lc.flashBalls(10)

#testTweets()
realTweets()
#simpleMode()

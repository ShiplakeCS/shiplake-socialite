# shiplake-socialite

This project is a Python3 app for powering a RaspberryPi-based light display, triggered by Twitter.

The app sets of a Twitter stream listener to tracks a trigger phrase, which then calls one or more functions within the program. Threading is used to allow the app to continue listening for twitter triggers whilst the light display activity is taking place.

Dropbox is used to upload the local IP of the Pi host in case zeroconf isn't working and you need to identify the IP address when running in a headless state (as in when it's connected to a jumper and a keyboard/monitor/mouse.

Flask has been added to provide a web-based controller also, in case Twitter is unavailable or if users simply want to directly control the lights without having to send a tweet.

The project uses the GPIO pins on the Raspberry Pi. It is configured to drive three LED light circuits, sharing a common ground on pin 14, and +3V on pins 12 (BCM 18), 16 (BCM 23) and 18 (BCM 24).

There are a number of dependencies required, most of which can be installed via pip3:
- flask -> sudo apt-get install python3-flask
- tweepy - pip3 install tweepy
- netifaces - download the source tar, extract and run python3 steup.py install
- dropbox - pip3 install dropbox

You will need to create apps within Twitter and Dropbox and then get access and consumer tokens and secrets, which then get placed in the keys.py file. Do NOT share your account access details with others!

Please do make use of this project and let us know what you build with it!

Mr. A. W. Dimmick
Teacher of Computer Science
Shiplake College, Henley-on-Thames, UK

computing@shiplake.org.uk | @shiplake_comp | www.shiplake.org.uk

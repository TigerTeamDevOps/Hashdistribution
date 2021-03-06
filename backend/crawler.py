#!/usr/bin/env python
# coding: utf8

from TwitterSearch import *
import os, sys, time, json, configparser
import random


def chachetime(datei):
    systime = time.time()
    filetime = os.path.getmtime(datei)
    global daysDiff
    daysDiff = (systime - filetime)
    if (daysDiff < 86400):  # Wenn Cache älter als 1 Tag
        return True  # Chache aktuell
    else:
        return False  # Neuen Cache erstellen


def gettweets(hashtag):
    if (os.path.isdir(".cache/")):
        datei = '.cache/{}.json'.format(hashtag)
    if not (os.path.isdir(".cache/")):
        os.system("mkdir .cache")
        print("Cache Ordner wurde erstellt!")
        datei = '.cache/{}.json'.format(hashtag)
    if (os.path.isfile(datei) and chachetime(datei)):  # Wenn Cache existiert
        with open(datei) as cachefile:  # Lese Cache aus
            print("Ausgabe aus Cache " + datei)
            print("Cache wurde zuletzt vor " + str(round(daysDiff / 3600, 2)) + " Stunde/n aktualisiert.")
            return json.loads(cachefile.read())  # Gebe Cache aus

    print("Chache {} wird neu erstellt".format(datei))
    tso = TwitterSearchOrder()  # Twitter Objekt erstellen
    tso.set_keywords([hashtag])  # Wir suchen nach einem hashtag
    tso.set_language('de')  # Nur Deutsche Tweets
    tso.set_include_entities(False)  # Kein Entity Zeug ausgeben

    Config = configparser.ConfigParser()
    configfiles = ['config.ini', 'config2.ini', 'config3.ini']
    configfile = random.choice(configfiles)
    print("Verwende " + configfile)
    if os.path.isfile(configfile):
        Config.read(configfile)
    else:
        print("The config file does not exist, please create a new config with the example file")
        sys.exit()

    consumer_key = Config.get("Twitter API", "consumer_key")
    consumer_secret = Config.get("Twitter API", "consumer_secret")
    access_token = Config.get("Twitter API", "access_token")
    access_token_secret = Config.get("Twitter API", "access_token_secret")

    # Objekt mit Zugangsdaten erstellen
    ts = TwitterSearch(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    tweets = set()
    counter = 0
    for tweet in ts.search_tweets_iterable(tso):
        if (counter <= 100):
            counter += 1
            tweets.add(tweet['text'])
        else:
            break

    tweets = list(tweets)

    with open(datei, 'w') as cachefile:
        tweetsasjson = json.dumps(tweets)
        cachefile.write(tweetsasjson)

    if (datei == "jugendhackt.json"):
        # os.system("sudo cp /home/pi/Hashdistribution/backend/.cache/jugendhackt.json /var/www/html/data/jh.json")
        print("Startseiten Tweets aktualisiert!")
    return tweets

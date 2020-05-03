# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 01:09:18 2020

@author: naren
"""

import pymongo
import pandas as pd
import json
from flask import *
from random import randint
app = Flask(__name__)

# Mongo db connection
client = pymongo.MongoClient("mongodb+srv://naren:narenmongodb@cluster0-jhuvp.mongodb.net/test?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true")
db = client["tweet_database"]
tweets = db.tweet_collection_final

@app.route('/')
def homePage():
    return render_template("index.html")

@app.route('/query', methods = ["GET","POST"])
def query():
    if request.method == "POST":
        select = str(request.form.get("select_query"))
        if select == "tweetType":
            tweet_type = {'original': 0, 'retweets': 0}
            for tweet in tweets.find():
                if tweet['retweet'] == False:
                    tweet_type['original'] += 1
                else:
                    tweet_type['retweets'] += 1
            return render_template("index.html", tweetType = tweet_type)
        elif select == "typeOfMedia":
            type_count = {"text": 0, "image":0, "both":0}
            for tweet in tweets.find():
                md = tweet["media"]
                if len(md) != 0:
                    if tweet["content"] == "":
                        type_count["image"] += 1 # Only Image
                    else:
                        type_count["both"] += 1 # Image and text
                else:
                    type_count["text"] += 1 # Only text
            return render_template("index.html", typeOfMedia = type_count)
        elif select == "distinctUser":
            distinct_users = set()
            for tweet in tweets.find():
                distinct_users.add(tweet['user_id'])
            return render_template("index.html", distinctUser = len(distinct_users))
        elif select == "topRetweet":
            max_retweet_count = 0
            for tweet in tweets.find():
                if tweet['retweet_count'] > max_retweet_count:
                    max_retweet_count = tweet['retweet_count']
                    tweet_id = tweet['id']
            print(max_retweet_count)

            myquery = {'id': tweet_id}
            twts = list(tweets.find(myquery))
            return render_template("index.html", topRetweet = twts[0])
        elif select == "topFav":
            max_FavCount = 0
            for tweet in tweets.find():
                if tweet['FavCount']>max_FavCount:
                    max_FavCount = tweet['FavCount']
                    tweet_id = tweet['id']
            print(max_FavCount)
            
            myquery = {'id': tweet_id}
            twts = list(tweets.find(myquery))
            return render_template("index.html", topFav = twts[0])
        elif select == "byWord":
            searchTerm = str(request.form["searchTerm"])
            print(searchTerm)
            myquery = {"content":{"$regex":searchTerm,"$options" :'i'}}
            twts = list(tweets.find(myquery))
            if twts:
                mydf = pd.DataFrame.from_records(twts)
                df1 = mydf[['user_name','content', 'created_at', 'hashtags', 'retweet_count','FavCount']]
                print(df1.head())
                return render_template("index.html", byWord =  df1.to_html(classes='data', header="true"), word = searchTerm, count = tweets.count_documents(myquery), found = True)
            else:
                return render_template("index.html", byWord = "No tweet found for the given word", found = False)
        elif select == "byHashtag":
            searchTerm = str(request.form["searchTerm"])
            searchTerm = "#" + searchTerm
            print(searchTerm)
            myquery = {"content":{"$regex":searchTerm,"$options" :'i'}}
            twts = list(tweets.find(myquery))
            if twts:
                mydf = pd.DataFrame.from_records(twts)
                df1 = mydf[['user_name', 'hashtags', 'content', 'created_at', 'retweet_count','FavCount']]
                return render_template("index.html", found = True, byHashtag =  df1.to_html(classes='data', header="true"), hashtag = searchTerm)
            else:
                return render_template("index.html", byHashtag = "No hashtags were used in any tweet", found = False)
        elif select == "timeRange":
            start = str(request.form["timeRangeStart"])
            end = str(request.form["timeRangeEnd"])
            start = start.replace("T"," ")
            end = end.replace("T"," ")
            start = start+":00"
            end = end+":00"
            print(end)
            twts = tweets.find({"created_at":{ "$gt": start, "$lt": end }})
            twts = list(twts)
            if twts:
                mydf = pd.DataFrame.from_records(twts)
                df1 = mydf[['user_name', 'hashtags', 'content', 'created_at', 'retweet_count','FavCount']]
                print(df1.head())
                return render_template("index.html", found = True, timeRange = df1.to_html(classes = 'data', header = 'true'), start = start, end = end)
            else:
                return render_template("index.html", timeRange = "There are no tweets within the given range", found = False)
        elif select == "byuname":
            searchTerm = str(request.form["searchTerm"])
            print(searchTerm)
            twts = tweets.find({"user_name":searchTerm})
            twts = list(twts)
            if twts:
                print(twts)
                mydf = pd.DataFrame.from_records(twts)
                df1 = mydf[['user_name', 'hashtags', 'content', 'created_at', 'retweet_count','FavCount']]
                print(df1.head())
                return render_template("index.html", byuname =  df1.to_html(classes='data', header="true"), uname = searchTerm, found = True)
            else:
                return render_template("index.html", byuname = "No data found for the query", found = False)
        elif select == "byuid":
            searchTerm = str(request.form["searchTerm"])
            print(searchTerm)
            twts = tweets.find({"user_id":searchTerm})
            twts = list(twts)
            if twts:
                mydf = pd.DataFrame.from_records(twts)
                df1 = mydf[['user_id', 'user_name', 'hashtags', 'content', 'created_at', 'retweet_count','FavCount']]
                return render_template("index.html", byuid =  df1.to_html(classes='data', header="true"), uid = searchTerm, found = True)    
            else:
                return render_template("index.html", byuid = "User id not found", found = False)
        elif select == "by2words":
            searchTerm1 = str(request.form["searchTerm1"])
            searchTerm2 = str(request.form["searchTerm2"])
            
            twts = tweets.find( {
                "$and" : [
                    {"content":{"$regex":searchTerm1,"$options" :'i'}} , {"content":{"$regex":searchTerm2,"$options" :'i'}}
                ]
            } )
            twts = list(twts)
            if twts:
                mydf = pd.DataFrame.from_records(twts)
                df1 = mydf[['user_id', 'user_name', 'hashtags', 'content', 'created_at', 'retweet_count','FavCount']]
                return render_template("index.html", by2words =  df1.to_html(classes='data', header="true"), term1 = searchTerm1, term2 = searchTerm2, found = True) 
            else:
                 return render_template("index.html", by2words = "No tweets found with given keywords", found = False)
        elif select == "tophashtag":
            hashtag_count = {}
            for tweet in tweets.find():
                ht = tweet["hashtags"]
                for hash in ht:
                    hash = hash.lower()
                    if hash not in hashtag_count:
                        hashtag_count[hash] = 1
                    else:
                        hashtag_count[hash] += 1

            hc = sorted(hashtag_count, key=hashtag_count.get, reverse=True)
            hc[:10]
            return render_template("index.html", hashtags = hc[:10])
        elif select == "trump":
            myquery = {"content":{"$regex":"trump","$options" :'i'}}
            return render_template("index.html", trump = tweets.count_documents(myquery))
        elif select == "trumpTweet":
            myquery = {"content":{"$regex":"trump","$options" :'i'}}
            twts = list(tweets.find(myquery))
            return render_template("index.html", trumpTweet = twts[randint(0, len(twts))]["content"])
if __name__ == "__main__":
    app.run(debug=True)

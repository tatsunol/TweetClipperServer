# -*- coding: utf-8
import os
import json
from collections import deque
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from flask import Flask, render_template
from flask import session, abort

from requests_oauthlib import OAuth1Session
import toml
import requests

monthes = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May' ,'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

app = Flask(__name__)

if os.path.exists(".keys"):
    keys = toml.load(open(".keys"))
    os.environ['CK'] = keys['CK']
    os.environ['CS'] = keys['CS']
    os.environ['AT'] = keys['AT']
    os.environ['ATS'] = keys['ATS']


@app.route("/tweet/<int:tweet_id>", methods=["GET"])
def tweet(tweet_id):

    session = OAuth1Session(os.environ['CK'], os.environ['CS'], os.environ['AT'], os.environ['ATS'])
    end_point = "https://api.twitter.com/1.1/statuses/show.json"
    params = {
        "id": tweet_id,
        "tweet_mode": "extended"
    }
    headers = {
        "content-type": "application/json"
    }
    response = session.get(end_point, params=params, headers=headers)

    if response.status_code == 200:
        tweet = response.json()

        if app.debug:
            with open("{}.json".format(tweet_id), 'w') as f:
                json.dump(tweet, f, ensure_ascii=False, indent=4)

        tweet['tweets'] = get_self_reply_trees(session, tweet)

        for t in tweet['tweets']:
            # created_at format => Sat Apr 11 13:25:05 +0000 2020
            weekday, monthstr, day, times, tz, year = tweet['created_at'].split()
            month = monthes.index(monthstr) + 1
            hour, minute, second = times.split(":")
            utc_datetime = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), tzinfo=timezone.utc)
            asia_tokyo_datetime = utc_datetime.astimezone(timezone(timedelta(hours=9)))
            t['datetime'] = asia_tokyo_datetime.strftime("%Y年%m月%d日 %H:%M:%S")

        return render_template('tweets.html', **tweet)

    elif response.status_code == 429:
        # API LIMIT ERROR
        tweet_url = "https://twitter.com/x/status/{}".format(tweet_id)
        return render_template('error.html', **{"url": tweet_url, "error": "api limit error"})

    else:
        tweet_url = "https://twitter.com/x/status/{}".format(tweet_id)
        return render_template('error.html', **{"url": tweet_url, "error": "twitter returns {}".format(response.status_code)})


def get_self_reply_trees(session, target_tweet):

    query = "from:{} to:{}".format(target_tweet['user']['screen_name'], target_tweet['user']['screen_name'])
    end_point = "https://api.twitter.com/1.1/search/tweets.json"
    params = {
        "q": query,
        "since_id" : target_tweet['id'],
        "tweet_mode": "extended",
        "include_entities": True
    }
    headers = {
        "content-type": "application/json"
    }
    response = session.get(end_point, params=params, headers=headers)
    all_replies = response.json()

    if app.debug:
        with open("{}_replies.json".format(target_tweet['id']), 'w') as f:
            json.dump(all_replies, f, ensure_ascii=False, indent=4)

    # ToDo: target tweet自体がself-replyの場合は，そのreply先を最初のtarget_tweetにする
    # ToDo: 会話API

    # Get Self Reply List from replies
    self_reply_tweets = [ target_tweet ]
    target_id_q= deque([target_tweet['id']])
    while target_id_q:
        target_id = target_id_q.popleft()

        # Target Tweet宛てのリプライを抽出
        matched_tweets = [ tweet for tweet in all_replies['statuses'] if tweet['in_reply_to_status_id'] == target_id]
        self_reply_tweets += matched_tweets
        # リプライのIDをTarget Tweetに
        matched_tweets_ids = [ tweet['id'] for tweet in matched_tweets]
        target_id_q.extend(matched_tweets_ids)

    return self_reply_tweets


if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0')

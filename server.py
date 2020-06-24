# -*- coding: utf-8
import toml
import requests
import os
from flask import Flask, render_template
from flask import session, abort
from filters import twitter
import json

from requests_oauthlib import OAuth1Session
from fake_useragent import UserAgent

app = Flask(__name__)

keys = toml.load(open(".keys"))
print(keys)

@app.route("/tweet/<int:tweet_id>", methods=["GET"])
def tweet(tweet_id):

    session = OAuth1Session(keys['CK'], keys['CS'], keys['AT'], keys['ATS'])

    end_point = "https://api.twitter.com/1.1/statuses/show.json"
    # end_point = "https://api.twitter.com/1.1/followers/ids.json"


    get_params = {
        "id": tweet_id,
        "tweet_mode": "extended"
    }
    headers = {
        "content-type": "application/json"
    }
    response = session.get(end_point, params=get_params, headers=headers)
    print(response.encoding)
    #data = json.loads(response.text)
    # json.dump(data, open("{}.json".format(tweet_id), 'w'), indent=4, ensure_ascii=False)

#     html = tweet_to_html(response.json())
# 
#     return html
# 
# def tweet_to_html(tweet):
    tweet = response.json()
    with open("{}.json".format(tweet_id), 'w') as f:
        json.dump(tweet, f, ensure_ascii=False, indent=4)


    tweet['datetime'] = tweet['created_at'].split("+")[0]

    return render_template('layout.html', **tweet)





def old(tweet_id):
    if not isinstance(tweet_id, int):
        abort(400)

    ua = UserAgent()
    ua.chrome

    tweet_url = "https://twitter.com/i/status/{0:d}".format(tweet_id)
    print(ua.chrome)
    ua_t = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    response = requests.get(tweet_url, headers = {'User-Agent': ua_t})

    print(os.environ)


    if response.status_code != 200:
        abort(response.status_code)

    filtered_html = twitter.filter(response.text)

    return filtered_html

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0')

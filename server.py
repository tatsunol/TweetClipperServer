# -*- coding: utf-8
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import session, abort

app = Flask(__name__)

@app.route("/tweet/<int:tweet_id>", methods=["GET"])
def tweet(tweet_id):
    if not isinstance(tweet_id, int):
        abort(400)

    tweet_html = get_tweet_html(tweet_id)
    return tweet_html

def get_tweet_html(tweet_id):
    tweet_url = "https://twitter.com/i/status/{0:d}".format(tweet_id)

    response = requests.get(tweet_url)

    if response.status_code != 200:
        abort(response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    buttons = soup.find_all("button")
    for button in buttons:
        button.extract()

    links = soup.find_all("a")
    for link in links:
        link.unwrap()

    footer = soup.find(attrs={"class":"stream-footer"})
    if footer is not None:
        footer.extract()

    new_html = "<html lang='ja'>"
    if soup.head is not None:
        new_html += soup.head.prettify()
    new_html += "<body>"

    main = soup.find(attrs={"role":"main"})
    if main is not None:
        new_html += main.prettify()

    new_html += "</body>"
    new_html += "</html>"

    return new_html

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0')
# -*- coding: utf-8
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import session, abort

app = Flask(__name__)
__style = """
<style>
    * {
        padding: 0;
        margin: 0;
    }
	li {
		list-style-type: none;
	}
    .AdaptiveMedia-photoContainer  {
        padding: 8px;
    }
	.tweet {
		background: #eeeeee;
		padding: 16px;
		margin: 16px;
		border-radius: 5px;
		box-shadow: 0 2px 5px #ccc;
	}
	.tweet-text {
		background: #efefef;
		padding: 4px;
        font-size: 1.2rem;
	}
    .QuoteTweet {
        background: #eeeeee;
        border : solid 1px #090909;
		padding: 16px;
		margin: 16px;
		border-radius: 5px;
		box-shadow: 0 2px 5px #ccc;
    }
</style>
"""


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

    metas = soup.find_all("meta")
    for meta in metas:
        meta.extract()

    scripts = soup.find_all("script")
    for script in scripts:
        script.extract()

    imgs = soup.find_all("img")
    for img in imgs:
        img["style"] = ""

    buttons = soup.find_all("button")
    for button in buttons:
        button.extract()
    
    links = soup.find_all("link")
    for link in links:
        link.extract()

    alinks = soup.find_all("a")
    for alink in alinks:
        alink.unwrap()

    dismiss_modules = soup.find_all(attrs={"class": "dismiss-module"})
    for dismiss_module in dismiss_modules:
        dismiss_module.extract()

    footer = soup.find(attrs={"class":"stream-footer"})
    if footer is not None:
        footer.extract()

    action = soup.find(attrs={"ProfileTweet-action"})
    if action is not None:
        action.extract()

    sfc = soup.find(attrs={"class": "stream-fail-container"})
    if sfc is not None:
        sfc.extract()

    adms = soup.find(attrs={"class": "AdaptiveMedia-singlePhoto"})
    if adms is not None:
        adms.unwrap()

    follow_bar = soup.find(attrs={"class": "follow-bar"})
    if follow_bar is not None:
        follow_bar.extract()

    avatar_row = soup.find(attrs={"class": "avatar-row"})
    if avatar_row is not None:
        avatar_row.extract()

    new_html = "<html lang='ja'>"
    title = soup.find("title")
    new_html += "<head>"
    if title is not None:
        new_html += title.prettify()
    new_html += __style
    new_html += "</head>"
    new_html += "<body>"

    url = "https://twitter.com/wonosatoru/status/{}".format(tweet_id)

    new_html += '<div class="main">'
    new_html += "<a href={}>{}</a>".format(url, url)

    main = soup.find(attrs={"role":"main"})
    if main is not None:
        new_html += main.prettify()

    new_html += "</div>"
    new_html += "</body>"
    new_html += "</html>"

    return new_html

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0')

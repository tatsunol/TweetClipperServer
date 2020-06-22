# -*- coding: utf-
from bs4 import BeautifulSoup

__style = """
<style>
    * {
        padding: 0;
        margin: 0;
    }
"""
_t = """
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

def filter(input_html, direct=False):

    direct = True

    if direct:
        return input_html

    soup = BeautifulSoup(input_html, "html.parser")

    # prompts = soup.find_all("toast_client_prompt")
    # for prompt in prompts:
        # prompt.extract()

    # ========

    new_html = "<html lang='ja'>"
    title = soup.find("title")
    new_html += "<head>"
    if title is not None:
        new_html += title.prettify()
    # new_html += __style
    new_html += "</head>"
    new_html += "<body>"

    # url = "https://twitter.com/i/status/{}".format(tweet_id)
    url = "https://twitter.com/i/status/XXX"

    new_html += '<div class="main">'
    new_html += "<a href={}>{}</a>".format(url, url)

    main_tweet = soup.find(class_="main-tweet")

    if main_tweet is not None:
        print(len(main_tweet))
        new_html += main_tweet.prettify()

    new_html += "</div>"
    new_html += "</body>"
    new_html += "</html>"

    return new_html


    return input_html


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


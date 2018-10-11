# -*- coding: utf-8
import requests
import json
from bs4 import BeautifulSoup


tweet_url = "https://twitter.com/i/status/{}".format(tweet_id)

response = requests.get(tweet_url)
soup = BeautifulSoup(response.text, "html.parser")

buttons = soup.find_all("button")
for button in buttons:
    button.extract()

links = soup.find_all("a")
for link in links:
    link.unwrap()

soup.find(attrs={"class":"stream-footer"}).extract()

new_html = "<html lang='ja'>"
new_html += soup.head.prettify()
new_html += "<body>"

new_html += soup.find(attrs={"role":"main"}).prettify()

new_html += "</body>"
new_html += "</html>"

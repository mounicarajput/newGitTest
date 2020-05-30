import numpy as np
import pandas as pd
import requests
import bs4
import re
import datetime as datetime

import lxml.etree as xml
from requests import get
from bs4 import BeautifulSoup
from flask import Flask,request,jsonify

app = Flask(__name__)

#data = []


# main url
@app.route("/", methods=['POST', 'GET'])
def home_view():
    data = []
    if request.method == "POST":
        try:
            url = request.get_json(silent=True)
            link = url['urls']
            for i in link:
                r = requests.get(i)
                r.encoding = 'utf-8'
                html_content = r.text
                html_soup = BeautifulSoup(html_content, 'html.parser')

                para = html_soup.find_all('p',"")
                topic= html_soup.find('h1').text
                time = html_soup.find_all('a')

                contest=html_tag_remover(str(para))
                top=html_tag_remover(str(topic))
                year=html_tag_remover(str(time))

                array = re.findall(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}, \d{4}|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1})', year)
                #md = date(year)
                #print(year)
                ts = array[0][0]


                query={"URLS" : i,"Contents":contest,"Header" : top,"published" :ts,}
                data.append(query)
        except Exception as e:
            return jsonify(error="Received wrong json structure or can be other reasons")

        return jsonify(success=true)
    else:
        return jsonify(error="get method not allowed")


def html_tag_remover(texts):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', texts)
    return cleantext

def date(d):
  pattern = r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{2})'
  find_d=re.findall(pattern, d)
  return(find_d)

def convert(date_time):
    format = '%b %d %Y'
    datetime_str = datetime.datetime.strptime(date_time, format)
    return datetime_str


if __name__ == "__main__":
    app.run(debug=True)

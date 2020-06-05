import firebase_admin
from firebase_admin import credentials, firestore, db
import PyPDF2
import re
from datetime import date
import flask
from flask import jsonify, Flask

import requests

cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)


@app.route('/covid19/srilanka/districts', methods=['POST'])
def myfunc(chunk_size=None):
    distDict = {
        "Ampara": 0,
        "Anuradhapura": 0,
        "Badulla": 0,
        "Batticaloa": 0,
        "Colombo": 0,
        "Galle": 0,
        "Gampaha": 0,
        "Hambantota": 0,
        "Jaffna": 0,
        "Kalutara": 0,
        "Kandy": 0,
        "Kegalle": 0,
        "Kilinochchi": 0,
        "Kurunegala": 0,
        "Mannar": 0,
        "Matale": 0,
        "Matara": 0,
        "Monaragala": 0,
        "Mullaittivu": 0,
        "Nuwara Eliya": 0,
        "Polonnaruwa": 0,
        "Puttalam": 0,
        "Rathnapura": 0,
        "Trincomalee": 0,
        "Vavuniya": 0
    }
    today = date.today()
    # month = today.strftime("%m")
    # day= today.strftime("%d")
    month = "06"
    day = "04"

    url = 'http://www.epid.gov.lk/web/images/pdf/corona_virus_report/sitrep-sl-en-' + day + '-' + month + '_10.pdf'
    r = requests.get(url, stream=True)

    with open("dailyStats.pdf", "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):

            # writing one chunk at a time to pdf file
            if chunk:
                pdf.write(chunk)


    pdfFile = "dailyStats.pdf"
    pdfRead = PyPDF2.PdfFileReader(pdfFile)
    page = pdfRead.getPage(1)
    pageContent = page.extractText()
    # print(pageContent)

    l = []
    arr = ""
    obj = {}

    for x in range(0, len(pageContent)):
        if pageContent[x] == '\n':
            if (arr == " " or arr == "  " or arr == ""):
                continue
            arr = arr.replace(" ", "")
            l.append(arr)
            arr = ""
            continue

        arr = arr + pageContent[x]

    # print(l)
    for x in range(0, len(l)):
        str = l[x]
        if len(str) > 0 and str[0].isalpha():
            str = str.capitalize()

        if str in distDict:
            y = x
            stat = ""
            while (l[y + 1][0].isdigit()):
                stat = stat + l[y + 1]
                y = y + 1
            distDict[str] = int(stat)
    print(distDict)
    return jsonify(distDict), 200


if __name__ == '__main__':
    app.run()

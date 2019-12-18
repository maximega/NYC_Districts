import json
import pymongo
import requests
from flask import Flask, request, render_template, redirect, url_for, session, json


app = Flask(__name__)

@app.route('/result', methods=['GET'])
def result():

    district = request.args['district'].lower().split()[0:-1]

    if 'Neighborhood' in district:
        district = 'nta'
    elif len(district) > 1:
        district = district[1]

    data = get_boundry(district)
        
    res = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return res

def get_boundry(repo_name):
    client = pymongo.MongoClient()
    repo = client.district_repo
    data = repo[repo_name].find_one()

    for item in data:
        item['_id'] = ''

    return data

if __name__ == "__main__":
    app.run(port=8080, debug=True)

import json
import pymongo
import requests
from flask import Flask, request, render_template, redirect, url_for, session, json


app = Flask(__name__)

@app.route('/result', methods=['GET'])
def result():
    # ----------------- If no options are toggled -----------------
    if not request.args['districts']:
        res = app.response_class(
            response=None,
            status=200,
            mimetype='application/json'
        )
        return res
        
    # ----------------- SIf at least one district is toggled -----------------
    districts = request.args['districts'].lower().split('&')
    for d in districts:
        d.split()[0:-1]

    d_len = len(districts)
    data = [None] * d_len

    for i in range(d_len):
        data[i] = get_boundry(districts[i])
        
    res = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return res

#---------- Retrieve district geo info ---------------
def get_boundry(repo_name):

    if 'neighborhood' in repo_name:
        repo_name = 'nta'
    elif len(repo_name) > 1:
        repo_name = repo_name[1]

    client = pymongo.MongoClient()
    repo = client.district_repo
    data = repo[repo_name].find_one()

    for item in data:
        item['_id'] = ''

    return data

if __name__ == "__main__":
    app.run(port=8080, debug=True)

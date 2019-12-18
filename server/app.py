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

    # ----------------- If at least one district is toggled -----------------
    districts = request.args.getlist('districts')[0].lower().split(',')
    d_len = len(districts)

    for i in range(d_len):
        temp = districts[i].split()[0]
        if temp == 'neighborhood':  districts[i] = 'nta'
        elif temp == 'city':    districts[i] = 'council'
        elif temp == 'state':    districts[i] = 'assembly'
        elif temp == 'angela':    districts[i] = 'senate' #TODO: remeber to make this the same accross the board
        else:   districts[i] = temp

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
    client = pymongo.MongoClient()
    repo = client.district_repo
    #TODO: pymongo find our how to query data properly
    data = repo[repo_name].find_one()
    print(data)
    for item in data:
        item['_id'] = ''

    return data

if __name__ == "__main__":
    app.run(port=8080, debug=True)

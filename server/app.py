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

    json_ = {}
    for i in range(d_len):
        repo_name = "district." + districts[i]
        json_[districts[i]] = get_boundry(repo_name)

    res = app.response_class(
        response=json.dumps(json_),
        status=200,
        mimetype='application/json'
    )
    return res

#---------- Retrieve district geo info ---------------
def get_boundry(repo_name):
    client = pymongo.MongoClient()
    repo = client.district_repo
    boundries = repo[repo_name]

    district_temp = {}
    #TODO: create uniform labeling for every data set 
    for boundry in boundries.find():
        district_temp['_id'] = ''
        district_temp['the_geom'] = boundry['the_geom']

    return district_temp

if __name__ == "__main__":
    app.run(port=8080, debug=True)

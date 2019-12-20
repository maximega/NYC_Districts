import json
import pymongo
import urllib.request
import uuid

class Police():
    reads = []
    writes = ['district.police']

    @staticmethod
    def execute(trial = False):
        repo_name = Police.writes[0]
        # ----------------- Set up the database connection -----------------
        client = pymongo.MongoClient()
        repo = client.district_repo
        
        #------------------ Data retrieval ---------------------
        url = 'https://data.cityofnewyork.us/resource/kmub-vria.json'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read()
        json_response = json.loads(content)
        
        insert_many_arr = []
        for item in json_response:
            insert_many_arr.append({
                'the_geom': item['the_geom'],
                'label': item['precinct']
            })

        #----------------- Data insertion into Mongodb ------------------
        repo.drop_collection(repo_name)
        repo.create_collection(repo_name)
        repo[repo_name].insert_many(insert_many_arr)
        
        repo.logout()
        print(repo_name, "completed")
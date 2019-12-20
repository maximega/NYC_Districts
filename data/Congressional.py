import json
import pymongo
import urllib.request
import uuid

class Congressional():
    reads = []
    writes = ['district.congressional']

    @staticmethod
    def execute(trial = False):
        repo_name = Congressional.writes[0]
        # ----------------- Set up the database connection -----------------
        client = pymongo.MongoClient()
        repo = client.district_repo
        
        #------------------ Data retrieval ---------------------
        url = 'https://data.cityofnewyork.us/resource/miue-f5mc.json'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read()
        json_response = json.loads(content)
        
        insert_many_arr = []
        for item in json_response:
            insert_many_arr.append({
                'the_geom': item['the_geom'],
                'label': item['cong_dist']
            })

        #----------------- Data insertion into Mongodb ------------------
        repo.drop_collection(repo_name)
        repo.create_collection(repo_name)
        repo[repo_name].insert_many(insert_many_arr)
        
        repo.logout()
        print(repo_name, "completed")



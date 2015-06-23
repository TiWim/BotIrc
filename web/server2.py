from collections import OrderedDict
import json
from pymongo import MongoClient

from flask import Flask, make_response

app = Flask(__name__)

#####################################################
#                 INITIALISATION                    #
#####################################################


# Mongo
client = MongoClient()
db = client.ModVote
polls_collection = db.polls


#####################################################
#                   GET METHODS                     #
#####################################################


@app.route('/0x90r00t/votes/')
def get_stats():
    polls = list(polls_collection.find({}))

    # Detailed information
    response = make_response(json.dumps(polls))
    response.mimetype = "application/json"
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5668, debug=True)

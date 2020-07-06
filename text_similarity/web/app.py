from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import bcrypt
from pymongo import MongoClient
import spacy

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")

db = client.SimilarityDB
users = db["users"]

def UserExist(username):
    if users.find({"username":username}).count() == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status": 301,
                "message": "Username already exists"
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({"username":username,"password":hashed_pw, "tokens": 6})
        retJson = {
            "Status": 200,
            "message": "Registration successful"
        }
        return jsonify(retJson)

def check_pw(username, password):
    if not UserExist:
        return False
    hashed_pw = users.find({"username":username})[0]["password"]
    if bcrypt.hashpw(password.encode("utf8"), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def count_tokens(username):
    tokens = users.find({"username":username})[0]["tokens"]
    return tokens

class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            retJson = {
                "status": 301,
                "message": "Username already exists"
            }
            return jsonify(retJson)

        correct_pw = check_pw(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "message": " invalid password"
            }
            return jsonify(retJson)

        num_tokens = count_tokens(username)

        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "message": "out of tokens, please refill"
            }
            return jsonify(retJson)

        #calculate edit distance
        nlp = spacy.load("en_core_web_sm")
        text1 = nlp(text1)
        text2 = nlp(text2)
        ratio = text1.similarity(text2)

        retJson = {
            "status": 200,
            "similarity": ratio,
            "message": "similarity calculated successfully"
        }

        currrent_tokens = count_tokens(username)
        users.update({"username":username}, {"$set":{"tokens":currrent_tokens-1}})

        return jsonify(retJson)

class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["amount"]

        if not UserExist(username):
            retJson = {"status": 301, "message": "User does not exist"}
            return jsonify(retJson)

        correct_pw = "1234"
        if correct_pw != password:
            retJson = {
                "status": 304,
                "message": " invalid admin password"
            }
            return jsonify(retJson)

        currrent_tokens = count_tokens(username)
        users.update({"username":username},
                    {"$set":{"tokens":refill_amount + currrent_tokens}})

        retJson = {
            "status": 200,
            "message": " Refill successful"
        }
        return jsonify(retJson)


api.add_resource(Register, "/register")
api.add_resource(Detect, "/detect")
api.add_resource(Refill, "/refill")

if __name__ == "__main__":
    app.run(host = '0.0.0.0')

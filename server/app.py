from flask import request
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from http import HTTPStatus
from bson import ObjectId
from dotenv import load_dotenv
import os

from sastquatch_library.server import *


load_dotenv()

app = Flask(__name__)
CORS(app)

mongo = PyMongo(app, uri=os.getenv("MONGO_URI"))
user_collection = mongo.db.get_collection(os.getenv("USER_COLLECTION"))
repo_collection = mongo.db.get_collection(os.getenv("REPO_COLLECTION"))
bugs_collection = mongo.db.get_collection(os.getenv("BUGS_COLLECTION"))


"""
GET /
"""
@app.route("/")
def index():
    return create_response(
        success=True,
        message="Hello World!",
        status=HTTPStatus.OK
    )


"""
POST /login
"""
@app.route("/login", methods=["POST"])
def login():
    try:
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")

        # clean data
        username = username.strip()
        password = hash_password(password.strip())

        user = user_collection.find_one({
            "username": username
        })

        if not user:
            return create_response(
                success=False,
                message=f"User With Username: {username} Doesn't Exist",
                status=HTTPStatus.OK
            )

        if user["password"] == password:
            token = create_token({"username": username})
            return create_response(
                success=True,
                message="Successfully Logged In",
                data={
                    "token": token
                },
                status=HTTPStatus.OK
            )
    except Exception as e:
        print(e)
        return create_response(
            success=False,
            message=f"Error While Logging In",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
POST /register
"""
@app.route("/register", methods=["POST"])
def register():
    try:
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")

        # hash the password
        password = hash_password(password)

        # check if already exist or not
        user = user_collection.find_one({
            "username": username
        })
        if user:
            return create_response(
                success=False,
                message="User Already Exists",
                status=HTTPStatus.OK
            )

        user = user_collection.insert_one({
            "username": username,
            "password": password,
            "verified": False,
            "admin": False
        })
        user_id = str(user.inserted_id)

        return create_response(
            success=True,
            message="Successfully Registered a User",
            data={
                "user_id": user_id
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)
        return create_response(
            success=False,
            message="Error While Registering User",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
GET /repositories
"""
@app.route("/repositories", methods=["GET"])
def get_repos():
    try:
        repos = repo_collection.find({})
        repos = list(repos)

        return create_response(
            success=True,
            message="Successfully Queried All Repositories",
            data={
                "repos": repos
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)
        return create_response(
            success=False,
            message="Error While Quering Repos",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
GET /repositories/PLATFORM
"""
@app.route("/repositories/<platform>", methods=["GET"])
def get_repos_platform(platform: str):
    try:
        platform = platform.upper()
        repos = repo_collection.find({
            "platform": platform
        })
        repos = list(repos)

        return create_response(
            success=True,
            message="Successfully Queried All Repositories Platform",
            data={
                "repos": repos
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)
        return create_response(
            success=False,
            message="Error While Quering Repos",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
GET /repositories/PLATFORM/OWNER
"""
@app.route("/repositories/<platform>/<owner>", methods=["GET"])
def get_repos_platform_owner(platform: str, owner: str):
    try:
        platform = platform.upper()
        owner = decode_alias(owner.lower())
        
        repos = repo_collection.find({
            "platform": platform,
            "owner": owner
        })
        repos = list(repos)

        return create_response(
            success=True,
            message="Successfully Queried All Repositories Platform Owner",
            data={
                "repos": repos
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)
        return create_response(
            success=False,
            message="Error While Quering Repos",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
GET /repositories/PLATFORM/OWNER/REPO
"""
@app.route("/repositories/<platform>/<owner>/<repo>", methods=["GET"])
def get_repos_platform_owner_repo(platform: str, owner: str, repo: str):
    try:
        platform = platform.upper()
        owner = decode_alias(owner.lower())
        repo = decode_alias(repo.lower())
        
        repos = repo_collection.find({
            "platform": platform,
            "owner": owner,
            "repo": repo
        })

        bugs = []
        for repo in repos:
            new_bugs = bugs_collection.find({
                "repo_id": ObjectId(repo["_id"])
            })
            bugs.extend(list(new_bugs))

        return create_response(
            success=True,
            message="Successfully Queried All Repositories Platform Owner Repo",
            data={
                "bugs": bugs
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)
        return create_response(
            success=False,
            message="Error While Quering Repos",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


# entrypoint
if __name__ == "__main__": 
 
    port = os.getenv("FLASK_PORT") or 3000
    debug = (os.getenv("FLASK_DEBUG").lower() == "true")

    app.run(port=port, debug=debug)

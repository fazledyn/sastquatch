from flask import request
from flask import Flask
from http import HTTPStatus
from bson import ObjectId
import os

from sastquatch_library.server import *
from sastquatch_library.database import *


app = Flask(__name__)


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
GET /packages
"""
@app.route("/packages", methods=["GET"])
def get_packages():
    try:
        packages = package_collection.find({})
        packages = list(packages)

        return create_response(
            success=True,
            message="Successfully Queried All Packages",
            data={
                "packages": packages
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)

        return create_response(
            success=False,
            message="Error While Quering Packages",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
GET /packages/ECOSYSTEM
"""
@app.route("/packages/<ecosystem>", methods=["GET"])
def get_packages_ecosystem(ecosystem: str):
    try:
        ecosystem = ecosystem.lower()
        packages = package_collection.find({
            "ecosystem": ecosystem
        })
        packages = list(packages)

        return create_response(
            success=True,
            message="Successfully Queried All Ecosystem Packages",
            data={
                "packages": packages
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)

        return create_response(
            success=False,
            message="Error While Quering Packages",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
GET /packages/ECOSYSTEM/ALIAS
"""
@app.route("/packages/<ecosystem>/<alias>", methods=["GET"])
def get_packages_ecosystem_alias(ecosystem: str, alias: str):
    try:
        ecosystem = ecosystem.lower()
        alias = decode_alias(alias)
        packages = package_collection.find({
            "ecosystem": ecosystem,
            "alias": alias
        })
        packages = list(packages)

        return create_response(
            success=True,
            message="Successfully Queried All Ecosystem Alias Packages",
            data={
                "packages": packages
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)

        return create_response(
            success=False,
            message="Error While Quering Packages",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
GET /packages/ECOSYSTEM/ALIAS/VERSION
"""
@app.route("/packages/<ecosystem>/<alias>/<version>", methods=["GET"])
def get_packages_ecosystem_alias_version(ecosystem: str, alias: str, version: str):
    try:
        ecosystem = ecosystem.lower()
        alias = decode_alias(alias)
        version = version.lower()
        packages = []

        __packages = package_collection.find({
            "ecosystem": ecosystem,
            "alias": alias,
            "version": version
        })

        for package in list(__packages):
            package_id = package["_id"]
            package_alias = package["alias"]
            package_version = package["version"]
            package_ecosystem = package["ecosystem"]
            __problems = problem_collection.find({
                "package_id": package_id
            })
            package_problems = list(__problems)
            packages.append({
                "package_id": str(package_id),
                "package_alias": package_alias,
                "package_ecosystem": package_ecosystem,
                "package_version": package_version,
                "package_problems": package_problems
            })

        return create_response(
            success=True,
            message="Successfully Queried All Ecosystem Alias Version Packages",
            data={
                "packages": packages
            },
            status=HTTPStatus.OK
        )
    except Exception as e:
        print(e)

        return create_response(
            success=False,
            message="Error While Quering Packages",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )



"""
GET /packages/id/PACKAGE_ID
"""
@app.route("/packages/id/<package_id>", methods=["GET"])
def get_package(package_id: str):
    try:
        package = package_collection.find_one({
            "_id": ObjectId(package_id)
        })
        return create_response(
            success=True,
            message="Successfully Queried Package",
            data={
                "package": package
            }
        )
    except Exception as e:
        print(e)

        return create_response(
            success=False,
            message=f"Error While Querying Package id: {package_id}",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


"""
POST /packages
"""
@app.route("/packages", methods=["POST"])
def post_package():
    try:
        package_data = request.get_json()
        package = package_collection.insert_one(package_data)
        package_id = str(package.inserted_id)
        return create_response(
            success=True,
            message="Package Created Successfully",
            data={
                "package_id": package_id
            },
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(e)

        return create_response(
            success=False,
            message="Error While Creating a Package",
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )


# entrypoint
if __name__ == "__main__":

    from dotenv import load_dotenv
    load_dotenv()
    load_database()
 
    port = os.getenv("FLASK_PORT") or 3000
    debug = (os.getenv("FLASK_DEBUG").lower() == "true")

    app.run(port=port, debug=debug)

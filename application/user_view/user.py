from flask import Blueprint, render_template, jsonify, request
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from application.extensions.extensions import *
from application.settings.settings import *
from application.settings.setup import app
from application.database.user.user_db import User, db
from sqlalchemy import or_, desc, and_
from datetime import datetime
from datetime import date
from flask import session

user = Blueprint("user", __name__)
guard.init_app(app, User)

class User_schema(ma.Schema):
    class Meta:
        fields = ("id", "firstname", "lastname", "about", "email", "username", "hashed_password",
                  "roles", "city", "country", "address", "phone", "created_date",
                  "account_status", "state", "transaction_pin", "photo")

user_schema = User_schema(many=True)

@user.route("/register_quick", methods=["POST"])
def register_quick():
    try:
        firstname = request.json["firstname"]
        username = request.json["username"]
        password = request.json["password"]
        lastname = request.json["lastname"]
        about = request.json["about"]
        country = request.json["country"]
        city = request.json["city"]
        email = request.json["email"]
        address = request.json["address"]
        role = request.json["role"]
        phone = request.json["phone"]
        
        hashed_password = guard.hash_password(password)
        
        owner = User(firstname=firstname, lastname=lastname, about=about, country=country,
                     city=city, phone=phone, username=username, hashed_password=hashed_password, 
                     roles=role, address=address, email=email, created_date=datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        db.session.add(owner)
        db.session.commit()
        resp = jsonify("success")
        resp.status_code = 200
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user.route("/register", methods=["POST"])
def register():
    try:
        firstname = request.json["firstname"]
        username = request.json["username"]
        password = request.json["password"]
        lastname = request.json["lastname"]
        email = request.json["email"]
        role = request.json["role"]

        hashed_password = guard.hash_password(password)
        
        owner = User(firstname=firstname, lastname=lastname, username=username, hashed_password=hashed_password, 
                     roles=role, email=email, created_date=datetime.now().strftime('%Y-%m-%d %H:%M'))

        db.session.add(owner)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 200
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user.route('/get_signin_client', methods=['GET', 'POST'])
def get_signin_client():
    try:
        req = request.get_json(force=True)
        username = req.get("username", None)
        password = req.get("password", None)
        
        user = guard.authenticate(username, password)
        ret = {"id_token": guard.encode_jwt_token(user)}

        return ret, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user.route("/get_info", methods=['GET'])
@flask_praetorian.auth_required
def get_info():
    try:
        info = db.session.query(User).filter_by(id=flask_praetorian.current_user().id).all()
        results = user_schema.dump(info)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user.route("/get_users", methods=['GET'])
@flask_praetorian.auth_required
def get_users():
    try:
        info = db.session.query(User).all()
        results = user_schema.dump(info)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user.route("/delete_user/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_user(id):
    try:
        info = db.session.query(User).filter_by(id=id).first()
        if not info:
            return jsonify({"error": "User not found"}), 404
        
        db.session.delete(info)
        db.session.commit()
        res = jsonify("success")
        res.status_code = 200
        return res
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user.route("/get_user_details/<id>", methods=['GET'])
@flask_praetorian.auth_required
def get_user_details(id):
    try:
        info = db.session.query(User).filter_by(id=id).all()
        results = user_schema.dump(info)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user.route("/update_user_profile", methods=['PUT'])
@flask_praetorian.auth_required
def update_user_profile():
    try:
        id = request.json["id"]
        password = request.json["password"]

        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.firstname = request.json["firstname"]
        user.about = request.json["about"]
        user.lastname = request.json["lastname"]
        user.phone = request.json["phone"]
        user.username = request.json["username"]
        user.country = request.json["country"]
        user.city = request.json["city"]
        user.address = request.json["address"]
        user.email = request.json["email"]
        user.roles = request.json["role"]
        user.hashed_password = guard.hash_password(password)

        db.session.commit()
        res = jsonify("success")
        res.status_code = 200
        return res
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

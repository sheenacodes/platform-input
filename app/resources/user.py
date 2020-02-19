
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
from app import swagger
from flasgger.utils import swag_from
from app.models import PlatformUser
from app import db

users = {}

def validate_post_user(request):
        validation_status = True
        result = {}
        try:
            data = request.json
            if not ('username' in data and 'email' in data and 'password' in data):
                result = {'status' : "failure",
                'data': "Insufficient Data: Username, email, password are required"}
                validation_status = False

        except Exception as e:
            print(e)
            result = {'status' : "failure",
            'data': "Invalid Input, Check JSON schema"}
            validation_status = False
        
        response = jsonify(result)
        response.status_code = 400

        return validation_status, response

def db_error_response():
    result = {'status' : "failure",
            'data': "Database error"}
    response = jsonify(result)
    response.status_code = 400
    return response

class User(Resource):

    @swag_from('user.yml')
    def post(self):
        """
        Post new user
        """
        validation_status, response = validate_post_user(request)

        if not validation_status:
            return response
        
        data = request.json
        print(data)
        
        try:
            user = PlatformUser.query.filter_by(username=data['username']).first()
        except Exception as e:
            print(e)
            return db_error_response()
        
        print(user)
        if user is not None :            
            result = {'status' : "failure",
            'data': "Username exists. Choose another"}
            return jsonify(result)
        
        try:
            email = PlatformUser.query.filter_by(email=data['email']).first()
        except Exception as e:
            print(e)
            return db_error_response()

        if email is not None :
            result = {'status' : "failure",
            '   data': "email exists. Choose another"}
            return jsonify(result)

        try:
            user = PlatformUser(username=data['username'], email=data['email'], password=data['password']) #,created_at = dt.now())
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()

            del data['password']
            result = {'status' : "success",
                      'data': data}
            response = jsonify(result)
            return jsonify(result)
        
        except Exception as e:
            print(e)

            return db_error_response()

from flask import Flask,request
from flask_restful import Resource, Api
from app import app
from app.resources.user import User
from app.resources.observations import Observation

api = Api(app)
api.add_resource(User, '/user')
api.add_resource(Observation, '/observation')


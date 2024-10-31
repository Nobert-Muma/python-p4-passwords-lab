#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user=User.query.filter(User.id==session.get('user_id')).first()
        if user:
            return user.to_dict(), 200
        else:
            return "", 204

class Login(Resource):
    def post(self,):
        user=User.query.filter(User.username==request.get_json()['username']).first()
        session['user_id']=user.id
        return user.to_dict()

class Logout(Resource):
    def delete(self):
        session['user_id']=None
        return {'message': '204: No Content'}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
if __name__ == '__main__':
    app.run(port=5555, debug=True)

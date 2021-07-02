from flask import Flask, request, jsonify
from flask.globals import session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import desc
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_jwt_extended import set_access_cookies
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,  check_password_hash
from functools import wraps
from Queries.dbQueries import get_domains, get_single_domain, get_all, get_basic_metrics, get_na

from flask_jwt_extended import JWTManager


app = Flask(__name__)
# CORS(app,resources={r"/*": {"origins": "*"}})
#CORS(app,origins=["http://127.0.0.1:3000/"], headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'])

CORS(app)

api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:$Hockeylax2@localhost/website_metrics'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['JWT_SECRET_KEY'] = 'cf41db4341bf4561a61ab6a2058d0f3f'
# app.config["JWT_COOKIE_SECURE"] = False
# app.config['JWT_COOKIE_SAMESITE'] = 'None'
# app.config['JWT_COOKIE_CSRF_PROTECT'] = True
# JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# jwt = JWTManager(app)
# app.config['CORS_HEADERS'] = ['Content-Type']
# app.config['SESSION_COOKIE_SECURE'] = True
# print(app.config['SESSION_COOKIE_SECURE'])



# db = SQLAlchemy(app)
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help='')
user_post_args.add_argument("password", type=str, help='')
domain_field = {
    'domains':fields.String
}

user_field = {
    'id':fields.Integer,
    'username':fields.String,
    'password':fields.String,
    'logged_in':fields.Boolean

}

# class NewUser(Resource):
#     def post(self):
#         data = user_post_args.parse_args(strict=True)
#         hashed_password = generate_password_hash(data['password'])
#         new_user(data['username'], hashed_password)
#         return {'message': 'User created'}


# class UserLogin(Resource):
#     # @cross_origin(origin='*',headers=['Content-Type','Authorization','Access-Control-Allow-Origin'])
#     def post(self):
#         data = user_post_args.parse_args(strict=True)
#         print(data)
#         db_password = get_user(data['username'])
#         if db_password == None:
#             return {'message':'Something went wrong'}

#         if check_password_hash(db_password, data['password']):
#             response = jsonify({"message":"welcome"})
#             access_token = create_access_token(identity = data['username'])
#             set_access_cookies(response, access_token)
#             return {'message': 'logged in', 'access_token': access_token}
#         else: 
#             return {'message': 'Something went wrong'}

class GetAll(Resource):
    def get(self):
        request = get_all()
        # resp = {'pagespeed': request[0], 'gtmetrix': request[1]}
        # print(type(request))
        return request

class GetDomains(Resource):
    def get(self):
        req = get_domains()
        # print(req)
        return req

class GetSingleDomain(Resource):
    def get(self,domain):
        # print(domain)
        domain = domain.replace('~','.')
        print(f"https://{domain}")

        req = get_single_domain(f"https://{domain}")
        # print(req)
        if req == "Error":
            return "error"
        pagespeed_dict = req[0]
        gtmetrix_dict = req[1]
        return {'domain': f'https://{domain}','pagespeed':pagespeed_dict, 'gtmetrix':gtmetrix_dict}

# class GetCount(Resource):
#     def get(self):
#         count = get_entries_count()
#         return count

class GetStats(Resource):
    def get(self):
        stats = get_basic_metrics()
        # print(stats)
        return jsonify(stats)

class GetNa(Resource):
    def get(self):
        na = get_na()
        return jsonify(na)

# api.add_resource(UserLogin, '/login')
# api.add_resource(NewUser, '/register')
api.add_resource(GetNa, '/api/na')
api.add_resource(GetStats, '/api/stats')
# api.add_resource(GetCount, '/get/count')
api.add_resource(GetDomains, '/api/domains')
api.add_resource(GetAll, '/api/alldata')
api.add_resource(GetSingleDomain,'/api/single/<string:domain>')


if __name__ == "__main__":
    app.run(debug=True)
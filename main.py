from flask import Flask, request, jsonify, make_response
from flask.globals import session
from flask_jwt_extended.utils import get_csrf_token, get_jwt
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import desc
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_csrf_token
from flask_jwt_extended import set_access_cookies
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash,  check_password_hash
from functools import wraps
from Queries.dbQueries import get_domains, get_single_domain, get_all, get_basic_metrics, get_na, add_domain
# from logging import FileHandler, WARNING

from flask_jwt_extended import JWTManager

app = Flask(__name__)
# CORS(app,resources={r"/*": {"origins": "*"}})
#CORS(app,origins=["http://127.0.0.1:3000/"], headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'])

CORS(app,supports_credentials=True)

api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:$Hockeylax2@localhost/website_metrics'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# file_handler = FileHandler('errorlog.txt')
# file_handler.setLevel(WARNING)
# app.logger.addHandler(file_handler)

app.config['JWT_SECRET_KEY'] = 'cf41db4341bf4561a61ab6a2058d0f3f'
app.config["JWT_COOKIE_SECURE"] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=23)
jwt = JWTManager(app)
# app.config['CORS_HEADERS'] = ['Content-Type']
# app.config['SESSION_COOKIE_SECURE'] = True
# print(app.config['SESSION_COOKIE_SECURE'])



# db = SQLAlchemy(app)
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("user_uid", type=str, help='')

domain_post_args = reqparse.RequestParser()
domain_post_args.add_argument("domain", type=str, help='')
domain_post_args.add_argument("server", type=str, help='')


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


class User(Resource):
    def post(self):
        data = user_post_args.parse_args(strict=True)
        # return data
        
        access_token = create_access_token(identity = data['user_uid'])
        response = jsonify({'message': 'success'})
        # res = make_response({'message': 'success'})
        # res.set_cookie('access_token',access_token, domain='127.0.0.1',samesite='None', secure=True)
        # res.set_cookie('access_token','', expires=0)
        # res.delete_cookie('access_token',access_token)
        set_access_cookies(response, access_token)
        return response


class GetAll(Resource):
    def get(self):
        request = get_all()
        # resp = {'pagespeed': request[0], 'gtmetrix': request[1]}
        # print(type(request))
        return request

class GetDomains(Resource):
    @jwt_required(locations=['cookies'])
    def get(self):
        user = get_jwt_identity()
        # print(user)
        header = request.headers.get('Ran-Header')
        print(header)
        if user and header:
            req = get_domains()
        else:
            return 'Error'
        # print(req)
        return req

class GetSingleDomain(Resource):
    @jwt_required(locations=['cookies'])
    def get(self,domain):
        user = get_jwt_identity()
        header = request.headers.get('Ran-Header')
        if user and header:
            domain = domain.replace('~','.')
            req = get_single_domain(f"https://{domain}")
            if req == "Error":
                return "error"
            pagespeed_dict = req[0]
            gtmetrix_dict = req[1]
        else:
            return 'error'
        return {'domain': f'https://{domain}','pagespeed':pagespeed_dict, 'gtmetrix':gtmetrix_dict}

# class GetCount(Resource):
#     def get(self):
#         count = get_entries_count()
#         return count

class GetStats(Resource):
    @jwt_required(locations=['cookies'])
    def get(self):
        user = get_jwt_identity()
        header = request.headers.get('Ran-Header')
        if user and header:
            stats = get_basic_metrics()
        else:
            return "error"
        # print(stats)
        return jsonify(stats)

class GetNa(Resource):
    def get(self):
        na = get_na()
        return jsonify(na)

class AddDomain(Resource):
    @jwt_required()
    # gets token and csrf to send in header for post request
    def get(self):
        user = get_jwt_identity()
        header = request.headers.get('Ran-Header')
        # print(header)
        csrf_token = get_jwt()
        csrf = csrf_token['csrf']
        # print(csrf)
        if user and header:
            csrf_token = get_jwt()
            csrf = csrf_token['csrf']
        else: 
            return 'error'
        return {'csrf': csrf}

    @jwt_required()
    def post(self):
        data = domain_post_args.parse_args(strict=True)
        add_domain(data['domain'], data['server'])
        return {'msg':'added'}


# api.add_resource(UserLogin, '/login')
api.add_resource(User, '/api/user')
api.add_resource(AddDomain, '/api/adddomain')
# api.add_resource(NewUser, '/register')
api.add_resource(GetNa, '/api/na')
api.add_resource(GetStats, '/api/stats')
# api.add_resource(GetCount, '/get/count')
api.add_resource(GetDomains, '/api/domains')
api.add_resource(GetAll, '/api/alldata')
api.add_resource(GetSingleDomain,'/api/single/<string:domain>')


if __name__ == "__main__":
    app.run(debug=True)
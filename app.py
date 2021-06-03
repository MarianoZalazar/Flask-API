from flask import Flask, request
from mongoengine import ValidationError, NotUniqueError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

import misc.pswd_manager as pswd_manager
import misc.email as email
from misc.response import get_json

from apiproject import EMAIL, PSWD_EMAIL, PORT, jwt, app

from models.product import Product
from models.user import User

from messages.error_messages import error_message_helper

@app.route('/')
def home():
    return ""

#######################################################


#User Routes

@app.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    try:
        User.register(request_data['email'], request_data['username'], pswd_manager.generate_password(request_data['password']))
        response = get_json('', 201)
    except ValidationError as exc:
        response = get_json(error_message_helper(exc.message), 400)
    except NotUniqueError as exc:
        response = get_json({"msg": "Username/Email already registered"}, 409)
    return response

#######################################################

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    try:
        user = User.authenticate(username, password)
        access_token = create_access_token(user.username)
        response = get_json({"access_token": access_token}, 202)
    except ValidationError as exc:
        response = get_json(error_message_helper(exc.message), 401)
    return response

#######################################################

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        user_email = email.validate_token(token)
    except:
        response = get_json({'Error': 'The confirmation link is invalid or has expired.'}, 401)
        return response
    user = User.get_by_email(user_email)
    if user.confirmed:
        response = get_json({'Ok': 'Account Confirmed, return to login'}, 200)
    else:
        user.confirm_user()
        response = get_json({'Ok': 'Account Confirmed, return to login'}, 200)
    return response

#######################################################
              
@app.route('/users')
def get_users():
    return_value = User.get_all_users()
    return get_json(return_value, 200)

#######################################################

@app.route('/users/<string:username>')
def get_user_by_username(username):
    return_value = User.get_by_username(username)
    return get_json(return_value, 200)

#######################################################



#Products Routes

@app.route('/products')
def get_all_products():
    return_value = {"Products": Product.get()}
    return return_value

#######################################################

@app.route('/products/<int:product_id>')
def get_one_product(product_id):
    return_value = Product.get_one(product_id)
    return get_json(return_value, 200)


#######################################################

@app.route('/products/<string:username>')
def get_products_by_owner(username):
    return_value = Product.get_by_owner(username)
    return get_json(return_value, 200)


#####Need Permissions

@app.route('/products', methods=['POST'])
@jwt_required()
def add_one_product():
    request_data = request.get_json()
    try:
        product_posted = Product.post(request_data['name'], request_data['price'], request_data.get('description', None), request_data['quantity'], get_jwt_identity())
        response = get_json(product_posted, 201)
    except ValidationError as exc:
        response = get_json(error_message_helper(exc.message), 400)
    return response    

#######################################################
    
@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_one_product(product_id):
    request_data = request.get_json()
    try:
        Product.put(product_id, request_data['name'], request_data['price'], request_data.get('description', None), request_data['quantity'], get_jwt_identity())
        response = get_json('', 204)
    except ValidationError as exc:
        response = get_json(error_message_helper(exc.message), 400)
    return response    

#######################################################

@app.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_one_product(product_id):
    try:
        Product.delete_product(product_id, get_jwt_identity())
        response = get_json('', 204)
    except ValidationError as exc:
        response = get_json(error_message_helper(exc), 404)
    return response

#######################################################
#######################################################

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
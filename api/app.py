from flask import Flask, request
from mongoengine import ValidationError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from misc import pswd_manager, email, response
from apiproject import EMAIL, PSWD_EMAIL, jwt, app
from models import Product
from messages import error_messages
from models import User

#200 Ok Get
#201 Created Post
#204 No Content Put/Delete
#404 Not Found
#400 Bad Request

#app.config["JWT_SECRET_KEY"] = "super-secret"
#app.config["SECRET_KEY"] = "ultra-secret"
#app.config["SECURITY_PASSWORD_SALT"] = "mega-secret"
#app.config["MAIL_DEFAULT_SENDER"] = 'from@example.com'

@app.route('/')
def home():
    return "Hello Flask"

#######################################################

@app.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    try:
        User.register(request_data['email'], request_data['username'], pswd_manager.generate_password(request_data['password']))
        response = shared.get_json('', 201)
    except ValidationError as exc:
        response = shared.get_json(error.error_message_helper(exc.message), 400)
    return response

#######################################################

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    try:
        user = User.authenticate(username, password)
        access_token = create_access_token(user.username)
        response = shared.get_json({"access_token": access_token}, 202)
    except ValidationError as exc:
        response = shared.get_json(error.error_message_helper(exc.message), 401)
    return response

#######################################################

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = shared.validate_token(token)
    except:
        response = shared.get_json({'Error': 'The confirmation link is invalid or has expired.'}, 401)
        return response
    user = User.get_by_email(email)
    if user.confirmed:
        response = shared.get_json({'Ok': 'Account Confirmed, return to login'}, 200)
        pass
    else:
        user.confirm_user()
        response = shared.get_json({'Ok': 'Account Confirmed, return to login'}, 200)
    return response

#######################################################
              
@app.route('/products')
def get_all_products():
    return_value = {"Products": Product.get()}
    return return_value

#######################################################

@app.route('/products/<int:product_id>')
def get_one_product(product_id):
    return_value = Product.get_one(product_id)
    return shared.get_json(return_value, 200)


#######################################################

@app.route('/products/<string:username>')
def get_products_by_owner(username):
    return_value = Product.get_by_owner(username)
    return shared.get_json(return_value, 200)


#####Need Permissions

@app.route('/products', methods=['POST'])
@jwt_required()
def add_one_product():
    request_data = request.get_json()
    try:
        product_posted = Product.post(request_data['name'], request_data['price'], request_data.get('description', None), request_data['quantity'], get_jwt_identity())
        response = shared.get_json(product_posted, 201)
    except ValidationError as exc:
        response = shared.get_json(error.error_message_helper(exc.message), 400)
    return response    

#######################################################
    
@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_one_product(product_id):
    request_data = request.get_json()
    try:
        Product.put(product_id, request_data['name'], request_data['price'], request_data.get('description', None), request_data['quantity'], get_jwt_identity())
        response = shared.get_json('', 204)
    except ValidationError as exc:
        response = shared.get_json(error.error_message_helper(exc.message), 400)
    return response    

#######################################################

@app.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_one_product(product_id):
    try:
        Product.delete_product(product_id, get_jwt_identity())
        response = shared.get_json('', 204)
    except ValidationError as exc:
        response = shared.get_json(error.error_message_helper(exc), 404)
    return response

#######################################################
#######################################################

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
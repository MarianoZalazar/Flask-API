from models import Product
from misc import pswd_manager
from misc import email
import datetime
import mongoengine as mongo

class User(mongo.Document):
    user_id = mongo.SequenceField(primary_key=True)
    username = mongo.StringField(unique=True, required=True)
    email = mongo.EmailField(unique=True, required=True)
    password = mongo.StringField(required=True)
    products = mongo.ListField(null=True)
    created_at = mongo.DateTimeField()
    confirmed = mongo.BooleanField(null=False, default=False)
    confirmed_on = mongo.DateTimeField(null=True)
    
    def to_json(self):
        return {"user_id": self.user_id, 
                "username": self.username, 
                "created_at": self.created_at, 
                "products_user": Product.get_by_owner(self.username),
                "confirmed": self.confirmed,
                "confirmed_on": self.confirmed_on}
        
    @staticmethod
    def register(req_email, req_username, req_password):
        user = User(email=req_email, username=req_username, password=req_password, created_at=datetime.datetime.utcnow(), confirmed=False)
        email.send_mail_confirmation(user)
        user.save()
     
    @staticmethod
    def get_by_username(req_username):
         return User.objects(username=req_username).first()
    
    @staticmethod
    def authenticate(req_username, req_password):
        user = User.objects(username=req_username).first()
        req_password = pswd_manager.validate_password(user.password, req_password)
        if req_password or user.confirmed:
            return user
        else:
            raise Exception
    
    def confirm_user(self):
        self.update(confirmed=True)
        self.update(confirmed_on = datetime.datetime.now())
    
    @staticmethod
    def get_by_email(req_email):
        return User.objects(email=req_email).first()
    
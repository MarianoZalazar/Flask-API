import datetime
import mongoengine as mongo

class Product(mongo.Document):
    product_id = mongo.SequenceField(primary_key=True)
    name = mongo.StringField(required=True)
    price = mongo.FloatField(required=True)
    quantity = mongo.IntField(required=True)
    description = mongo.StringField(null=True, max_length=1000)
    created_at = mongo.DateTimeField()
    modified_at = mongo.DateTimeField()
    owner_name = mongo.StringField(required=True)
    
    def to_json(self):
        return {"product_id": self.product_id, "name": self.name, "price": self.price, "description": self.description, "quantity": self.quantity, "owner_name": self.owner_name, "created_at": self.created_at, "modified_at": self.modified_at}
    
    @staticmethod
    def get():
        return [product.to_json() for product in Product.objects()]
      
    @staticmethod
    def get_one(req_id):
        product_found = Product.objects(product_id=req_id).first()
        return product_found.to_json()
    
    @staticmethod
    def get_by_owner(req_owner):
        products_found = [product.to_json() for product in Product.objects(owner_name=req_owner)]
        return products_found
    
    @staticmethod
    def post(req_name, req_price, req_description, req_quantity, req_owner):
        new_product = Product(name=req_name, price=req_price, description=req_description,quantity=req_quantity, owner_name = req_owner, created_at=datetime.datetime.utcnow())
        new_product.save()
        return new_product.to_json()
    
    @staticmethod    
    def put(req_id, req_name, req_price, req_description, req_quantity, req_owner):
        product_to_update = Product.objects(product_id=req_id, owner_name=req_owner).first()
        product_to_update.update(name=req_name, price=req_price, description=req_description, quantity=req_quantity, modified_at=datetime.datetime.utcnow())
    
    @staticmethod    
    def delete_product(req_id, req_owner):
        product_to_delete = Product.objects(product_id=req_id, owner_name=req_owner).first()
        product_to_delete.delete()
        
    def __repr__(self):
        product_object = {"product_id": self.product_id,
                          "name": self.name,
                          "price": self.price,
                          "quantity": self.quantity,
                          "owner_name": self.owner_name
                        }
        return json.dump(product_object)

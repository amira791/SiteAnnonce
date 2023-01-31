from app import db, ma, app
from datetime import datetime, date

class Account(db.Model) :
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False, unique = False)
    phone = db.Column(db.String(100), nullable = False)
    wilaya = db.Column(db.String(100), nullable = False)
    photo = db.Column(db.String(100), nullable = False)
    posts = db.relationship('Post', backref='owned_user')
    likes = db.relationship('Like', backref='likes_owned_user')
    
    
    def __init__(self, username, email, password, phone, wilaya, photo):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.wilaya = wilaya
        self.photo = photo
        
class AccountSchema(ma.Schema) :
class Meta : 
        fields = ('id','username','email','password','phone','wilaya','photo')  


# with app.app_context() : 
#     db.drop_all()
#     db.create_all()


class Post(db.Model) :
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(190), nullable = False)
    year = db.Column(db.Integer(), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    km_driven = db.Column(db.Integer(), nullable = False)
    fuel = db.Column(db.String(30), nullable = False)
    seller_type = db.Column(db.String(30), nullable = False)
    transmission = db.Column(db.String(30), nullable = False)
    mileage = db.Column(db.Float(), nullable = False)
    engin = db.Column(db.Integer(), nullable = False)
    max_power = db.Column(db.Float(), nullable = False)
    torque = db.Column(db.String(100), nullable = False)
    seats = db.Column(db.Integer(), nullable = False)
    created_at = db.Column(db.String(100), default = "date")
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'),nullable=False)
    likes = db.relationship('Like', backref='likes_owned_post')
    
    def __init__(self, name, year, price, km_driven, fuel, seller_type, transmission, mileage, engin, max_power, torque, seats, owner_id, created_at) : 
        self.name = name
        self.year = year
        self.price = price
        self.km_driven = km_driven
        self.fuel = fuel
        self.seller_type = seller_type
        self.transmission = transmission
        self.mileage = mileage
        self.engin = engin
        self.max_power = max_power
        self.torque = torque
        self.seats = seats
        self.created_at = created_at
        self.owner_id = owner_id

# with app.app_context() : 
#     db.drop_all()
#     db.create_all()

class PostSchema(ma.Schema) :
    class Meta : 
        fields = ('id','name', 'year', 'price', 'km_driven', 'fuel', 'seller_type', 'transmission', 'mileage', 'engin', 'max_power', 'torque', 'seats', 'owner_id', 'created_at') 
        

class Like(db.Model) : 
    id = db.Column(db.Integer(), primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),nullable=False)
    
    def __init__(self, post_id, account_id) : 
        self.account_id = account_id
        self.post_id = post_id
    
class LikeSchema(ma.Schema) :
    class Meta : 
        fields = ('id','post_id', 'account_id')
    


# class ReviewProfile(db.Model) :
#     id = db.Column(db.Integer(), primary_key = True)
#     account_id = db.Column(db.Integer, db.ForeignKey('acount.id'),nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)
#     content = db.Column(db.String(100), nullable = False)
    
#     def __init__(self, account_id, post_id, content) : 
#         self.account_id = account_id
#         self.post_id = post_id
#         self.content = content
        
# class ReviewProfileSchema(ma.Schema) : 
#     class Meta : 
#         fields = ('id','account_id', 'post_id','content')


# with app.app_context() : 
#     db.drop_all()
#     db.create_all()

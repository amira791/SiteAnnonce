from flask import jsonify, request
from app import app, db
from app.models import Account, AccountSchema, PostSchema, Post, Like, LikeSchema
import pickle
from joblib import dump, load
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
import category_encoders as ce
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from tabulate import tabulate



account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)   

@app.get("/accounts")
def get_accounts(): 
    all_accounts = Account.query.all()
    accounts = accounts_schema.dump(all_accounts)
    return jsonify(accounts)


@app.get("/accounts/<id>")
def get_account(id):
    account = Account.query.get(id)
    return account_schema.jsonify(account)

@app.post("/accounts")
def create_account():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    wilaya = request.json['wilaya']
    photo = request.json['photo']
    
    account = Account(username, email, password, phone, wilaya, photo)
    
    db.session.add(account)
    db.session.commit()
    return account_schema.jsonify(account)

@app.post("/login")
def login_function() :
    mail_saisi = request.json['email']
    pass_saisi = request.json['password']
    
    account = Account.query.filter_by(email = mail_saisi, password = pass_saisi).first()
    print("ggg")
    print(type(account))
    print(account)
    
    if account:
        return jsonify({
            'message' : "Il existe"
        }), 200
    else :
        return jsonify({
            'message' : "Il existe pas"
        }), 400



@app.put("/accounts/<id>")
def update_account(id) :
    account = Account.query.get(id)
    
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    wilaya = request.json['wilaya']
    photo = request.json['photo']
    
    account.username = username
    account.email = email
    account.password = password
    account.phone = phone
    account.wilaya = wilaya
    account.photo = photo
    db.session.commit()
    return account_schema.jsonify(account)


@app.delete("/accounts/<id>")
def delete_user(id) :
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()  
    return account_schema.jsonify(account)







post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.get("/posts")
def get_posts(): 
    all_posts = Post.query.all()
    posts = posts_schema.dump(all_posts)
    return jsonify(posts)

@app.post("/posts")
def create_post():
    name = request.json['name']
    year = request.json['year']
    price = request.json['price']
    km_driven = request.json['km_driven']
    fuel = request.json['fuel']
    seller_type = request.json['seller_type']
    transmission = request.json['transmission']
    owner_id = request.json['owner_id']
    mileage = request.json['mileage']
    engin = request.json['engin']
    max_power = request.json['max_power']
    torque = request.json['torque']
    seats = request.json['seats']
    created_at = request.json['created_at']
    
    post = Post(name, year, price, km_driven, fuel, seller_type, transmission, mileage, engin, max_power, torque, seats, owner_id,created_at)

    with app.app_context():
     db.create_all()

    
    db.session.add(post)
    db.session.commit()
    return account_schema.jsonify(post)

@app.put("/posts/<id>")
def update_post(id) :
    post = Post.query.get(id)
    print("hna")
    name = request.json['name']
    year = request.json['year']
    price = request.json['price']
    km_driven = request.json['km_driven']
    fuel = request.json['fuel']
    seller_type = request.json['seller_type']
    transmission = request.json['transmission']
    owner_id = request.json['owner_id']
    mileage = request.json['mileage']
    engin = request.json['engin']
    max_power = request.json['max_power']
    torque = request.json['torque']
    seats = request.json['seats']
    created_at = request.json['created_at']
    
    post.name = name
    post.year = year
    post.price = price
    post.km_driven = km_driven
    post.fuel = fuel
    post.seller_type = seller_type
    post.transmission = transmission
    post.owner_id = owner_id
    post.mileage = mileage
    post.engin = engin
    post.max_power = max_power
    post.torque = torque
    post.seats = seats
    post.created_at = created_at
    db.session.commit()
    return account_schema.jsonify(post)


@app.get("/account/<id>/posts")
def get_my_posts(id) :
    all_my_posts = Post.query.filter_by(owner_id = id)
    posts = posts_schema.dump(all_my_posts)
    return jsonify(posts)

@app.delete("/posts/jjj")
def delete_post(id) :
    post = Post.query.get(5)
    db.session.delete(post)
    db.session.commit()
    return account_schema.jsonify(post)





like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)

@app.post("/like")
def like_unlike_post() : 
    account_id = request.json['account_id']
    post_id = request.json['post_id']
    
    like = Like.query.filter_by(account_id = account_id, post_id = post_id).first()
    
    if like:
        print("afichage")
        print(like.account_id)
        db.session.delete(like)
        db.session.commit()
        return jsonify({
            'liked' : False, 
            'message' : "post is unliked"
        }), 200
    else :
        new_like = Like(post_id, account_id)
        print("creer un new like")
        print(new_like.post_id)
        print(new_like.account_id)
        db.session.add(new_like)
        db.session.commit()
        return like_schema.jsonify(new_like)
        
@app.get("/account/<id>/fav_posts")
def get_my_favorite_posts(id) : 
    likes = Like.query.filter_by(account_id = id)
    likes = likes_schema.dump(likes)
    if len(likes) != 0 : 
        print("le type de likes")
        print(type(likes))
        res_fin = [] 
        for like in likes : 
            postes = Post.query.filter_by(id = like['post_id'])
            likes_temp = likes_schema.dump(postes) 
            for element in likes_temp : 
                print(type(element))
                res_fin.append(element)        
        return jsonify(res_fin)
    else : 
        return jsonify({
            'message' : "Pas de postes likés"
        }), 400
    
    








clf = load("model.pkl")

@app.post("/predict")
def calcul_prix():
    
    year = request.json['year']       
    engine = request.json['engin']
    max_power = request.json['max_power']
    print(year)
    print(engine)
    print(max_power)
    table = [[year, engine , max_power]]
    prediction_prix =  clf.predict(table)
    print("le resultat")
    liste = prediction_prix.tolist()
    fin = liste[0]
    print(fin)
    if prediction_prix : 
        return jsonify({'prix de prediction' : fin}), 200
    else : 
        return jsonify({'message' : "Error lors de prediction"}), 400













from flask import request,json,jsonify
from app import app
from flask_marshmallow import Marshmallow
from app import db


ma=Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True)
    email = db.Column(db.String)
    password=db.Column(db.String)
    ph_no=db.Column(db.String)

    def __init__(self,username,email,password,ph_no):
        self.username=username
        self.email=email
        self.password=password
        self.ph_no = ph_no
        

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','username','email','password','ph_no')

user_schema=UserSchema()
users_schema=UserSchema(many=True)

db.create_all()

@app.route('/user/<user>',methods=['GET'])
def get_user(user):
    user=User.query.filter_by(username=user)
    result = users_schema.dump(user)
    return jsonify(result[0])
    #return user_schema.jsonify(user)

@app.route('/user',methods=['POST','GET'])
def add():
    if request.method=="POST":
        username = request.json['username']
        email=request.json['email']
        password=request.json['password']
        ph_no=request.json['ph_no']
        user=User(username,email,password,ph_no)
        db.session.add(user)
        db.session.commit()

        return user_schema.jsonify(user)
    else:
        all_user= User.query.all()
        result= users_schema.dump(all_user)
        return jsonify(result)
    

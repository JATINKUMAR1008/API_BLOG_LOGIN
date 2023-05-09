from flask import request,json,jsonify,Response
from app import app
from flask_marshmallow import Marshmallow
from app import db
from werkzeug.utils import secure_filename

ma=Marshmallow(app)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String)
    name = db.Column(db.Text)
    mimetype = db.Column(db.Text)

db.create_all()

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    author = db.Column(db.String)

class Blog_Schema(ma.Schema):
    class Meta:
        fields = ('id', 'title','content','author')
blog_Schema = Blog_Schema()
blogs_Schema = Blog_Schema(many=True)

db.create_all()

@app.route('/add_blog',methods=['POST'])
def add_blog():
    title = request.json['title']
    content = request.json['content']
    author = request.json['author']
    blog = Blog(title,content,author)
    db.session.add(blog)
    db.session.commit()
    return blog_Schema.jsonify(blog)

@app.route('/get_blogs',methods=['GET'])
def get_blog():
    blogs = Blog.query.all()
    res_blogs = blogs_Schema.dump(blogs)
    return jsonify(res_blogs)

@app.route('/blog_image',methods=['GET','POST'])
def get_img(name):
    if request.method=='POST':
        pic = request.files['file']
        filename = secure_filename(name)
        mimetype=pic.mimetype
        img = Img(img=pic.read(),mimetype=mimetype,name=filename)
        db.session.add(img)
        db.session.commit()
        return 'Img uploaded' ,200
    else:
        

        new_name = name.replace(" ","_")
        new_name = new_name.replace("'","")
        if new_name[len(new_name)-1] == "_":
            new_name = new_name[:-1]
        
        img_data = Img.query.filter_by(name = new_name).first()
        return Response(img_data.img,mimetype=img_data.mimetype)
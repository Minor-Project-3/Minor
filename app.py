from flask import Flask, render_template, request,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import random
import json
import os
import string
# from werkzeug import *
from werkzeug.utils import secure_filename
from datetime import datetime

with open('config.json', 'r') as c:
    parameter = json.load(c)["parameter"]

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/fakenews'
app.config['UPLOAD_FOLDER']=parameter['folder_location']
app.config['SQLALCHEMY_DATABASE_URI'] = parameter['database_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = parameter['admin_mail'],
    MAIL_PASSWORD=  parameter['admin_pass']
)
mail = Mail(app)
i=0

follows=db.Table('follows',db.Column('uid_who',db.Integer,db.ForeignKey('user.uid'),primary_key=True),db.Column('uid_whom',db.Integer,db.ForeignKey('user.uid'),primary_key=True))
liketab=db.Table('liketab',db.Column('uid_who',db.Integer,db.ForeignKey('user.uid'),primary_key=True),db.Column('pid',db.Integer,db.ForeignKey('post.pid'),primary_key=True),db.Column('like_date',db.DateTime))

class User(db.Model):
    __tablename__="user"
    uid=db.Column(db.Integer,primary_key=True, unique=True,autoincrement=True)
    uname=db.Column(db.String(120), nullable=False)
    passw=db.Column(db.String(120), nullable=False)
    name=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(120), nullable=False)
    ContactNo=db.Column(db.String(120), nullable=False)
    follower_count=db.Column(db.Integer)
    following_count=db.Column(db.Integer)
    descrp=db.Column(db.String(220))
    terror_count=db.Column(db.Integer)
    posts=db.relationship('Post',backref='user')
    #follo=db.relationship('User',secondary=follows)

    def __init__(self,passw,uName,name,cont,ema,descrp,follower_count=0,following_count=0,terror_count=0):
        self.passw=passw
        self.uname=uName
        self.name=name
        self.ContactNo=cont
        self.email=ema
        self.follower_count=follower_count
        self.following_count=following_count
        self.descrp=descrp
        self.terror_count=terror_count

class Post(db.Model):
    __tablename__="post"
    pid=db.Column(db.Integer,primary_key=True, unique=True,autoincrement=True)
    ptitle=db.Column(db.String(120),nullable=False)
    pdate=db.Column(db.DateTime)
    pdesc=db.Column(db.String(500))
    pimgpath=db.Column(db.String(120))
    likes=db.Column(db.Integer)
    active=db.Column(db.Integer)
    uid=db.Column(db.Integer,db.ForeignKey('user.uid'),nullable=False)
#lik=db.relationship('user',secondary=liketab)

def __init__(self, ptitle,pdate,pdesc,uid,pimgpath,likes=0,active=1):
    self.ptitle=ptitle
    self.pdate=pdate
    self.pdesc=pdesc
    self.pimgpath=pimgpath
    self.likes=likes
    self.active=active
    self.uid=uid

@app.route("/")
def func():
    return render_template('index.html')

# -----------------------------------------------------------------------

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        uname = request.form.get('uname')
        name = request.form.get('name')
        passw = request.form.get('passw')
        rpassw = request.form.get('rpassw')
        email= request.form.get('email')
        phno = request.form.get('phno')
        if passw==rpassw:
            user1=User(passw=passw,uName=uname,name=name,cont=phno,ema=email,descrp="Hi There I am using Fake Book")
            db.session.add(user1)
            db.session.commit()
            return render_template('index.html',tick=1)
    return"HEllo"

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        if(request.method=='POST'):
            Custname = request.form.get('user')
            Custpass = request.form.get('pass')
            getinfo = db.session.query(User).filter_by(uname=Custname,passw=Custpass).count()
            if getinfo==1:
                session['logged_in'] = True
                return render_template('dashboard.html',my_string=Custname)
            else:
                return render_template('index.html',val=1)
    else:
        return render_template("home.html")
    

@app.route("/logout")  
def logout():
    session['logged_in'] = False
    return render_template("index.html")

@app.route("/forget",methods = ['GET', 'POST'])
def forget():
    return render_template("forget.html")

@app.route("/reset",methods = ['GET', 'POST'])  
def reset():
    uname=request.form.get('uname')
    email = request.form.get('email')
    getinfo = db.session.query(User).filter_by(uname=uname,email=email)
    # smail="psp51790@gmail.com"
    smail=parameter['admin_mail']
    if getinfo.count()==1:
        pas=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        getinfo.update(dict(passw=pas))
        message="Hello There %s .<br>Your Password has been generated .<br>Your password is <strong>%s</strong>.<br>Please login with this password to change password"%(uname,pas)
        #msg=MIMEText(message,'html')
        db.session.commit()
        mail.send_message(subject="Password Generated",html=message,sender=smail,recipients = [email])
        return "Hello"
    else:
        return "Hi"

# -----------------------------------------------------------------------------------------------------------

@app.route("/upload",methods=['POST','GET'])
def upload():
    if (request.method =="POST"):
        f=request.files['file']
        ptitle=request.form.get('ptitle')
        global i
        i=i+1
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        # path=str(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename+str(i)))
        path=str(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        # print(path) 
        post=Post(ptitle=ptitle,pdate=datetime.now(),pdesc="Hello",uid=1,pimgpath=path,likes=0,active=1)  
        db.session.add(post)
        db.session.commit()
        return "uploaded"
    else:
        return "sorry"

@app.route("/uploadPost",methods=['POST','GET'])
def uploadPost():
    return render_template("upload.html")

# -----------------------------------------------------------------------------------------------------------

@app.route("/retrivePost",methods=['POST','GET'])
def retrivePost():
    post=Post.query.first()
    return render_template("postRetrive.html",post=post)


if __name__ == "__main__":
    app.run(debug=True)
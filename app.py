from flask import Flask,render_template,request,session,flash,redirect,url_for,send_from_directory,flash
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import random, copy
import smtplib
import requests
import string
import random
from werkzeug.utils import secure_filename
import os
from database import db,User,Post,follows,liketab
from flask_mail import Mail
from datetime import datetime
from passlib.hash import sha256_crypt
import tensorflow as tf
import joblib
import numpy as np
from keras.preprocessing import image



app=Flask(__name__)
loaded_model = joblib.load('./pipeline.sav')

model = tf.keras.models.load_model('model (1).h5') 
app.config['UPLOAD_FOLDER']=r'static\uploads'
app.secret_key='United'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:saksham@localhost/minor'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ykznxsdzcebfil:d1f44feba03fada8da02d88a302da48ac1544efbbf301f9a47361ac1fde07ea9@ec2-54-159-175-113.compute-1.amazonaws.com:5432/ddqgp9nsn8aj32?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "psp51790@gmail.com",
    MAIL_PASSWORD=  "ps*123456"
)
mail = Mail(app)

i=0
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if(request.method=='POST'):
        Custname = request.form.get('user')
        Custpass = request.form.get('pass')
        getinfo = db.session.query(User).filter_by(uname=Custname).first()
        if Custname=="admin" and Custpass=="admin":
            session['user'] = "admin"
            return render_template('admindashboard.html',name=Custname)
        elif sha256_crypt.verify(Custpass, getinfo.passw):
            session['user'] = Custname
            session['uid']=getinfo.uid
            b=session['uid']
            a = db.session.execute("SELECT * FROM follows WHERE uid_who=:param ",{"param": b})
            names = [row[1] for row in a]
            c,d=[],[]
            for i in names :
                getinfo = db.session.query(User).filter_by(uid=i).order_by(func.random()).all()
                c.append(getinfo[0])
            for j in c:
                get = db.session.query(Post).filter_by(uid=j.uid,active=1).order_by(Post.pdate.desc()).all()
                d.append(get)
                        
            return render_template("homepage.html",unam=session['user'],c=zip(c,d))
        else:
            return render_template('index.html')

@app.route("/logout")  
def logout():
    print(session['user'])
    session.pop('user', None)
    return redirect("/")


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        uname = request.form.get('uname')
        name = request.form.get('name')
        passw = request.form.get('passw')
        rpassw = request.form.get('rpassw')
        email= request.form.get('email')
        phno = request.form.get('phno')
        info=db.session.query(User).filter_by(uname=uname).count()
        if passw==rpassw and info!=1:
            passs=sha256_crypt.encrypt(passw)
            user1=User(passw=passs,uName=uname,name=name,cont=phno,ema=email,descrp="Hi There I am using Fake Book")
            db.session.add(user1)
            db.session.commit()
            return render_template("index.html",mess="Congratulation,Account has been created")
        else:
            return "Username Already Exist"

@app.route("/forget",methods = ['GET', 'POST'])
def forget():
    return render_template("forget.html")
    
@app.route("/reset",methods = ['GET', 'POST'])  
def reset():
    uname=request.form.get('uname')
    email = request.form.get('email')
    getinfo = User.query.filter_by(uname=uname,email=email)
    smail="psp51790@gmail.com"
    if getinfo.count()==1:
        pas=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        type(getinfo)
        message="Hello There %s .<br>Your Password has been generated .<br>Your password is <strong>%s</strong>.<br>Please login with this password to change password"%(uname,pas)
        #msg=MIMEText(message,'html')
        getinfo.update(dict(passw=pas))
        db.session.commit()
        mail.send_message(subject="Password Generated",html=message,sender=smail,recipients = [email])
        return "Hello"
    else:
        return "Hi"  

@app.route("/upload",methods=['POST','GET'])
def upload():
    if (request.method =="POST"):
        f=request.files['file']
        ptitle=request.form.get('ptitle')
        pdesc=request.form.get('desc')
        i=0
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        path=str(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        print(path)
        result = loaded_model.predict([pdesc])
        print(result)
        test_image = image.load_img(path, target_size = (64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result1 = model.predict(test_image)
        if result1[0][0] == 1:
            prediction = 'terror'
            i=0   
        else:
            prediction = 'person'
            i=1
        print(prediction) 
        post=Post(ptitle=ptitle,pdate=datetime.now(),pdesc=pdesc,uid=session['uid'],pimgpath=path,likes=0,active=i)  
        db.session.add(post)
        db.session.commit()
        return render_template("homepage.html",unam=session['user'],mesg="Post Uploaded Successfully")
    else:
        return "sorry"

@app.route("/uploadPost",methods=['POST','GET'])
def uploadPost():
    return render_template("upload.html")    

@app.route("/displayPost/<posttype>",methods=['POST','GET'])
def displayPost(posttype):
    if posttype=="fair":
        info=db.session.query(Post).filter_by(active=1).all()
        return render_template("test.html",post=info)
    if posttype=="blocked":
        info=db.session.query(Post).filter_by(active=0).all()
        return render_template("test.html",post=info)
    if posttype=="critical":
        info=db.session.query(User).filter_by(terror_count=2).all()
        return render_template("userlist.html",info=info)
    if posttype=="blockedusr":
        info=db.session.query(User).filter_by(terror_count=3).all()
        return render_template("userlist.html",info=info)

@app.route('/display/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename=filename)

@app.route('/userlist')
def userlist():
    info=db.session.query(User)
    return render_template('userlist.html',info=info)

@app.route("/adminDashboard",methods=['POST','GET'])
def adminDashBoard():
    return render_template("upload.html") 

@app.route("/deletePost/<string:id>",methods=['POST'])
def deletePost(id):
    db.session.query(Post).filter_by(pid=id).delete()
    db.session.commit()
    return render_template('admindashboard.html')

@app.route("/followUser",methods=['POST'])
def followUser():
    getinfo = db.session.query(User).all()
    return render_template("Following.html",users=getinfo)  

 

@app.route("/follow/<string:id>",methods=['POST'])
def follow(id):
    user=session['uid']
    statement = follows.insert().values(uid_who=user, uid_whom=id)
    db.session.execute(statement)
    db.session.commit()
    getinfo=db.session.query(User).filter_by(uid=user)
    getinfo1=db.session.query(User).filter_by(uid=id)
    i=getinfo.first().following_count
    i+=1
    getinfo.update({User.following_count:i})
    k=getinfo1.first().follower_count
    k+=1
    getinfo1.update({User.follower_count:k})
    db.session.commit()
    a = db.session.execute("SELECT * FROM follows WHERE uid_who=:param ",{"param": user})
    names = [row[1] for row in a]
    c,d=[],[]
    for i in names :
        getinfo = db.session.query(User).filter_by(uid=i).order_by(func.random()).all()
        c.append(getinfo[0])
    for j in c:
        get = db.session.query(Post).filter_by(uid=j.uid,active=1).order_by(Post.pdate.desc()).all()
        d.append(get)
                        
    return render_template("homepage.html",unam=session['user'],c=zip(c,d))
    

@app.route("/followingList",methods=['GET'])
def followingList():
    b=session['uid']
    # info=follows.select().where(uid_who==b)
    a = db.session.execute("SELECT * FROM follows WHERE uid_who=:param",{"param": b})
    names = [row[1] for row in a]
    c=[]
    for i in names :
        getinfo = db.session.query(User).filter_by(uid=i).all()
        c.append(getinfo[0])
    print(c[0].uid)
    # print(getinfo[0].uid)
    return render_template("unfollow.html",users=c)
@app.route("/followerList",methods=['GET'])
def followerList():
    b=session['uid']
    # info=follows.select().where(uid_who==b)
    a = db.session.execute("SELECT * FROM follows WHERE uid_whom=:param",{"param": b})
    names = [row[1] for row in a]
    c=[]
    for i in names :
        getinfo = db.session.query(User).filter_by(uid=i).all()
        c.append(getinfo[0])
    print(c[0].uid)
    # print(getinfo[0].uid)
    return render_template("Following.html",users=c)

@app.route("/unfollow/<string:id>",methods=['POST'])
def unfollow(id):
    user=session['uid']
    # statement = follows.delete(uid_who=a, uid_whom=id)
    a = db.session.execute("DELETE FROM follows WHERE uid_who=:param and uid_whom=:para ",{"param": user,"para":id})
    # db.session.execute(statement)
    db.session.commit()
    getinfo=db.session.query(User).filter_by(uid=user)
    i=getinfo.first().following_count
    i-=1
    getinfo.update({User.following_count:i})

    getinfo1=db.session.query(User).filter_by(uid=id)
    k=getinfo1.first().follower_count
    k-=1
    getinfo1.update({User.follower_count:k})

    db.session.commit()
    a = db.session.execute("SELECT * FROM follows WHERE uid_who=:param ",{"param": user})
    names = [row[1] for row in a]
    c,d=[],[]
    for i in names :
        getinfo = db.session.query(User).filter_by(uid=i).order_by(func.random()).all()
        c.append(getinfo[0])
    for j in c:
        get = db.session.query(Post).filter_by(uid=j.uid,active=1).order_by(Post.pdate.desc()).all()
        d.append(get)
                    
    return render_template("homepage.html",unam=session['user'],c=zip(c,d))

@app.route("/Myprofile",methods=['GET'])
def Myprofile():
    getinfo = db.session.query(User).filter_by(uid=session['uid']).first()
    getpost = db.session.query(Post).filter_by(uid=session['uid'],active=1).order_by(Post.pdate.desc()).all()
    return render_template("Myprofile.html",users=getinfo,post=getpost)

@app.route("/like",methods=['POST','GET'])
def like():
    if (request.method =="POST"):
        f=request.form['pid']
        print(f)
        return "H"
        
if __name__=="__main__":
    app.run(debug=True)


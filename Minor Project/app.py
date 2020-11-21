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


app=Flask(__name__)
app.config['UPLOAD_FOLDER']=r'C:\Users\1\Desktop\Minor Project\static\uploads'
app.secret_key='United'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:saksham@localhost/minor'
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
    if not session.get('logged_in'):
        if(request.method=='POST'):
            Custname = request.form.get('user')
            Custpass = request.form.get('pass')
            getinfo = db.session.query(User).filter_by(uname=Custname,passw=Custpass).count()
            if getinfo==1:
                session['logged_in'] = True
                return ('dashboard')
            elif Custname=="admin" and Custpass=="admin":
                session['logged_in'] = True
                return render_template('admindashboard.html',name=Custname)
            else:
                return render_template('index.html')
    else:
        flash('Already logged in')
        return render_template("index.html")

@app.route("/logout")  
def logout():
    session['logged_in'] = False
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
        if passw==rpassw:
            user1=User(passw=passw,uName=uname,name=name,cont=phno,ema=email,descrp="Hi There I am using Fake Book")
            db.session.add(user1)
            db.session.commit()

        return "HEllo"

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
        global i
        i=i+1
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        # path=str(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename+str(i)))
        path=secure_filename(f.filename)
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

@app.route("/retimg",methods=['POST','GET'])
def retimg():
    info=db.session.query(Post)
    return render_template("test.html",post=info)

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


if __name__=="__main__":
    app.run(debug=True)


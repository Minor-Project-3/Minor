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


app=Flask(__name__)
model = tf.keras.models.load_model('model (1).h5') 
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
    if(request.method=='POST'):
        Custname = request.form.get('user')
        Custpass = request.form.get('pass')
        getinfo = db.session.query(User).filter_by(uname=Custname).first()
        if Custname=="admin" and Custpass=="admin":
            session['user'] = "admin"
            return render_template('admindashboard.html',name=Custname)
        elif sha256_crypt.verify(Custpass, getinfo.passw):
            session['user'] = Custname
            return ('dashboard')
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
            return "HEllo"
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
        global i
        i=i+1
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        # path=str(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename+str(i)))
        path=secure_filename(f.filename)
        # print(path) 
        post=Post(ptitle=ptitle,pdate=datetime.now(),pdesc=pdesc,uid=1,pimgpath=path,likes=0,active=0)  
        db.session.add(post)
        db.session.commit()
        return "uploaded"
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

@app.route("/predictImg/<str:path>",methods=['POST','GET'])
def predictImg(path):
  test_image = image.load_img(path, target_size = (64, 64))
  test_image = image.img_to_array(test_image)
  test_image = np.expand_dims(test_image, axis = 0)
  result = model.predict(test_image)
  if result[0][0] == 1:
      prediction = 'terror'
  else:
      prediction = 'person'
  print(prediction)

if __name__=="__main__":
    app.run(debug=True)


from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()


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

    
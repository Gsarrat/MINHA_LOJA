from loja import db, app
from datetime import datetime


class Cadastrar(db.Model):
    id       = db.Column(db.Integer,primary_key = True)
    name     = db.Column(db.String(50), unique = False)
    username = db.Column(db.String(50), unique = False)
    email    = db.Column(db.String(50), unique = False)
    password = db.Column(db.String(50), unique = False)
    confirm  = db.Column(db.String(50), unique = False)
    country  = db.Column(db.String(50), unique = False)
    city     = db.Column(db.String(50), unique = False)
    contact  = db.Column(db.String(50), unique = False)
    address  = db.Column(db.String(50), unique = False)
    zipcode  = db.Column(db.String(50), unique = False)
    profile  = db.Column(db.String(50), unique = False, default='profile.jpg')
    data_criado  = db.Column(db.DateTime, nullable='False', default=datetime.utcnow)


    def __repr__(self):
        return '<Cadastrar %r>' % self.name

with app.app_context():

    db.create_all()
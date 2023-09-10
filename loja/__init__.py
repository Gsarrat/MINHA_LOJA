from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///minhaloja.db"
app.config['SECRET_KEY'] = "12345"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'clienteLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Fazer o login Primeiro"


app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from loja.ADMIN import rotas
from loja.produtos import rotas
from loja.carrinho import carrinhos
from loja.clientes import rotas




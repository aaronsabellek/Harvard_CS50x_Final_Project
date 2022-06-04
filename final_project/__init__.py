from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xxxxx'
app.config["SECURITY_PASSWORD_SALT"] = 'xxxxx'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure bootstrap
Bootstrap(app)

# Configure Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configure Mail Server
app.config['MAIL_SERVER']='xxxxx'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xxxxx'
app.config['MAIL_PASSWORD'] = 'xxxxx'
app.config['MAIL_DEFAULT_SENDER'] = 'xxxxx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

from final_project import routes
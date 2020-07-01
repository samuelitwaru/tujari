from flask import (
    Flask, 
    request, 
    Blueprint, 
    jsonify, 
    make_response, 
    g, 
    abort,
    flash,
    render_template
)
from flask_login import LoginManager
from . import config, extensions as ext
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(config.DevelopmentConfig)
login_manager = LoginManager(app)
login_manager.login_view = '/home'
login_manager.login_message_category = 'info'


# csrf = ext.csrf
# csrf.init_app(app)
redis = ext.redis
from sqlalchemy import create_engine
from Application.database.model import Base, engine, session
from flask_migrate import Migrate
from Application.routes.customers.routes import customers
from Application.routes.vendors.routes import vendors

## NEW BLUEPRINTS
from Application.routes.customers.account import account
from Application.routes.vendors.account import vendor_account

app.register_blueprint(customers)
app.register_blueprint(vendors)

app.register_blueprint(account)
app.register_blueprint(vendor_account)


from Application.routes.admin import initialize_admin

@app.teardown_request
def remove_session(exception=None):
    session.remove()
    
class db(object):
    engine = engine
    metadata = Base.metadata


migrate = Migrate(app, db)





from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
# config
app.config.from_object(Config)

app.config['SECRET_KEY'] = 'handsome_cxm'  # 设置session加密的密钥

# init ext
db.init_app(app)
from .models import init_model
init_model()

with app.app_context():
    from .views import user_view
    app.register_blueprint(user_view, url_prefix="/cxm")

    from .views import purchase_view
    app.register_blueprint(purchase_view, url_prefix="/cxm")

    from .views import message_view
    app.register_blueprint(message_view, url_prefix="/cxm")


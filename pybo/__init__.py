from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

#import config
from flaskext.markdown import Markdown

def page_not_found(e):
    return render_template('404.html'), 404


naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"        
    }

db = SQLAlchemy( metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # from_object 를 from_envvar 로 변경
    app.config.from_envvar('APP_CONFIG_FILE')
    
    # 아래 config 부분을 config.py 로 따로 두고 불러오
    #basedir = os.path.abspath(os.path.dirname(__file__))
    #app.config['SQLALCHEMY_DATABASE_URI'] = \
    #       'sqlite:///' + os.path.join(basedir, 'pybo.db' )
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SECRET_KEY'] =  "dev"    
    #app.config.from_object(config)

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app,db)
    
    from .views import main_views, question_views, answer_views
    from .views import auth_views, comment_views,vote_views
    
    from . import models        
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)    
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)    

    from .filter import format_datetime, format_datetime_han
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['datetimehan'] = format_datetime_han

    Markdown( app, extensions=['nl2br', 'fenced_code'])
    
    app.register_error_handler(404, page_not_found)
    
    return app

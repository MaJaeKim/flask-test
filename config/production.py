from config.defalut import *
from logging.config import dictConfig

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format( os.path.join( BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b'\x86\x82\xe8\x87Di\x1d\x96\xe4,j3h\xc6c\x0b'

dictConfig({
    'version':1,
    'formatters':{
        'default': {
            'format':'[%(asctime)s] %(levelname)s in %(module)s: %(message)s',                
            }
        },
    'handlers':{
        'file':{
            'level':'INFO',
            'class': 'logging.handler.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/flasktest.log'),
            'maxBytes': 1024*1024*5,
            'backupCount':5,
            'formatter':'default',            
            },
        },
    'root':{
        'level':'INFO',
        'handlers':['file']
        }
})        

from config.defalut import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format( os.path.join( BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b'\x86\x82\xe8\x87Di\x1d\x96\xe4,j3h\xc6c\x0b'

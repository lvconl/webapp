from ajax import ajax
from models import app

views = __import__('views')
app.register_blueprint(ajax)

if __name__ == '__main__':
    app.run()

from ajax import ajax
from models import app
from models import db
from topic.views import topic

views = __import__('views')
app.register_blueprint(ajax)
app.register_blueprint(topic)

if __name__ == '__main__':
    app.run()

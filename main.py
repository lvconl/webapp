from ajax import ajax
from models import app
from models import db
from topic.views import topic
from comment.views import comment
from user.views import person

views = __import__('views')
app.register_blueprint(ajax)
app.register_blueprint(topic)
app.register_blueprint(comment)
app.register_blueprint(person)

if __name__ == '__main__':
    app.run()

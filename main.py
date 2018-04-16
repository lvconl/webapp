from ajax import ajax
from models import app
from models import db
from topic.views import topic
from comment.views import comment
from user.views import person
from answer.views import answer

views = __import__('views')
app.register_blueprint(ajax)
app.register_blueprint(topic)
app.register_blueprint(comment)
app.register_blueprint(person)
app.register_blueprint(answer)

if __name__ == '__main__':
    app.run()

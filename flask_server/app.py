from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=['GET'])
def index():
    posts = models.Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        message = models.Post(name=name, content=post)
        db.session.add(message)
        db.session.commit()


@app.route('/login', methods=['GET','POST'])
def login():
    form = Loginform
    return{"test":["test1", "test2", "test3"]}


if __name__ == '__main__':
    app.run(debug=True)

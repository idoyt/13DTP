from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        message = models.Post(name=name, content=post)
        db.session.add(message)
        db.session.commit()

    posts = models.Post.query.all()

    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

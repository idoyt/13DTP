from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)

CORS(app)
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        models.Post.query.add(name, post)
        db.Post.commit()

    posts = models.Post.query.all()

    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, LoginManager, current_user, login_required
from forms import LoginForm, RegistrationForm
import models
from is_safe_url import is_safe_url



app = Flask(__name__)

app.config['SECRET_KEY'] = 'Ligmaballz!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return models.Auth.query.get(int(id))


@app.route('/', methods=['GET'])
@login_required
def index():
    posts = models.Chat.query.all()
    return render_template('index.html', posts=posts)


@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    if request.method == 'POST':
        post = request.form.get('post')
        message = models.Chat(name=name, content=post)
        db.session.add(message)
        db.session.commit()

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        message = models.Chat(name=name, content=post)
        db.session.add(message)
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        auth = models.Auth.query.filter_by(login=form.username.data).first()
        #if auth is None or not auth.check_password(form.password.data):
        login_user(auth, remember=form.remember_me.data)
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next, allowed_hosts="localhost:5000"):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(form.username.data, form.email.data)
    if form.validate_on_submit():
        auth = models.Auth(login=form.username.data, email=form.email.data)
        auth.set_password(form.password.data)
        db.session.add(auth)
        db.session.commit()
        flash('You are now a registered user.')
        print('You are now a registered user.')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

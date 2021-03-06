from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, LoginManager, current_user, login_required
from forms import LoginForm, RegistrationForm, CreateChatForm, SendMessageForm
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
    return models.User.query.get(int(id))


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/chat/<int:id>', methods=['GET','POST'])
@login_required
def chat(id):
    #chat_history = models.Chat_Line.query().filter_by(id=id).all()
    form = SendMessageForm()
    if request.method == 'POST':
        chat_line = models.Chat_Line(user_id=current_user.id, chat_id=id, reply_to=form.reply_to.data)
        db.session.add(chat_line)
        db.session.commit()
        chat_line_id = models.Chat_Line.query.filter_by(user_id=current_user.id, chat_id=id, reply_to=form.reply_to.data).first()
        message = models.Message(Chat_Line_id=chat_line_id.id, content=form.content.data)
        db.session.add(message)
        db.session.commit()
    return render_template("chat.html", form=form, messages=chat_history, user=current_user.id)

@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = CreateUserProfile()
    if form.validate_on_submit():
        user_profile = models.User()

@app.route('/create_chat', methods=['GET', 'POST'])
@login_required
def create_chat():
    form = CreateChatForm()
    if form.validate_on_submit():
        chat = models.Chat(user_id=current_user.id, name=form.name.data, image=form.image.data)
        db.session.add(chat)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("create_chat.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('wrong password or username')
        else:
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next, allowed_hosts="localhost:5000"):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data, username=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

from avengers_book import app, db, Message, mail
from flask import render_template, request, redirect, url_for
from avengers_book.forms import UserInfoForm, BlogPostForm, LoginForm

from avengers_book.models import User, Post, check_password_hash

from flask_login import login_required, login_user, current_user, logout_user


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n",username, password, email)
        user= User(username, email, password)
        db.session.add(user)
        db.session.commit()
        # SendGrid account was under review so email feature wasn't working
        # msg = Message(f'Thanks for signing up, {username}!', recipients=[email])
        # msg.body = ('Looking forward to your other attributes')
        # msg.html = ('<h1> Welcome to the Avengers Phone Book </h1>')

        # mail.send(msg)
    return render_template("register.html", form=form)

        
@app.route('/createanewcontact', methods=['GET', 'POST'])
@login_required
def createanewcontact():
    form = BlogPostForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        print("\n", title, content)
        post = Post(title,content, user_id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('createanewcontact'))
    return render_template('createanewcontact.html', form=form)

@app.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = BlogPostForm()
    
    if request.method == 'POST' and update_form.validate():
        title = update_form.title.data
        content = update_form.content.data
        user_id = current_user.id
        
        post.title = title
        post.content = content
        post.user_id = user_id

        db.session.commit()
        return redirect(url_for('post_update', post_id=post.id))

    return render_template('post_update.html', update_form=update_form)


@app.route('/posts/delete/<int:post_id>', methods=['POST']) 
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))
    






@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

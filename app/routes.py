from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for
from flask import request
from .forms import LoginForm, EditProfileForm, RegistrationForm, BlockListForm
from app import myapp_obj
from app import db
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from .models import User, Post, BlockList
# unique user id for profile image
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import uuid as uuid
#saving image
import os
#github api
import requests
import json
from github import Github

@myapp_obj.route('/')
@myapp_obj.route('/index')
def index():
    users = User.query.all()
    posts = Post.query.all()
    return render_template('index.html', users=users, posts=posts)

# @myapp_obj.route('/welcome', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         # future change will incorporate a simple textfile database and maybe a SQL database if provded time
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('index'))
#     return render_template('login.html', error=error)


@myapp_obj.route('/profile/<username>/')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('profile.html', user = user)


@myapp_obj.route('/editProfile/<section>/', methods=['GET', 'POST'])
@login_required
def edit_profile(section):
    form = EditProfileForm()

    if request.method == 'POST':
        if section == 'username':
            current_user.username   = form.username.data
        elif section == 'password':
            current_user.set_password(form.password.data)
        elif section == 'email':
            current_user.email      = form.email.data
        elif section == 'name':
            current_user.name      = form.name.data
        elif section == 'bio':
            current_user.bio        = form.bio.data
        elif section =='profilePic':
            current_user.profilePic = request.files['profilePic']
            picFilename = secure_filename(current_user.profilePic.filename)
            picName = str(uuid.uuid1()) +"_"+ picFilename
            saver = request.files['profilePic']
            
            current_user.profilePic = picName
            saver.save(os.path.join(myapp_obj.config['UPLOAD_FOLDER'], picName))

            

        db.session.commit()
        
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username = current_user.username))
    elif request.method == 'GET':
        form.username.data          = current_user.username
        form.email.data             = current_user.email
        form.name.data             = current_user.name
        form.bio.data               = current_user.bio
    return render_template('editProfile.html', title='Edit Profile', form=form, section=section)

# @app.route('/welcome', methods=['GET', 'POST'])
@myapp_obj.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user: {}, password: {}, remember_me={}'.format(form.username.data, form.password.data, form.remember_me.data))
        user = User.query.filter_by(username=form.username.data).first()
        # pass = User.query.filter_by(password=form.password.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password: {}'.format(user))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.name = form.name.data

        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@myapp_obj.route('/logout')
def logout():
    logout_user()
    flash('Sorry to see you go! Logging out...')
    return redirect(url_for('index'))

@myapp_obj.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete_user():
    userDelete = User.query.get_or_404(current_user.id)
    postDelete = Post.query.filter(Post.receive_id == current_user.id).delete()
    postDelete2 = Post.query.filter(Post.author_id == current_user.id).delete()
    db.session.delete(userDelete)
    db.session.commit()
    flash("Sorry to see you go! Deleting User & all Posts by and to User...")
    return redirect(url_for('index'))
    

@myapp_obj.route("/github/<string:username>/")
def connectGithub(username):
    # Github authentication
    token = "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"

    gh_session = requests.Session()
    gh_session.auth = (username , token)
    user = Github().get_user(username)

    repos = ''
    
    for repo in user.get_repos():
        repos += "#" + repo.full_name

        flash(repos)

    current_user.name           = user.name
    current_user.bio            = user.bio
    current_user.followers      = user.followers
    current_user.following      = user.following
    current_user.repositories   = user.public_repos
    current_user.repositories_name   = repos
    db.session.commit()
    
    @myapp_obj.route('/block', methods=['GET', 'POST'])
def block():
    form = BlockListForm()
    if form.validate_on_submit():
        blocked = BlockList(username = form.username.data)
        db.session.add(blocked)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('blocklist.html', title='BlockList', form=form)




    # user_data = requests.get(url).json()
    # flash(json.dumps(user_data))
    
    return redirect(url_for('profile', username=username))

@myapp_obj.route("/compose_email", methods=['GET', 'POST'])
def compose_email():
        return render_template('sendEmail.html')

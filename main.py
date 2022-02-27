import sqlite3
from time import strftime

from flask import url_for, redirect, session, request
import datetime
from __init__ import app, render_template, db, flash, oauth, ckeditor
from contact_form import MessageForm, MessageDatabase, Post, User, postdbs

user_login = False

email = None
name = "hello world!"


def getowner(id):
    owner = User.query.filter_by(id=id).first()
    return owner.name


def get_date(a):
    return a.strftime('%A, %B the %dth, %Y')


def deldelete(id):
    delete = postdbs.query.filter_by(id=id).first()
    user = User.query.filter_by(id=delete.owner).first()
    if email == user.email:
        db.session.delete(delete)
        db.session.commit()
    else:
        print('error')


@app.route('/')
def index():
    def isLoggedIn():
        x = session.get('profile')
        if x:
            return True
        else:
            return False

    global user_login
    user_login = isLoggedIn()
    if user_login:
        flash("hello ")
    all_post = postdbs.query.order_by(postdbs.date_posted.desc())
    return render_template('index.html', user=isLoggedIn(), posts=all_post, owner=getowner, time=get_date)


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()

    resp = google.get('userinfo').json()

    print(f'\n{resp["email"]}\n')
    session['profile'] = resp
    global email
    global name
    global user_login
    user_login = True
    name = resp['name']
    email = resp['email']

    x = User.query.filter_by(email=email).first()
    if x is not None:
        print(x)
        return redirect('/')
    else:
        user = User(name=resp['name'],
                    email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    # do something with the token and profile


@app.route('/about')
def about():
    return render_template('about.html', user=user_login)


@app.route('/test')
def test():
    return render_template('test.html', user=user_login)


@app.route('/post/<int:id>')
def post(id):
    show_post = postdbs.query.get_or_404(id)
    y = show_post.date_posted.strftime('%A, %B the %dth, %Y')
    return render_template('post.html', user=user_login, post=show_post,
                           owner=User.query.filter_by(id=show_post.owner).first(), time=y)


@app.route('/delete/<int:id>')
def delete(id):
    print('success')
    deldelete(id)
    redirect_uri = url_for('my_posts', _external=True)
    return redirect(redirect_uri)


@app.route('/my_posts')
def my_posts():
    if user_login:
        x = User.query.filter_by(email=email).first()
        my_posts = postdbs.query.filter_by(owner=x.id)

        return render_template('My posts.html', user=user_login, my_posts=my_posts, time=get_date, owner=getowner,
                               delete=delete)
    else:
        redirect_uri = url_for('login', _external=True)
        return redirect(redirect_uri)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if user_login:
        posts = Post()
        title = posts.title.data
        body = posts.body.data
        if request.method == 'POST':
            global email
            x = User.query.filter_by(email=email).first()
            print(x)
            postdb = postdbs(title=posts.title.data, body=posts.body.data, owner=x.id)
            db.session.add(postdb)
            db.session.commit()
            print("success!")

        return render_template('Add posts.html', form=posts, user=user_login, body=body, title=title)
    else:
        redirect_uri = url_for('login', _external=True)
        return redirect(redirect_uri)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    message = MessageForm()
    if message.validate_on_submit():
        messagesent = MessageDatabase(username=message.username.data, email_address=message.email_address.data
                                      , message=message.message.data)
        db.session.add(messagesent)
        db.session.commit()
        flash("Message Sent I will you contact you soon!", category='success')

    return render_template('contact.html', message=message, user=user_login)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.clear()

    global email
    email = None

    return redirect('/')


@app.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    if user_login:
        x = User.query.filter_by(email=email).first()
        return render_template('my_profile.html', users=x.name, user=user_login)
    else:
        redirect_uri = url_for('login', _external=True)
        return redirect(redirect_uri)


@app.route('/profile/<int:id>')
def profile(id):
    person = User.query.filter_by(id=id).first()

    if person.email == email:
        redirect_uri = url_for('my_profile', _external=True)
        return redirect(redirect_uri)


    else:
        return render_template('profile.html', person=person, user=user_login)


@app.route('/all_posts/<int:id>')
def all_posts(id):
    all_posts = postdbs.query.filter_by(owner=id)
    return render_template('all posts.html', all_posts=all_posts, owner=getowner, time=get_date, user=user_login)


if __name__ == '__main__':
    app.run(debug=True)

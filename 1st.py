from flask import Flask, render_template, request, session, redirect
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math


with open("config.json", "r") as c:
    params = json.load(c)["params"]
local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mj.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(120), nullable=False)
    msg = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(20), nullable=True)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(25), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    
@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(
        params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)


@app.route('/post/<string:post_slug>', methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/sample')
def sample():
    post = Posts.query.filter_by().first()
    return render_template('sample.html', params=params, post=post)


@app.route('/dashboard', methods=['GET', "POST"])
def login():
    if ('user' in session and session['user'] == params['admin_user']):
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)
    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)
    posts = Posts.query.all()
    return render_template('login.html', params=params, posts=posts)


@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if "user" in session and session['user'] == params['admin_user']:
        if request.method == "POST":
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            date = datetime.now()

            if sno == '0':
                post = Posts.query.filter_by(sno=sno).first()
                post = Posts(title=box_title, slug=slug,
                             content=content, tagline=tline, date=date)
                db.session.add(post)
                db.session.commit()
                return redirect('dashboard')
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.box_title = box_title
                post.tline = tline
                post.slug = slug
                post.content = content
                post.date = date
                db.session.commit()
                return redirect('/edit/' + sno)

        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post, sno=sno)


@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if "user" in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('dashboard')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')
        
        entry = Contacts(name=name, email=email,
                         phone_num=phone, msg=msg, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        
    return render_template('contact.html', params=params)


app.run(debug=True)

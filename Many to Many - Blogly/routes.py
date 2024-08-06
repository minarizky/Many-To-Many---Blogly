from flask import Flask, render_template, redirect, request, flash, jsonify
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

connect_db(app)
db.create_all()

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

@app.route('/tags/new', methods=["GET", "POST"])
def new_tag():
    if request.method == "POST":
        name = request.form['name']
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('tags/new.html')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == "POST":
        tag.name = request.form['name']
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/new', methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        tag_ids = request.form.getlist('tags')
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        for tag_id in tag_ids:
            post_tag = PostTag(post_id=new_post.id, tag_id=tag_id)
            db.session.add(post_tag)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    else:
        users = User.query.all()
        tags = Tag.query.all()
        return render_template('posts/new.html', users=users, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']
        tag_ids = request.form.getlist('tags')
        post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        db.session.commit()
        return redirect(f"/posts/{post_id}")
    else:
        tags = Tag.query.all()
        return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

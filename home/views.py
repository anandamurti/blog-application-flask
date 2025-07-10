from flask import current_app as app
from flask import render_template, redirect, flash, url_for, session, abort, request
from home.form import SetupForm
from app_init import db
from author.module import Author
from home.models import Blog
from author.decorators import login_required, author_required
from app_init import bcrypt
from home.models import Post, Category
from home.form import PostForm
from slugify import slugify
from flask import Blueprint
home_bp = Blueprint('home', __name__)
import os
from werkzeug.utils import secure_filename
from flask import current_app


@home_bp.route('/')
@home_bp.route('/index')
def index():
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('home.setup'))
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template('blog/index.html', blog=blog, posts=posts)


@home_bp.route('/admin')
@author_required
def admin():
    if session.get('is_author'):
        page = request.args.get('page', default=1, type=int)
        pagination = Post.query.order_by(Post.publish_date.desc()).paginate(page=page, per_page=5, error_out=False)
        posts = pagination.items
        return render_template('blog/admin.html', posts=posts, pagination=pagination)
    else:
        abort(403)


@home_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    print("Request method:", request.method)
    print("Request form:", request.form)
    print("Request files:", request.files)

    form = SetupForm(formdata=request.form, meta={'csrf': False})
    form.image.data = request.files.get('image')

    print("Form errors:", form.errors)

    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            author = Author(
                fullname=form.fullname.data,
                email=form.email.data,
                username=form.username.data,
                password=hashed_password,
                is_author=True
            )
            db.session.add(author)
            db.session.flush()

            blog = Blog(
                name=form.name.data,
                admin=author.id
            )
            db.session.add(blog)
            db.session.flush()

            file = request.files.get('file') or request.files.get('image')
            if file and file.filename:
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    blog.image = filename

            if author.id and blog.id:
                db.session.commit()
                flash("Blog created", "success")

                if app.config.get("TESTING"):
                    return "Blog created", 200

                return redirect(url_for('home.admin'))
            else:
                db.session.rollback()
                return "Unexpected error occurred", 500

        except Exception as e:
            db.session.rollback()
            flash("Something went wrong. Try again.", "danger")
            print("Exception:", e)
            return render_template("blog/error.html", error="Unexpected error occurred")

    return render_template("blog/setup.html", form=form)


@home_bp.route('/post', methods=['GET', 'POST'])
@author_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        if form.new_category.data:
            new_category = Category(name=form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        elif form.category.data:
            category = form.category.data
        else:
            category = None

        blog = Blog.query.first()
        username = session.get('username')
        if not username:
            flash("You must be logged in to post.", "danger")
            return redirect(url_for('author.login'))

        author = Author.query.filter_by(username=username).first()
        if not author:
            flash("Author not found.", "danger")
            return redirect(url_for('author.login'))

        title = form.title.data
        body = form.body.data
        slug = slugify(title) if title else None

        post = Post(
            blog_id=blog.id,
            author_id=author.id,
            title=title,
            body=body,
            slug=slug,
            category_id=category.id if category else None,
            live=True
        )

        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            author.image = filename
            post.image = filename

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home.article', slug=slug))

    return render_template('blog/post.html', form=form)

@home_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@author_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)  # Pre-fill form with existing post data

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data

        if form.new_category.data:
            new_category = Category(name=form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category_id = new_category.id
        elif form.category.data:
            post.category_id = form.category.data.id

        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post.image = filename

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('home.article', slug=post.slug))

    return render_template('blog/edit.html', form=form, post=post)



@home_bp.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@home_bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files.get('image')

        if not file or file.filename == '':
            flash('No selected file.', 'warning')
            return redirect(request.url)

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('Image uploaded successfully!', 'success')
            return redirect(url_for('home.index'))
        else:
            flash('Invalid file type. Only png, jpg, jpeg, gif allowed.', 'danger')
            return redirect(request.url)

    return render_template('blog/upload.html')


@home_bp.route('/delete/<int:post_id>')
@author_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Post deleted", "warning")
    return redirect(url_for('home.admin'))


@home_bp.route('/restore/<int:post_id>')
@author_required
def restore(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = True
    db.session.commit()
    flash("Post restored", "success")
    return redirect(url_for('home.admin'))

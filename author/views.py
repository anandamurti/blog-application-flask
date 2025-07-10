from flask import flash, render_template, request, redirect, url_for, session
from flask import current_app as app
from app_init import db, bcrypt
from author.form import RegisterForm, LoginForm
from author.module import Author
from sqlalchemy.exc import IntegrityError
from wtforms.validators import ValidationError
from author.decorators import login_required
from flask import Blueprint
author_bp = Blueprint('author', __name__)



@author_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(username=form.username.data).first()

        if author and bcrypt.check_password_hash(author.password, form.password.data):
            session['username'] = author.username
            session['is_author'] = author.is_author

            # Flash only once, right before redirecting to the actual UI page (admin)
            flash("Login successful!", "success")

            if 'next' in session:
                next_page = session.pop('next')
                return redirect(next_page)
            return redirect(url_for('home.index'))
        else:
            error = "Invalid username or password"
            flash(error, "danger")

    return render_template('author/login.html', form=form, error=error)


@author_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_author = Author(
            fullname=form.fullname.data,
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )

        try:
            db.session.add(new_author)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for("author.success"))
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists. Please choose another.", "danger")

    return render_template("author/register.html", form=form)

@author_bp.route("/success")
def success():
    return "Author registered!"


@author_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_author')
    flash("You have been logged out.", "info")
    return redirect(url_for('home.index'))

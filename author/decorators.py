from functools import wraps
from flask import session, request, redirect, url_for, flash, abort
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_author'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
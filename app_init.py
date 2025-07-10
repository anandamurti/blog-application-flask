import os
from flask import Flask
from flask import flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import markdown
from markupsafe import Markup
from datetime import datetime, timezone
from werkzeug.exceptions import RequestEntityTooLarge


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')

     # Template global
    app.jinja_env.globals['current_year'] = datetime.now(timezone.utc).year

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        flash("File too large! Max size is 5MB.", "danger")
        return redirect(request.url)


    @app.template_filter('markdown')
    def markdown_filter(text):
        return Markup(markdown.markdown(text))

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Import routes AFTER app is created to avoid circular import
    from home.views import home_bp
    from author.views import author_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(author_bp)

    return app

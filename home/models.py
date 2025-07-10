from datetime import datetime
from app_init import db
from author.module import Author
from flask import url_for





class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))
    posts = db.relationship('Post', back_populates='blog', lazy='dynamic')

    # Relationship to Author
    admin_user = db.relationship('Author', backref='blogs', lazy=True)

    def __repr__(self):
        return f'<Blog {self.name}>'


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(256))
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    live = db.Column(db.Boolean, nullable=False, default=False)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Relationships
    blog = db.relationship('Blog', back_populates='posts', lazy=True)
    category = db.relationship('Category', backref='posts', lazy=True)

    @property
    def image_url(self):
        if self.image:
            return url_for('static', filename='uploads/' + self.image)
        return None
    

    def __repr__(self):
        return f'<Post {self.title}>'


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f'<Category {self.name}>'
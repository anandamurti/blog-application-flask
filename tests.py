import unittest
import sqlalchemy
import uuid
import io
from app_init import create_app, db
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import create_engine, text


class UserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # ✅ Globally disables CSRF during tests

        # Setup test DB
        db_username = self.app.config['DB_USERNAME']
        db_password = self.app.config['DB_PASSWORD']
        db_host = self.app.config['DB_HOST']
        self.db_uri = f"mysql+pymysql://{db_username}:{db_password}@{db_host}"
        self.app.config['BLOG_DATABASE_NAME'] = 'blog_test'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f"{self.db_uri}/{self.app.config['BLOG_DATABASE_NAME']}"

        # Create the test database
        engine = create_engine(self.db_uri)
        conn = engine.connect()
        conn.execution_options(isolation_level="AUTOCOMMIT")
        try:
            conn.execute(text(f"CREATE DATABASE {self.app.config['BLOG_DATABASE_NAME']}"))
        except ProgrammingError:
            pass  # Already exists
        conn.close()

        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()

        engine = create_engine(self.db_uri)
        conn = engine.connect()
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"DROP DATABASE IF EXISTS {self.app.config['BLOG_DATABASE_NAME']}"))
        conn.close()

    def create_blog(self):
        image_file = (io.BytesIO(b"fake image content"), "test.jpg")
        return self.client.post(
            '/setup',
            data={
                'name': 'Test Blog',
                'fullname': 'Test User',
                'email': f"{uuid.uuid4().hex[:20]}@ex.com",
                'username': f"user_{uuid.uuid4().hex[:10]}",
                'password': '12345',
                'confirm': '12345',
                'image': image_file
            },
            content_type='multipart/form-data',
            follow_redirects=True
        )

    def test_create_blog(self):
        rv = self.create_blog()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Blog created', rv.data)


if __name__ == '__main__':
    unittest.main()

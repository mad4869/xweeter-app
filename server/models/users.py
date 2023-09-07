from datetime import datetime

from .. import db, bcrypt


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text())
    role = db.Column(db.String(50), nullable=False)
    profile_pic = db.Column(db.Text())
    header_pic = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "bio": self.bio,
            "role": self.role,
            "profile_pic": self.profile_pic,
            "header_pic": self.header_pic,
            "created_at": self.created_at,
        }

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def password_auth(self, password_input):
        return bcrypt.check_password_hash(self.password_hash, password_input)

    def __repr__(self):
        return f"{self.username}"

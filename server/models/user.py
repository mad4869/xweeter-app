from datetime import datetime

from .. import db, bcrypt, mc
from .follow import follow

BUCKET = "xweeter"


def get_default_pfp():
    return mc.presigned_get_object(BUCKET, "default_pfp.jpg")


def get_default_header():
    return mc.presigned_get_object(BUCKET, "default_header.png")


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text())
    role = db.Column(db.String(50), nullable=False, default="user")
    profile_pic = db.Column(db.Text(), default=get_default_pfp())
    header_pic = db.Column(db.Text(), default=get_default_header())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime())
    xweets = db.Relationship(
        "Xweet", backref="users", lazy=True, cascade="all, delete-orphan"
    )
    followed = db.Relationship(
        "User",
        secondary=follow,
        primaryjoin=("User.user_id == follows.c.follower_id"),
        secondaryjoin=("User.user_id == follows.c.followed_id"),
        backref=db.backref("users", lazy="dynamic"),
        lazy="dynamic",
    )
    replies = db.Relationship(
        "Reply", backref="users", lazy=True, cascade="all, delete-orphan"
    )
    rexweets = db.Relationship(
        "Rexweet", backref="users", lazy=True, cascade="all, delete-orphan"
    )
    likes = db.Relationship(
        "Like", backref="users", lazy=True, cascade="all, delete-orphan"
    )

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
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.updated_at
            else self.updated_at,
        }

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def password_auth(self, password_input):
        return bcrypt.check_password_hash(self.password_hash, password_input)

    def __repr__(self):
        return f"{self.username}"
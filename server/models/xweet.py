from datetime import datetime

from .hashtag_xweet import hashtag_xweet
from .. import db


class Xweet(db.Model):
    __tablename__ = "xweets"
    xweet_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    body = db.Column(db.String(140), nullable=False)
    media = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime())
    users = db.Relationship("Users", back_populates="xweets")
    replies = db.Relationship(
        "Reply", back_populates="replies", lazy=True, cascade="all, delete-orphan"
    )
    rexweets = db.Relationship(
        "Rexweet", back_populates="rexweets", lazy=True, cascade="all, delete-orphan"
    )
    likes = db.Relationship(
        "Like", back_populates="likes", lazy=True, cascade="all, delete-orphan"
    )
    hashtags = db.Relationship(
        "Hashtag",
        secondary=hashtag_xweet,
        backref="xweets",
        lazy="dynamic",
    )

    def serialize(self):
        return {
            "xweet_id": self.xweet_id,
            "user_id": self.user_id,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return f"{self.body}"

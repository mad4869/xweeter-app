from datetime import datetime

from .. import db


class Xweets(db.Model):
    __tablename__ = "xweets"
    xweet_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    body = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime())
    users = db.Relationship("Users", back_populates="xweets")
    replies = db.Relationship(
        "Replies", back_populates="xweets", lazy=True, cascade="all, delete-orphan"
    )
    rexweets = db.Relationship(
        "Rexweets", back_populates="xweets", lazy=True, cascade="all, delete-orphan"
    )
    likes = db.Relationship(
        "Likes", back_populates="xweets", lazy=True, cascade="all, delete-orphan"
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

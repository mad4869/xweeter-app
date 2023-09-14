from datetime import datetime

from .. import db


class Reply(db.Model):
    __tablename__ = "replies"
    reply_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    xweet_id = db.Column(db.Integer(), db.ForeignKey("xweets.xweet_id"))
    body = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime())
    users = db.Relationship("User", back_populates="replies")
    xweets = db.Relationship("Xweet", back_populates="replies")

    def serialize(self):
        return {
            "reply_id": self.like_id,
            "user_id": self.user_id,
            "xweet_id": self.xweet_id,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return f"{self.body}"

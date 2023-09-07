from datetime import datetime

from .. import db


class Xweets(db.Model):
    __tablename__ = "xweets"
    xweet_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    body = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def serialize(self):
        return {
            "xweet_id": self.xweet_id,
            "user_id": self.user_id,
            "body": self.body,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return f"{self.body}"

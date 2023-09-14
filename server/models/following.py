from datetime import datetime

from .. import db


class Following(db.Model):
    __tablename__ = "followings"
    following_id = db.Column(db.Integer(), primary_key=True)
    followed_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    follower_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime())

    def serialize(self):
        return {
            "following_id": self.following_id,
            "followed_id": self.followed_id,
            "follower_id": self.follower_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return f"{self.follower_id} follows {self.followed_id}"

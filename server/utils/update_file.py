from datetime import datetime, timedelta

from ..extensions import db, mc
from ..models import User, Xweet
from ..constants import MINIO_BUCKET


def set_new_url(data, name_col, url_col):
    for item in data:
        new_url = mc.presigned_get_object(MINIO_BUCKET, getattr(item, name_col))

        setattr(item, url_col, new_url)


def update_file_url():
    users = db.session.execute(db.select(User)).scalars()
    xweets = db.session.execute(db.select(Xweet)).scalars()

    outdated_pfp_data = []
    outdated_header_data = []
    outdated_media_data = []

    for user in users:
        if user.profile_pic_updated_at <= datetime.now() - timedelta(days=7):
            outdated_pfp_data.append(user)
        if user.header_pic_updated_at <= datetime.now() - timedelta(days=7):
            outdated_header_data.append(user)

    for xweet in xweets:
        if (
            xweet.media_updated_at
            and xweet.media_updated_at <= datetime.now() - timedelta(days=7)
        ):
            outdated_media_data.append(xweet)

    try:
        set_new_url(outdated_pfp_data, "profile_pic_name", "profile_pic")
        set_new_url(outdated_header_data, "header_pic_name", "header_pic")
        set_new_url(outdated_media_data, "media_name", "media")

        db.session.commit()
    except:
        db.session.rollback()

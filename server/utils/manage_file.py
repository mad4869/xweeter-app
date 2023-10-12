import base64
import io
import uuid
import imghdr


def manage_file(media_url):
    media_data = base64.b64decode(media_url.split(",")[1])
    media_stream = io.BytesIO(media_data)
    media_id = uuid.uuid4()
    media_ext = imghdr.what(media_stream)
    OBJECT_NAME = f"{media_id}.{media_ext}"

    return media_data, media_stream, OBJECT_NAME

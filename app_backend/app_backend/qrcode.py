from io import BytesIO
import urllib.parse
import qrcode
from app_backend import app
from flask import request, send_file


def create_qr(data: str) -> BytesIO:
    """generate png qr code as byte stream"""
    qr = qrcode.make(data)
    byte_stream = BytesIO()
    qr.save(byte_stream, "PNG")
    byte_stream.seek(0)
    return byte_stream


@app.route("/")
def test():
    return "running"


@app.route("/createQR", methods=["POST"])
def return_qr():
    """return qr code for the url given in the request"""
    request_data = request.get_json()
    url_str = request_data["url"]
    url_str = urllib.parse.quote(url_str)
    byte_stream = create_qr(url_str)
    return send_file(byte_stream, download_name="qr.png", mimetype="image/png")

import unittest
from PIL import Image
from app_backend import qrcode_gen

qrcode_gen.app.testing = True


class TestApp(unittest.TestCase):
    def test_return_qr(self):
        """qr png file returned"""
        post = {"url": "www.hello.com"}
        test_file = tempfile.NamedTemporaryFile()
        with qrcode_gen.app.test_client() as client:
            result = client.post("/createQR", json=post)
            assert result.status_code == 200
            assert result.headers["Content-Type"] == "image/png"

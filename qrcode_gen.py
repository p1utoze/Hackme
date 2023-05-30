from qrcode.image.pil import PilImage
import qrcode
q = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q,
                          box_size=1, border=1)
q.add_data("https://api.apis.guru/v2/list.json")
q.make(fit=True)
img = q.make_image(image_factory=PilImage)
img.save("api_guru.png")
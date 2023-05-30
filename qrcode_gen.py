from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
# from qrcode.main import s
# import pandas as pd
# df = pd.read_csv("teams.csv")
# names = df.groupby(len)['First Name']
# print(names)
q = qrcode.QRCode(version=4, error_correction=qrcode.constants.ERROR_CORRECT_H,
                          box_size=3, border=5)
q.add_data("https://testaventus-adityanawati.b4a.run/scan_qr/?uid=WEB01-01")
q.make(fit=True)
img = q.make_image(fill_color="#3A81AB", back_color="white").convert('RGB')
logo = Image.open("../../Pictures/juice wrld/DoggoWRLD.jpeg")
qr_width, qr_height = img.size
# center_size = int(qr_width * 0.25)  # Adjust the percentage as needed
# logo = logo.resize((center_size, center_size))
draw = ImageDraw.Draw(img)
font_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 'static/Michroma/Michroma-Regular.ttf'
    )
)
font = ImageFont.truetype(font=font_path, size=10)
# draw.text((qr_width - (qr_width * 0.10), qr_height - (qr_height * 0.10)), "", font=font, fill=(0,0,0,1))
draw.text((qr_width - (qr_width * 0.95), qr_height - (qr_height * 0.09)), "WEB01-01  Jayavibhav", font=font, fill=(0,0,0,1))
# pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
# img.paste(logo, pos)
print()
img.save("WEB01-01.png")


from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
# from qrcode.main import s
import pandas as pd

df = pd.read_csv("Final_List.csv")

def generate_qr(uid, fname):
    name = fname.split()
    fname = name[0]
    q = qrcode.QRCode(version=4, error_correction=qrcode.constants.ERROR_CORRECT_H,
                              box_size=3, border=5)
    q.add_data(f"https://aventus-hackaventus.b4a.run/qr_scan/?uid={uid}")
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white").convert('RGB')
    logo = Image.open("../../Pictures/juice wrld/DoggoWRLD.jpeg")
    draw = ImageDraw.Draw(img)
    qr_width, qr_height = img.size
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 'static/Michroma/Michroma-Regular.ttf'
        )
    )
    font = ImageFont.truetype(font=font_path, size=9)
    # draw.text((qr_width - (qr_width * 0.10), qr_height - (qr_height * 0.10)), "", font=font, fill=(0,0,0,1))
    draw.text((qr_width - (qr_width * 0.91), qr_height - (qr_height * 0.09)), "{0}  {1}".format(uid, fname), font=font,
              fill=(0, 0, 0, 1))
    print(f"{uid}")
    img.save(f"qrcodes/{uid}.png")


for uid, fname in zip(df["UID"].to_list(), df["firstName"].to_list()):
    generate_qr(uid, fname)
# center_size = int(qr_width * 0.25)  # Adjust the percentage as needed
# logo = logo.resize((center_size, center_size))

# pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
# img.paste(logo, pos)



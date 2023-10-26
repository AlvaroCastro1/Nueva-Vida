import qrcode

input = "https://www.youtube.com/watch?v=UMvQAyJrV6c"

qr = qrcode.QRCode(version=1,box_size=10, border=5) 

qr.add_data(input)
qr.make(fit=True)

img = qr.make_image(fill='black',back_color='white')
img.save('you.png')
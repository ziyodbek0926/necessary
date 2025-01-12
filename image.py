#rasmlarni formatini o'zgartirish uchun code


from PIL import Image

image_path = "/mnt/data/image.jpg"
img = Image.open(image_path)

resized_img = img.resize((640, 360))

resized_image_path = "/mnt/data/resized_image_640x360.jpg"
resized_img.save(resized_image_path)

resized_image_path

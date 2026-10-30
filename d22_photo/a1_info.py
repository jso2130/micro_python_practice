from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"

img = Image.open(PHOTO)            # Image클래스를 이용해 사진을 객체에 담는다
print("가로", img.width, "픽셀")
print("세로", img.height, "픽셀")
print("픽셀의 개수", img.width * img.height, "개")
print("색 방식", img.mode)

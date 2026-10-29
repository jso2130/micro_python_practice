from PIL import Image

# ---- 내가 바꾸는 값 ----
PHOTO = "cat.jpg"
X = 300                          # 가로로 몇 번째 픽셀 (0 부터)
Y = 200                          # 세로로 몇 번째 픽셀 (0 부터)

img = Image.open(PHOTO)          # 사진을 열어 img 라는 이름표를 붙인다
r, g, b = img.getpixel((X, Y))   # img.getpixel : (X, Y) 자리 픽셀의 숫자 3개를 r, g, b 에 하나씩 담는다
print("픽셀", (X, Y), "의 색 : 빨강", r, "초록", g, "파랑", b)

gray = img.convert("L")          # 흑백 사진으로 바꾼다 (L = 밝기). 0 ~ 255
print("같은 픽셀의 흑백 밝기 :", gray.getpixel((X, Y)))

print("이 픽셀 주변 5 x 5 칸의 흑백 밝기 :")
for dy in range(5):              # 5개의 행.
    row = []                     # 한 행의 열값들을 담아 줄 빈 배열 생성
    for dx in range(5):          # 5개의 열.
        row.append(gray.getpixel((X + dx, Y + dy)))   # 빈 배열(row)에 열 값 5개를 순서대로 추가한다.
    print(row)                   # 안쪽 반복이 끝나 상자에 5개가 차면 한 줄을 찍는다

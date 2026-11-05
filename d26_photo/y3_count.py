from ultralytics import YOLO            # ultralytics 도구 상자에서 YOLO 하나만 꺼낸다

# ---- 내가 바꾸는 값 ----
PHOTO = ("street.jpg")
WANT = "person"                         # 세고 싶은 물체의 이름 (person · car · dog · chair · orange …)
CONF = 0.25                             # 물체로 잡을 신뢰도 기준

model = YOLO("yolo26n.pt")
results = model(PHOTO, conf=CONF)
result = results[0]                     # 가장 신뢰도가 높은 것만 가져온다.

count = 0
for box in result.boxes:
    name = result.names[int(box.cls[0])]        # 결과에 맞는 이름을 목록(Tensor)에서 가져온다
    if name == WANT:                            # 신뢰도가 가장 높은 결과가 찾고싶은 물체라면
        count = count + 1

print(PHOTO, "에서", WANT, "는", count, "개")     # 판독한 사진 이름, 세고 싶은 물체 이름, 찾은 물체 개수
result.save("yolo_count.jpg")

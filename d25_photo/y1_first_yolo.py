from ultralytics import YOLO

# ---- 내가 바꾸는 값 ----
PHOTO = ("desk.jpg")
model = YOLO("yolo26n.pt")              #
results = model(PHOTO)                  # model 에 사진을 건네면 YOLO 의 답 묶음(results)이 돌아온다
result = results[0]                     # 가장 높은 확률값만 가져온다

print("찾은 물체의 개수 :", len(result.boxes))
for box in result.boxes:
    name = result.names[int(box.cls[0])]        # 확률이 높은 것의 이름 찾아온다.
    confidence = float(box.conf[0])             # 확률값을 실수로 가져온다.
    print(name, round(confidence, 2))           # 이름과 자신감을 소수 둘째 자리까지 보여 준다

result.save("yolo_result.jpg")          # 네모를 그린 사진을 yolo_result.jpg 파일로 저장한다
print("yolo_result.jpg 로 저장했다")

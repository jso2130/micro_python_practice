from ultralytics import YOLO            # ultralytics 도구 상자에서 YOLO 하나만 꺼낸다

# ---- 내가 바꾸는 값 ----
PHOTO = "moto.jpg"                    # 같은 폴더에 있는 사진 이름 (따옴표 안에 쓴다)
CONF = 0.1
IOU = 0.95                              # 겹침 기준 : 네모 둘이 이 숫자 이상 겹치면 같은 물체로 보고 자신감 높은 쪽만 남긴다 (0 ~ 1 사이)

model = YOLO("yolo26n.pt")              # 가장 작은 YOLO 파일을 불러와 model 이라는 이름을 붙인다
results = model(PHOTO, conf=CONF, iou=IOU)      # 사진을 보여 준다 : 왼쪽 conf·iou 는 YOLO 가 정한 이름, 오른쪽은 내 숫자
result = results[0]                     # 답 묶음의 0번째 = 사진 한 장에 대한 답


print("겹침 기준", IOU, "→ 찾은 물체의 개수 :", len(result.boxes))     # len : 정리하고 남은 네모의 수

obj_cnts = {}                               # 검출된 물체의 종류별 숫자를 담을 딕셔너리
for box in result.boxes:
    name = result.names[int(box.cls[0])]        # 이름 번호(정수)를 이름 목록에서 찾아 글자로 바꾼다
    confidence = float(box.conf[0])             # 이 네모의 자신감 (0 ~ 1 사이 소수)
    print("   ", name, round(confidence, 2))    # 이름과 자신감을 소수 둘째 자리까지 쓴다

    if name in obj_cnts:
        obj_cnts[name] += 1                 # 딕셔너리에 이름이 있으면 숫자를 더하고
    else:
        obj_cnts[name] = 1                  # 이름이 없으면 추가한다.

for name,count in obj_cnts.items():
    print(f"{name}:{count}개")

result.save("yolo_iou_95.jpg")             # 네모를 그린 사진을 파일로 저장한다
print("yolo_iou.jpg 로 저장했다")

import cv2

cam_no = 0
capture = cv2.VideoCapture(cam_no)
fps = capture.get(cv2.CAP_PROP_FPS)
print('fps: ' + str(fps))

ret, frame = capture.read()
img = frame.copy()
height = img.shape[0]
width = img.shape[1]

roi_size = 200
roi_x1 = int(width/2 - roi_size/2)
roi_y1 = int(height/2 - roi_size/2)
roi_x2 = roi_x1 + roi_size
roi_y2 = roi_y1 + roi_size
green = (0,255,0)
thick = 15

cv2.rectangle(img, (roi_x1, roi_y1), (roi_x2,roi_y2),green,thick)

cv2.imshow('image', img)  # 윈도우 창에 이미지 표시
cv2.waitKey(0)

tracker = cv2.TrackerCSRT_create()
roi = (roi_x1, roi_y1, roi_x2-roi_x1, roi_y2-roi_y1)
print('ROI x, y, w, h:' + str(roi))
tracker.init(frame,roi)

while True:
    ret, frame = capture.read()
    
    # 컬러 이미지로 변환
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    isFound, foundBox = tracker.update(frame)
    if (isFound) :
        found_x1 = int(foundBox[0])
        found_y1 = int(foundBox[1])
        found_x2 = int(foundBox[0] + foundBox[2])
        found_y2 = int(foundBox[1] + foundBox[3])
        
        font = cv2.FONT_HERSHEY_SIMPLEX  # 폰트 지정
        text = "Object location: ({}, {}), ({}, {})".format(found_x1, found_y1, found_x2, found_y2)  # 표시할 문자열
        textsize = cv2.getTextSize(text, font, 1, 2)[0]  # 텍스트 크기 계산

# 텍스트 위치 계산
        text_x = found_x1 + int((foundBox[2] - textsize[0]) / 2)
        text_y = found_y1 + int((foundBox[3] + textsize[1]) / 2)

        cv2.rectangle(frame, (found_x1, found_y1), (found_x2, found_y2), green, thick)
        
        cv2.putText(frame, text, (text_x, text_y), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # 다시 BGR 형식으로 변환하여 윈도우 창에 표시
        cv2.imshow('image', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        cv2.waitKey(1)

capture.release()
cv2.destroyAllWindows()



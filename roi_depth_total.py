import pyrealsense2 as rs
import numpy as np
import time
import matplotlib.pyplot as plt

# RealSense pipeline 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth,  1280, 720, rs.format.z16, 30)

# ROI 설정
roi_x = 850  # ROI 시작 x 좌표
roi_y = 300  # ROI 시작 y 좌표
roi_width = 400  # ROI 가로 길이
roi_height = 220  # ROI 세로 길이

# RealSense 시작
pipeline.start(config)

try:
    while True:
        # RealSense에서 프레임 가져오기
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # 프레임이 없으면 건너뜀
        if not depth_frame:
            continue

        # numpy 배열로 변환
        depth_image = np.asanyarray(depth_frame.get_data())

        # ROI 설정
        roi = depth_image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # 처리 또는 저장
        # 이 예제에서는 간단하게 최소, 최대, 평균값 출력
        min_depth = np.min(depth_image)
        max_depth = np.max(depth_image)
        avg_depth = np.mean(depth_image)

        min_depth = 500#600  # 최소 깊이
        max_depth = 1000#1000  # 최대 깊이
        depth_filtered = np.where((depth_image >= min_depth) & (depth_image <= max_depth), depth_image, 0)

        print("Minimum depth in ROI: ", min_depth)
        print("Maximum depth in ROI: ", max_depth)
        # print("Average depth in ROI: ", avg_depth)

        # ROI 시각화
        plt.imshow(depth_filtered, cmap='jet')
        plt.colorbar()
        plt.show()

        # 1초 대기
        time.sleep(1)

finally:
    # RealSense 종료
    pipeline.stop()

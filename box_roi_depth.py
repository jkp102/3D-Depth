import pyqt5_tools
print(pyqt5_tools.__file__)
import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt
import time

# 스케일링 요인
scaling_factor = 1.0 / 1.0  # 스케일링 요인 계산하여 설정 (예: 1.0 / 1000.0)

# RealSense 파이프라인 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

# roi_x = 580  # ROI 시작 x 좌표
# roi_y = 360  # ROI 시작 y 좌표
# roi_width = 180  # ROI 가로 길이
# roi_height = 110  # ROI 세로 길이

roi_x = 484  # ROI 시작 x 좌표
roi_y = 263  # ROI 시작 y 좌표
roi_width = 374  # ROI 가로 길이
roi_height = 200  # ROI 세로 길이

# RealSense 시작
pipeline.start(config)

# 초기 깊이 이미지 생성
depth_image = np.zeros((roi_height, roi_width))
# 이미지 플롯 설정
fig, ax = plt.subplots()
flipped_image = np.fliplr(depth_image)  # 이미지 배열 좌우로 반전
im = ax.imshow(flipped_image, cmap='jet', vmin=700, vmax=1000, origin='lower')  # origin 값을 'lower'로 설정
ax.invert_xaxis()  # x축 좌우 반전
plt.colorbar(im)

try:
    min_depth_text = None  # 이전 텍스트 객체를 저장하기 위한 변수
    while True:
        # RealSense에서 프레임 가져오기
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # 프레임이 없으면 건너뜀
        if not depth_frame:
            continue

        # 깊이 데이터를 넘파이 배열로 변환
        depth_image = np.asanyarray(depth_frame.get_data())

        # ROI 내 모든 위치에 대한 깊이 값 측정
        roi_depth_values = depth_image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # 깊이 값이 0인 픽셀 제외
        roi_depth_values = roi_depth_values.astype(float)  # float 형식으로 변환
        roi_depth_values[roi_depth_values == 0] = np.nan

        # 스케일링 요인 적용
        roi_depth_values *= scaling_factor

        # 예외 처리: 최댓값이 65535인 경우는 제외하고 가장 낮은 유효한 깊이 값 출력
        valid_depth_values = roi_depth_values[roi_depth_values < 65535]
        min_depth = np.nanmin(valid_depth_values)
        min_depth_indices = np.where(roi_depth_values == min_depth)
        min_depth_x = min_depth_indices[1][0]
        min_depth_y = min_depth_indices[0][0]
        print("가장 낮은 유효한 깊이 값:", min_depth)
        print("최소 깊이 좌표 (x, y):", min_depth_x, min_depth_y)
        
        # 이미지 업데이트
        roi_depth_values[roi_depth_values <= 700] = np.nan
        roi_depth_values[roi_depth_values >= 1000] = np.nan
        im.set_array(roi_depth_values)

        # 이전 텍스트 객체 삭제
        if min_depth_text is not None:
            min_depth_text.remove()

        # 좌표 및 높이 텍스트 포맷팅
        text = f"({min_depth_x}, {min_depth_y}), Depth: {min_depth}"

        # 좌표 텍스트 추가
        min_depth_text = ax.annotate(text, xy=(min_depth_x, min_depth_y),
                                     xytext=(min_depth_x + 10, min_depth_y + 10),
                                     color='black', weight='bold', fontsize=8,
                                     arrowprops=dict(arrowstyle='->', color='black'))
        
# 1초 대기
        time.sleep(1)
        # 창 업데이트
        plt.draw()
        plt.pause(0.001)

finally:
    # RealSense 종료
    pipeline.stop()

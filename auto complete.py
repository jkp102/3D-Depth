import tkinter as tk
from pymodbus.client import ModbusTcpClient
import struct
import time
import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt
import ctypes
# 스케일링 요인
scaling_factor = 1.0 / 1.0  # 스케일링 요인 계산하여 설정 (예: 1.0 / 1000.0)

# RealSense 파이프라인 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

roi_x = 520  # ROI 시작 x 좌표
roi_y = 300  # ROI 시작 y 좌표
roi_width = 330  # ROI 가로 길이
roi_height = 190  # ROI 세로 길이

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

def write_values(x_off, y_off, z_off, yaw_off, pitch_off, roll_off, sig_pick, sig_place, sig_Auto):
    try:
        x_off = float(x_off_entry.get()) if x_off_entry.get() != '' else 0.0
        y_off = float(y_off_entry.get()) if y_off_entry.get() != '' else 0.0
        z_off = float(z_off_entry.get()) if z_off_entry.get() != '' else 0.0
        yaw_off = float(yaw_off_entry.get()) if yaw_off_entry.get() != '' else 0.0
        pitch_off = float(pitch_off_entry.get()) if pitch_off_entry.get() != '' else 0.0
        roll_off = float(roll_off_entry.get()) if roll_off_entry.get() != '' else 0.0
        sig_pick = float(sig_pick_entry.get()) if sig_pick_entry.get() != '' else 0.0
        sig_place = float(sig_place_entry.get()) if sig_place_entry.get() != '' else 0.0
        sig_Auto = float(sig_place_entry.get()) if sig_place_entry.get() != '' else 0.0
        

    except ValueError:
        print("잘못된 값입니다. 숫자를 입력해주세요.")
        return
    # Holding Register (주소 0부터 시작)에서 다중 데이터 읽기
    result = client.read_holding_registers(address=9000, count=23)

    if not result.isError():
        print("다중 데이터 읽기 값:", result.registers)
    else:
        print("데이터 읽기 오류:", result)
        
    # values = [x_off, y_off, z_off, yaw_off, pitch_off, roll_off, sig_pick, sig_place, sig_home, sig_ready, sig_complete ]
        values = [x_off, y_off, z_off, yaw_off, pitch_off, roll_off, sig_pick, sig_place, sig_Auto]
        byte_values = []
        for value in values:
            byte_value = struct.pack('!f', value)
            byte_values.extend(struct.unpack('!HH', byte_value))

        result = client.write_registers(address=9001, values=byte_values)
        if not result.isError():
            print("다중 데이터 쓰기 성공")
        else:
            print("데이터 쓰기 오류:", result)

        values = [sig_Auto ]
        byte_values = []
        for value in values:
            byte_value = struct.pack('!f', value)
            byte_values.extend(struct.unpack('!HH', byte_value))
        result = client.write_registers(address=9023, values=[byte_values])
        if not result.isError():
            print("다중 데이터 쓰기 성공")
        else:
            print("데이터 쓰기 오류:", result)

    
    
# UI 생성
window = tk.Tk()
window.title("Modbus UI")
window.geometry("600x800")

# Modbus TCP IP 주소 입력
ip_label = tk.Label(window, text="Modbus TCP IP 주소:")
ip_label.pack()
ip_entry = tk.Entry(window)
ip_entry.pack()

# x_off 입력
x_off_label = tk.Label(window, text="x_off:")
x_off_label.pack()
x_off_entry = tk.Entry(window)
x_off_entry.pack()

# y_off 입력
y_off_label = tk.Label(window, text="y_off:")
y_off_label.pack()
y_off_entry = tk.Entry(window)
y_off_entry.pack()

# z_off 입력
z_off_label = tk.Label(window, text="z_off:")
z_off_label.pack()
z_off_entry = tk.Entry(window)
z_off_entry.pack()

# yaw_off 입력
yaw_off_label = tk.Label(window, text="yaw_off:")
yaw_off_label.pack()
yaw_off_entry = tk.Entry(window)
yaw_off_entry.pack()

# pitch_off 입력
pitch_off_label = tk.Label(window, text="pitch_off:")
pitch_off_label.pack()
pitch_off_entry = tk.Entry(window)
pitch_off_entry.pack()

# roll_off 입력
roll_off_label = tk.Label(window, text="roll_off:")
roll_off_label.pack()
roll_off_entry = tk.Entry(window)
roll_off_entry.pack()

def connect():
    ip_address = ip_entry.get()  # ip_entry는 UI 창에서 IP 주소를 입력 받는 필드입니다.

    # Modbus TCP 서버에 연결
    global client
    client = ModbusTcpClient(host=ip_address, port=502)
    client.connect()

    result = client.read_holding_registers(address=9000, count=23)
    
    
    # sig_home 값을 확인해보기
    if result.registers[17] == 1:
        print("sig_home",result.registers[17])
    else:
        print("sig_home is zero.",result.registers[17])
###########################################################################################        
    # sig_ready 값을 확인해보기
    if result.registers[19] == 1:
        print("sig_ready",result.registers[19])

    else:
        print("sig_ready is zero.",result.registers[19])
##########################################################################################        
    if result.registers[21] == 1:
        print("com",result.registers[21])
    else:
        print("com is zero.",result.registers[21])

    # 값을 전송하는 버튼
    send_button = tk.Button(window, text="Send Values", command=write_values)
    send_button.pack()
# 연결 버튼
connect_button = tk.Button(window, text="Connect", command=connect)
connect_button.pack()

def repeat_action():
    
    window.after(1000, repeat_action)
def toggle_sig_Auto():
    global client
    current_value = sig_Auto_button["text"]
    while current_value == "Auto ON":
        print("auto on")
        sig_Auto_button["text"] = "Auto OFF"
        sig_Auto_entry.delete(0, tk.END)
        sig_Auto_entry.insert(0, str(1.0))
        result = client.write_registers(address=9023, values=[1])
        result = client.read_holding_registers(address=9000, count=23)
        print("pick16_home",result.registers[17]) # 사진 픽쳐 시그널
        print("pick18_raedy",result.registers[19])
        print("pick18_com",result.registers[21])
        result = client.write_registers(address=9013, values=[1])
        result = client.write_registers(address=9015, values=[1])
        
        result = client.read_holding_registers(address=9001, count=23)
        if result.registers[16] == 1:
            print("home == 1")
            get_min_depth()  # 최소 깊이 값을 가져오고 min_depth_value 변수에 저장
            print("1",float(min_depth_value))
            values = [1172 -float(min_depth_value)]
# # 실수 값을 바이트로 변환하여 전송
            byte_values = []
            print(type(values))
            for value in values:
                byte_value = struct.pack('!f', value)
                byte_values.extend(struct.unpack('!HH', byte_value))
            result = client.write_registers(address=9005, values=byte_values)
            time.sleep(0.5)
            
        
        repeat_action()
        
    else:
        print("auto off")
        sig_Auto_button["text"] = "Auto ON"
        sig_Auto_entry.delete(0, tk.END)
        sig_Auto_entry.insert(0, str(0.0))
        result = client.write_registers(address=9023, values=[0])
######## pick off ######################################################################################################        
        result = client.write_registers(address=9013, values=[0])
        result = client.write_registers(address=9015, values=[0])
##############################################################################################################         
      
##############################################################################################################        
sig_Auto_button = tk.Button(window, text="Auto ON", command=toggle_sig_Auto)


sig_Auto_button.pack()
sig_Auto_entry = tk.Entry(window)
sig_Auto_entry.pack()   
# 연결 버튼과 repeat_action 함수 호출 추가
connect_button = tk.Button(window, text="Connect", command=connect)
connect_button.pack()

# RealSense 데이터 가져오기 위한 함수 호출
# repeat_action()
def toggle_sig_pick():
    try:
        global client
        current_value = sig_pick_button["text"]
        if current_value == "Pick ON":
            sig_pick_button["text"] = "Pick OFF"
            sig_pick_entry.delete(0, tk.END)
            sig_pick_entry.insert(0, str(1.0))
            
            result = client.write_registers(address=9013, values=[1])
            get_min_depth()  # 최소 깊이 값을 가져오고 min_depth_value 변수에 저장
            print("1",float(min_depth_value))
            values = [1172 -float(min_depth_value)]
# # 실수 값을 바이트로 변환하여 전송
            byte_values = []
            print(type(values))
            for value in values:
                byte_value = struct.pack('!f', value)
                byte_values.extend(struct.unpack('!HH', byte_value))
            result = client.write_registers(address=9005, values=byte_values)
        else:
            sig_pick_button["text"] = "Pick ON"
            sig_pick_entry.delete(0, tk.END)
            sig_pick_entry.insert(0, str(0.0))
            result = client.write_registers(address=9013, values=[0])

    except Exception as e:
        print("An error occurred in toggle_sig_pick:", e)


sig_pick_button = tk.Button(window, text="Pick ON", command=toggle_sig_pick)
sig_pick_button.pack()
sig_pick_entry = tk.Entry(window)
sig_pick_entry.pack()    # 전송된 수치 확인용
# sig_place 입력

def toggle_sig_place():
    global client
    current_value = sig_place_button["text"]
    if current_value == "Place ON":
        sig_place_button["text"] = "Place OFF"
        sig_place_entry.delete(0, tk.END)
        sig_place_entry.insert(0, str(1.0))
        result = client.write_registers(address=9015, values=[1])
    else:
        sig_place_button["text"] = "Place ON"
        sig_place_entry.delete(0, tk.END)
        sig_place_entry.insert(0, str(0.0))
        result = client.write_registers(address=9015, values=[0])
sig_place_button = tk.Button(window, text="Place ON", command=toggle_sig_place)
sig_place_button.pack()
sig_place_entry = tk.Entry(window)
sig_place_entry.pack()   

# # sig_auto 입력

# def toggle_sig_auto():
#     current_value = sig_auto_button["text"]
#     if current_value == "ON":
#         sig_auto_button["text"] = "OFF"
#         sig_auto_entry.delete(0, tk.END)
#         sig_auto_entry.insert(0, str(0.0))
#         result = client.read_holding_registers(address=9000, count=23)
#         print(result.registers[15])
#     else:
#         sig_auto_button["text"] = "ON"
#         sig_auto_entry.delete(0, tk.END)
#         sig_auto_entry.insert(0, str(1.0))
#         result = client.read_holding_registers(address=9000, count=23)
#         print(result.registers[15])

# sig_auto_button = tk.Button(window, text="AUTO ON", command=toggle_sig_auto)
# sig_auto_button.pack()
# sig_auto_entry = tk.Entry(window)



def reset_values():
    x_off_entry.delete(0, tk.END)
    y_off_entry.delete(0, tk.END)
    z_off_entry.delete(0, tk.END)
    yaw_off_entry.delete(0, tk.END)
    pitch_off_entry.delete(0, tk.END)
    roll_off_entry.delete(0, tk.END)
    sig_pick_entry.delete(0, tk.END)
    sig_place_entry.delete(0, tk.END)

# Reset 버튼
reset_button = tk.Button(window, text="Reset", command=reset_values)
reset_button.pack()


# Global variable to store min_depth value
min_depth_value = None
# RealSense 데이터 가져오는 함수
def get_min_depth():
    global min_depth_value
    # RealSense에서 프레임 가져오기
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()

    # 프레임이 없으면 건너뜀
    if not depth_frame:
        return

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
    if hasattr(get_min_depth, 'min_depth_text'):
        get_min_depth.min_depth_text.remove()

    # 좌표 및 높이 텍스트 포맷팅
    text = f"({min_depth_x}, {min_depth_y}), Depth: {min_depth}"

    # 좌표 텍스트 추가
    get_min_depth.min_depth_text = ax.annotate(text, xy=(min_depth_x, min_depth_y),
                                               xytext=(min_depth_x + 10, min_depth_y + 10),
                                               color='black', weight='bold', fontsize=8,
                                               arrowprops=dict(arrowstyle='->', color='black'))
    
    result = client.read_holding_registers(address=9017, count=21)
    if result.registers[17] == 1:
        print(result.registers[17])
        result = client.write_registers(address=9005, values=[1172 - min_depth])
        print(1172 - min_depth)
        
    result = client.read_holding_registers(address=9000, count=23)
    # sig_home 값을 확인해보기
    # if result.registers[17] == 1:
    # 최소 깊이 값을 z_off_entry에 자동으로 입력
    
    z_off_entry.delete(0, tk.END)
    z_off_entry.insert(0, str(1172 - min_depth)) #1172
    # result = client.write_holding_registers(5)
    # Return the min_depth value
    # Update the global variable min_depth_value
    # print("min_depth",min_depth)
    min_depth_value = min_depth

    # Return the min_depth value
    #return min_depth_value
    


# 최소 깊이 값을 가져오는 버튼
get_depth_button = tk.Button(window, text="Get Depth", command=get_min_depth)
get_depth_button.pack()

# UI 실행
window.mainloop()

# RealSense 종료
pipeline.stop()
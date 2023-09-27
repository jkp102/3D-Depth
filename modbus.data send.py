from pymodbus.client import ModbusTcpClient

# Modbus TCP 서버에 연결
client = ModbusTcpClient(host="163.254.250.211", port=502)  # 서버 IP 주소와 포트 번호를 적절히 수정하세요

# 연결
client.connect()

# Holding Register (주소 0부터 시작)에서 데이터 읽기
result = client.read_holding_registers(address=0, count=1)

if not result.isError():
    print("Holding Register 값:", result.registers)
else:
    print("데이터 읽기 오류:", result)

# Holding Register (주소 0부터 시작)에 데이터 쓰기
result = client.write_registers(address=1, values=[99])

if not result.isError():
    print("Holding Register에 데이터 쓰기 성공")
else:
    print("데이터 쓰기 오류:", result)

# Holding Register (주소 1부터 시작)에 다중 데이터 쓰기
result = client.write_registers(address=9000, values=[0,0,0,450,0,0,0,0,0,0,0,0])

if not result.isError():
    print("다중 데이터 쓰기 성공")
else:
    print("데이터 쓰기 오류:", result)

# Holding Register (주소 0부터 시작)에서 다중 데이터 읽기
result = client.read_holding_registers(address=9000, count=23)

if not result.isError():
    print("다중 데이터 읽기 값:", result.registers)
else:
    print("데이터 읽기 오류:", result)

# 연결 종료
client.close()
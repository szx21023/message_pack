import struct

# MessagePack 類型標識符
UINT8 = 0xCC
UINT16 = 0xCD
UINT32 = 0xCE
UINT64 = 0xCF
STRING8 = 0xD9
STRING16 = 0xDA
STRING32 = 0xDB
ARRAY16 = 0xDC
ARRAY32 = 0xDD
MAP16 = 0xDE
MAP32 = 0xDF

# 序列化整數（無符號）
def encode_int(value):
    if 0 <= value <= 0x7F:  # 小整數，0x00 到 0x7F
        return bytes([value])
    elif 0 <= value <= 0xFF:  # 1字節無符號整數
        return bytes([UINT8]) + struct.pack('B', value)
    elif 0 <= value <= 0xFFFF:  # 2字節無符號整數
        return bytes([UINT16]) + struct.pack('>H', value)
    elif 0 <= value <= 0xFFFFFFFF:  # 4字節無符號整數
        return bytes([UINT32]) + struct.pack('>I', value)
    elif 0 <= value <= 0xFFFFFFFFFFFFFFFF:  # 8字節無符號整數
        return bytes([UINT64]) + struct.pack('>Q', value)
    return b''

# 序列化字符串（這裡將做一些調整來與 msgpack 一致）
def encode_string(s):
    length = len(s)
    if length <= 31:  # 小於等於 31 個字元（msgpack 將此表示為 0xA0）
        return bytes([0xA0 + length]) + s.encode('utf-8')
    elif length <= 255:  # 小於等於 255 個字元
        return bytes([STRING8]) + struct.pack('B', length) + s.encode('utf-8')
    elif length <= 65535:  # 小於等於 65535 個字元
        return bytes([STRING16]) + struct.pack('>H', length) + s.encode('utf-8')
    elif length <= 4294967295:  # 小於等於 4294967295 個字元
        return bytes([STRING32]) + struct.pack('>I', length) + s.encode('utf-8')
    return b''

# 序列化列表（數組）
def encode_array(arr):
    length = len(arr)
    if length <= 65535:  # 小於等於 65535 個元素
        return bytes([ARRAY16]) + struct.pack('>H', length) + b''.join(encode_object(item) for item in arr)
    elif length <= 4294967295:  # 小於等於 4294967295 個元素
        return bytes([ARRAY32]) + struct.pack('>I', length) + b''.join(encode_object(item) for item in arr)
    return b''

# 序列化字典（Map）
def encode_map(d):
    length = len(d)
    if length <= 15:  # 小於等於 15 個鍵值對，msgpack 用 0x80 - 0x8F
        return bytes([0x80 + length]) + b''.join(
            encode_object(k) + encode_object(v) for k, v in d.items()
        )
    elif length <= 65535:  # 小於等於 65535 個鍵值對
        return bytes([MAP16]) + struct.pack('>H', length) + b''.join(
            encode_object(k) + encode_object(v) for k, v in d.items()
        )
    elif length <= 4294967295:  # 小於等於 4294967295 個鍵值對
        return bytes([MAP32]) + struct.pack('>I', length) + b''.join(
            encode_object(k) + encode_object(v) for k, v in d.items()
        )
    return b''

# 通用的物件序列化處理
def encode_object(obj):
    if isinstance(obj, int):
        return encode_int(obj)
    elif isinstance(obj, str):
        return encode_string(obj)
    elif isinstance(obj, list):
        return encode_array(obj)
    elif isinstance(obj, dict):
        return encode_map(obj)
    return b''

# 測試數據
data = {
    'name': 'Alice',
    'age': 30,
    'friends': ['Bob', 'Charlie'],
    'active': True
}

# 序列化數據
encoded_data = encode_object(data)
print(f'Encoded Data: {encoded_data.hex()}')

# 使用 msgpack 進行序列化
import msgpack
packed_data = msgpack.packb(data)

# 打印序列化后的数据
print(f"Packed Data: {packed_data.hex()}")
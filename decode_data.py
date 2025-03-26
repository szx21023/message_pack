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
TRUE = 0xC3  # `True` 在 msgpack 中的表示
FALSE = 0xC2  # `False` 在 msgpack 中的表示

# 解碼整數（無符號）
def decode_int(data):
    first_byte = data[0]
    if first_byte <= 0x7F:  # 小整數，0x00 到 0x7F
        return first_byte, data[1:]
    elif first_byte == UINT8:  # 1字節無符號整數
        return struct.unpack('B', data[1:2])[0], data[2:]
    elif first_byte == UINT16:  # 2字節無符號整數
        return struct.unpack('>H', data[1:3])[0], data[3:]
    elif first_byte == UINT32:  # 4字節無符號整數
        return struct.unpack('>I', data[1:5])[0], data[5:]
    elif first_byte == UINT64:  # 8字節無符號整數
        return struct.unpack('>Q', data[1:9])[0], data[9:]
    return None, data

# 解碼字符串
def decode_string(data):
    first_byte = data[0]
    if first_byte >= 0xA0 and first_byte <= 0xBF:  # 小於等於 31 個字元
        length = first_byte - 0xA0
        return data[1:1 + length].decode('utf-8'), data[1 + length:]
    elif first_byte == STRING8:  # 1字節長度字符串
        length = struct.unpack('B', data[1:2])[0]
        return data[2:2 + length].decode('utf-8'), data[2 + length:]
    elif first_byte == STRING16:  # 2字節長度字符串
        length = struct.unpack('>H', data[1:3])[0]
        return data[3:3 + length].decode('utf-8'), data[3 + length:]
    elif first_byte == STRING32:  # 4字節長度字符串
        length = struct.unpack('>I', data[1:5])[0]
        return data[5:5 + length].decode('utf-8'), data[5 + length:]
    return None, data

# 解碼布林值
def decode_bool(data):
    if data[0] == TRUE:
        return True, data[1:]
    elif data[0] == FALSE:
        return False, data[1:]
    return None, data

# 解碼列表（數組）
def decode_array(data):
    first_byte = data[0]
    if first_byte == ARRAY16:  # 2字節長度數組
        length = struct.unpack('>H', data[1:3])[0]
        arr = []
        new_data = data[3:]
        for _ in range(length):
            item, new_data = decode_object(new_data)
            arr.append(item)
        return arr, new_data
    elif first_byte == ARRAY32:  # 4字節長度數組
        length = struct.unpack('>I', data[1:5])[0]
        arr = []
        new_data = data[5:]
        for _ in range(length):
            item, new_data = decode_object(new_data)
            arr.append(item)
        return arr, new_data
    return None, data

# 解碼字典（Map）
def decode_map(data):
    first_byte = data[0]
    if first_byte == MAP16:  # 2字節長度字典
        length = struct.unpack('>H', data[1:3])[0]
        d = {}
        new_data = data[3:]
        for _ in range(length):
            key, new_data = decode_object(new_data)
            value, new_data = decode_object(new_data)
            d[key] = value
        return d, new_data
    elif first_byte == MAP32:  # 4字節長度字典
        length = struct.unpack('>I', data[1:5])[0]
        d = {}
        new_data = data[5:]
        for _ in range(length):
            key, new_data = decode_object(new_data)
            value, new_data = decode_object(new_data)
            d[key] = value
        return d, new_data
    return None, data

# 通用的物件解碼處理
def decode_object(data):
    first_byte = data[0]
    if first_byte <= 0x7F or (first_byte >= 0xA0 and first_byte <= 0xBF):  # 整數或小長度字符串
        return decode_int(data)
    elif first_byte == TRUE or first_byte == FALSE:  # 布林值
        return decode_bool(data)
    elif first_byte == ARRAY16 or first_byte == ARRAY32:  # 數組
        return decode_array(data)
    elif first_byte == MAP16 or first_byte == MAP32:  # 字典
        return decode_map(data)
    else:  # 字符串
        return decode_string(data)

# 測試的序列化數據
encoded_data = bytes.fromhex("84a46e616d65a5416c696365a36167651ea7667269656e6473dc0002a3426f62a7436861726c6965a46e616d65a5416c696365")

# 反序列化數據
decoded_data, remaining_data = decode_object(encoded_data)

print("Decoded Data:", decoded_data)
print("Remaining Data:", remaining_data)  # 應該是空的，表示解碼結束

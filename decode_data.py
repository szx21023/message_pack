import struct

def msgpack_encode(data):
    """ 手刻 MessagePack 編碼 """
    if data is None:
        return b'\xC0'
    elif isinstance(data, bool):
        return b'\xC3' if data else b'\xC2'
    elif isinstance(data, int):
        if -32 <= data <= 127:
            return struct.pack("b", data)  # fixint
        elif 0 <= data <= 255:
            return b'\xCC' + struct.pack("B", data)  # uint8
        elif -128 <= data <= 127:
            return b'\xD0' + struct.pack("b", data)  # int8
        elif 0 <= data <= 65535:
            return b'\xCD' + struct.pack(">H", data)  # uint16
        elif -32768 <= data <= 32767:
            return b'\xD1' + struct.pack(">h", data)  # int16
        elif 0 <= data <= 4294967295:
            return b'\xCE' + struct.pack(">I", data)  # uint32
        elif -2147483648 <= data <= 2147483647:
            return b'\xD2' + struct.pack(">i", data)  # int32
        elif 0 <= data <= 18446744073709551615:
            return b'\xCF' + struct.pack(">Q", data)  # uint64
        else:
            return b'\xD3' + struct.pack(">q", data)  # int64
    elif isinstance(data, float):
        return b'\xCB' + struct.pack(">d", data)  # float64
    elif isinstance(data, str):
        encoded_str = data.encode('utf-8')
        length = len(encoded_str)
        if length <= 31:
            return struct.pack("B", 0xA0 + length) + encoded_str
        elif length <= 255:
            return b'\xD9' + struct.pack("B", length) + encoded_str
        elif length <= 65535:
            return b'\xDA' + struct.pack(">H", length) + encoded_str
        else:
            return b'\xDB' + struct.pack(">I", length) + encoded_str
    elif isinstance(data, list):
        length = len(data)
        if length <= 15:
            header = struct.pack("B", 0x90 + length)
        elif length <= 65535:
            header = b'\xDC' + struct.pack(">H", length)
        else:
            header = b'\xDD' + struct.pack(">I", length)
        return header + b''.join(msgpack_encode(item) for item in data)
    elif isinstance(data, dict):
        length = len(data)
        if length <= 15:
            header = struct.pack("B", 0x80 + length)
        elif length <= 65535:
            header = b'\xDE' + struct.pack(">H", length)
        else:
            header = b'\xDF' + struct.pack(">I", length)
        return header + b''.join(msgpack_encode(k) + msgpack_encode(v) for k, v in data.items())
    else:
        raise TypeError(f"Unsupported type: {type(data)}")

def msgpack_decode(data, offset=0):
    """ 手刻 MessagePack 解碼 """
    prefix = data[offset]

    # nil
    if prefix == 0xC0:
        return None, offset + 1
    # boolean
    elif prefix == 0xC2:
        return False, offset + 1
    elif prefix == 0xC3:
        return True, offset + 1
    # fixint (正數)
    elif prefix <= 0x7F:
        return prefix, offset + 1
    # fixint (負數)
    elif prefix >= 0xE0:
        return prefix - 0x100, offset + 1
    # int
    elif prefix == 0xCC:
        return data[offset + 1], offset + 2
    elif prefix == 0xCD:
        return struct.unpack(">H", data[offset + 1:offset + 3])[0], offset + 3
    elif prefix == 0xCE:
        return struct.unpack(">I", data[offset + 1:offset + 5])[0], offset + 5
    elif prefix == 0xCF:
        return struct.unpack(">Q", data[offset + 1:offset + 9])[0], offset + 9
    # string
    elif prefix >= 0xA0 and prefix <= 0xBF:
        length = prefix - 0xA0
        return data[offset + 1:offset + 1 + length].decode("utf-8"), offset + 1 + length
    elif prefix == 0xD9:
        length = data[offset + 1]
        return data[offset + 2:offset + 2 + length].decode("utf-8"), offset + 2 + length
    # array
    elif prefix >= 0x90 and prefix <= 0x9F:
        length = prefix - 0x90
        array = []
        offset += 1
        for _ in range(length):
            item, offset = msgpack_decode(data, offset)
            array.append(item)
        return array, offset
    # map (dictionary)
    elif prefix >= 0x80 and prefix <= 0x8F:
        length = prefix - 0x80
        result = {}
        offset += 1
        for _ in range(length):
            key, offset = msgpack_decode(data, offset)
            value, offset = msgpack_decode(data, offset)
            result[key] = value
        return result, offset
    else:
        raise ValueError(f"Unsupported prefix: {hex(prefix)}")

# # 測試編碼
# test_data = {"name": "Alice", "age": 30, "is_student": False, "scores": [90, 80, 70]}
# packed_data = msgpack_encode(test_data)
# print("MessagePack 編碼結果:", packed_data.hex())

# # 測試解碼
# decoded_data, _ = msgpack_decode(packed_data)
# print("解碼後數據:", decoded_data)
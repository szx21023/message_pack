import msgpack

# 定义一个 Python 对象
data = {"name": "Alice", "age": 30, "languages": ["Python", "C++", "Java"]}

# 将 Python 对象序列化为 MessagePack 格式
packed_data = msgpack.packb(data)

print(type(packed_data))

# 打印序列化后的数据
print("Packed Data:", packed_data)

# 将序列化后的数据反序列化为原始的 Python 对象
unpacked_data = msgpack.unpackb(packed_data)

# 打印反序列化后的数据
print("Unpacked Data:", unpacked_data)

text = '\x83\xa4name\xa5Alice\xa3age\x1e\xa9languages\x93\xa6Python\xa3C++\xa4Java'.encode('latin1')
print(text, type(text))
print(packed_data, type(packed_data))
print(text == packed_data)
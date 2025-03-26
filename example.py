import msgpack

# 定义一个 Python 对象
data = {}
data = {'a': 1}
data = {'a': '1'}
data = {'a': '1', 'b': 2}
data = {'a': []}
data = {'a': ['a', 'b', 'c']}
data = {'a': ['a', 2, 3]}
data = {'a': (2, 3)}
data = {'a': {}}
data = {'a': {'a': 324, 'b': 'fwerw'}}
data = {'a': 9}

# 将 Python 对象序列化为 MessagePack 格式
packed_data = msgpack.packb(data)

print(type(packed_data))

# 打印序列化后的数据
print("Packed Data:", packed_data)

# 将序列化后的数据反序列化为原始的 Python 对象
unpacked_data = msgpack.unpackb(packed_data)

# 打印反序列化后的数据
print("Unpacked Data:", unpacked_data)



class MessagePack:
    def pack(self, data):
        self.data = data
        self.packed_data = msgpack.packb(data)
        return self.packed_data

    def unpack(self, packed_data):
        self.packed_data = packed_data
        self.unpacked_data = msgpack.unpackb(packed_data)
        return self.unpacked_data
    
    def serialize(self, data):
        text = ''
        if type(data) == dict:
            text = r'\x8' + str(len(data))
            for k, v in data.items():
                text += self.serialize(k) + self.serialize(v)

        if type(data) == list or type(data) == tuple:
            text = r'\x9' + str(len(data))
            for v in data:
                text += self.serialize(v)

        elif type(data) == str:
            text = r'\xa' + str(len(data)) + data

        elif type(data) == int:
            text = r'\x0' + str(data)
        
        return text

message_pack = MessagePack()
print(message_pack.pack(data))
print(message_pack.serialize(data).encode('latin1'))
print((9).to_bytes(1, 'big'))
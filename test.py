from decode_data import msgpack_decode, msgpack_encode
import msgpack

test_data = {"name": "Alice", "age": 30, "is_student": False, "scores": [90, 80, 70]}
packed_data = msgpack_encode(test_data)
msgpack_data = msgpack.packb(test_data)
print(packed_data == msgpack_data)

print(msgpack_decode(msgpack.packb(test_data))[0])
print(msgpack.unpackb(msgpack.packb(test_data)))
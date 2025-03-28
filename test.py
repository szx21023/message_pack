from encoder_and_decoder import msgpack_encode, msgpack_decode
import msgpack

def test_msgpack_encode():
    # 測試數據
    test_data = {"name": "Alice", "age": 30, "is_student": False, "scores": [90, 80, 70]}
    
    # 使用自定義的 msgpack_encode 函數進行編碼
    packed_data = msgpack_encode(test_data)
    
    # 使用 msgpack 庫進行編碼
    expected_data = msgpack.packb(test_data)
    
    # 比較兩者的結果
    assert packed_data == expected_data, f"Expected {expected_data}, but got {packed_data}"

def test_msgpack_decode():
    # 測試數據
    test_data = {"name": "Alice", "age": 30, "is_student": False, "scores": [90, 80, 70]}
    
    # 使用自定義的 msgpack_encode 函數進行編碼
    packed_data = msgpack_encode(test_data)
    
    # 使用自定義的 msgpack_decode 函數進行解碼
    decoded_data, _ = msgpack_decode(packed_data)
    
    # 比較解碼結果與原始數據
    assert decoded_data == test_data, f"Expected {test_data}, but got {decoded_data}"
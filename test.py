from encoder_and_decoder import msgpack_encode, msgpack_decode
import msgpack

import pytest

@pytest.mark.parametrize(
    "test_data",  # 測試欄位
    [
        ({}), # 第一組測試資料
        ({'a': 1}), # 第二組測試資料
        ({'a': -1}), # 第三組測試資料
        ({'a': '1'}), # 第四組測試資料
        ({'a': []}), # 第五組測試資料
        ({'a': 1, 'b': '4', 'C': True}), # 第六組測試資料
        ({'name': 'test', 'age': 40, 'address': 'ameriva', 'height': 180.4, 'weight': 74.855432542354235, 'is_student': False, 'scope': [80, 70, 60]}), # 第七組測試資料
        ({'nirieniwbgiwerbgiib': 'rweiogurioewgigoihuiih', 'aaa': None, 'tt': {'t': 1, 'b': 2}}) # 第八組測試資料
    ]
)
def test_msgpack_encode(test_data):
    # 使用自定義的 msgpack_encode 函數進行編碼
    packed_data = msgpack_encode(test_data)
    
    # 使用 msgpack 庫進行編碼
    expected_data = msgpack.packb(test_data)
    
    # 自定義 encode 和第三方 encode 的結果是否相同
    assert packed_data == expected_data, f"Expected {expected_data}, but got {packed_data}"

@pytest.mark.parametrize(
    "test_data",  # 測試欄位
    [
        ({}), # 第一組測試資料
        ({'a': 1}), # 第二組測試資料
        ({'a': -1}), # 第三組測試資料
        ({'a': '1'}), # 第四組測試資料
        ({'a': []}), # 第五組測試資料
        ({'a': 1, 'b': '4', 'C': True}), # 第六組測試資料
        ({'name': 'test', 'age': 40, 'address': 'ameriva', 'height': 180.4, 'weight': 74.855432542354235, 'is_student': False, 'scope': [80, 70, 60]}), # 第七組測試資料
        ({'nirieniwbgiwerbgiib': 'rweiogurioewgigoihuiih', 'aaa': None, 'tt': {'t': 1, 'b': 2}}) # 第八組測試資料
    ]
)
def test_msgpack_decode(test_data):
    # 使用自定義的 msgpack_encode 函數進行編碼
    packed_data = msgpack_encode(test_data)
    
    # 使用自定義的 msgpack_decode 函數進行解碼
    decoded_data, _ = msgpack_decode(packed_data)
    
    # 自定義 encode 再自定義 decode 後，與原始數據是否相同
    assert decoded_data == test_data, f"Expected {test_data}, but got {decoded_data}"
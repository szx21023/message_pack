安裝環境(Python 3.12.3)
```
pip install -r requirements.txt
```

encoder_and_decoder.py: 定義的手刻的 message pack 的 encoder 和 decoder

使用範例
```python
# 測試編碼
test_data = {"name": "Alice", "age": 30, "is_student": False, "scores": [90, 80, 70]}
packed_data = msgpack_encode(test_data)
print("MessagePack 編碼結果:", packed_data.hex())

# 測試解碼
decoded_data, _ = msgpack_decode(packed_data)
print("MessagePack 解碼結果:", decoded_data)
```

test.py: 擺放的是測試資料

測試內容:
- 自定義 encode 和第三方 encode 的結果是否相同
- 自定義 encode 再自定義 decode 後，與原始數據是否相同

執行測試
```
pytest test.py
```

預期測試執行結果(16 passed 表示 test.py 的測試全部通過):
```python
============================================================================================== test session starts ==============================================================================================
platform linux -- Python 3.12.3, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/herry/project/message_pack
collected 16 items

test.py ................                                                                                                                                                                                  [100%]

============================================================================================== 16 passed in 0.01s ===============================================================================================
```
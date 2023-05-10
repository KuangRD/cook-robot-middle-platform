import uuid

uuid_str = '550e8400-e29b-41d4-a716-446655440000'
uuid_obj = uuid.UUID(uuid_str)
uuid_bytes = uuid_obj.bytes

print("UUID字符串：", uuid_str)
print("转换后的byte数组：", uuid_bytes)
print(str(uuid_obj))

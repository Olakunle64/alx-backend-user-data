import base64

name = "kunle"
password = "password"
name_password = None
# name_password_bytes = name_password.encode("utf-8")
# base64_bytes = base64.b64encode(name_password.enocde("utf-8"))
decoded_base64 = base64.b64decode(89)
# base64_name_password = base64_bytes.decode("utf-8")
# print(base64_name_password)
print(decoded_base64.decode("utf-8"))
print(decoded_base64)
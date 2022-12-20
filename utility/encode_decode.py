import base64

def encodeString(str):
    result = base64.b64encode(str.encode('ascii')).decode('ascii')
    return result

def decodeString(str):
    result = base64.b64decode(str.encode('ascii')).decode('ascii')
    return result

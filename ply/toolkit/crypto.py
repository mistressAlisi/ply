from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
import base64

def get_or_set_key(request,in_bytes=False):

        if 'cck' in request.session.keys():
            scck = request.session.get('cck')
            if in_bytes is False:
                return bytes.fromhex(scck)
            else:
                return scck
        else:
            rkey = get_random_bytes(16).hex()
            request.session['cck']=rkey
            request.session.save()
            if not in_bytes:
                return rkey
            else:
                return bytes.fromhex(rkey)
    
def decrypt_from_skey(request,idata,ivd):
    try:
        key = get_or_set_key(request,True)
        
        print(ivd.encode())
        #iv = base64.b64decode(ivd.encode())
        iv = ivd.encode()
        #print(iv)
        cipher = AES.new(key, AES.MODE_CBC, ivd)
        print(cipher)
        #ct = base64.b64decode(data.encode())
        #cipher = AES.new(key, AES.MODE_CBC, iv)
        #pt = unpad(cipher.decrypt(ct, AES.block_size))
        #print("The message was: ", pt)
        #return pt
        return True
    except (ValueError, KeyError) as e:
        print(e)
        print("Incorrect decryption")

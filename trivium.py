import binascii
import os.path
import os
import time
from itertools import repeat

def hex_xor(hex_str1, hex_str2): 
    l = min(len(hex_str1), len(hex_str2))
    a = int(hex_str1[:l], 16)
    b = int(hex_str2[:l], 16)
    c = hex(a ^ b)[2:].zfill(l)
    return c

def generation_key(key, iv, N):
    key = bin(int(key, 16))[2:]
    iv = bin(int(iv, 16))[2:]
    iv = iv.zfill(80)
    key = key.zfill(80)
    iv = [int(_) for _ in iv]
    key = [int(_) for _ in key]
    
    key_stream = []
    # Init
    rA = iv + list(repeat(0, 13))
    rB = key + list(repeat(0, 4))
    rC = list(repeat(0, 108)) + list(repeat(1, 3))
    # Warm_up
    for _ in range(1152):
        t1 = rA[65] ^ rA[92] ^ (rA[90] & rA[91])
        t2 = rB[68] ^ rB[83] ^ (rB[81] & rB[82])
        t3 = rC[65] ^ rC[110] ^ (rC[108] & rC[109])
        rA.insert(0, rA[68] ^ t3)
        rA.pop()
        rB.insert(0, rB[77] ^ t1)
        rB.pop()
        rC.insert(0, rC[86] ^ t2)
        rC.pop()
    # Gen_key
    for _ in range(N*4):
        t1 = rA[65] ^ rA[92] ^ (rA[90] & rA[91])
        t2 = rB[68] ^ rB[83] ^ (rB[81] & rB[82])
        t3 = rC[65] ^ rC[110] ^ (rC[108] & rC[109])
        key_stream.append(t1 ^ t2 ^ t3)
        rA.insert(0, rA[68] ^ t3)
        rA.pop()
        rB.insert(0, rB[77] ^ t1)
        rB.pop()
        rC.insert(0, rC[86] ^ t2)
        rC.pop()
    key_stream = hex(int("0b" + ''.join([str(i) for i in key_stream]), 2))[2:].zfill(N)
    return key_stream

def encryption(file, key):
    with open("/dev/random", 'rb') as f:
        iv = binascii.hexlify(f.read(10)).decode()
    with open(file, 'rb') as rf:
        texts = binascii.hexlify(rf.read()).decode()
    key_stream = generation_key(key, iv, len(texts))
    if not os.path.exists("./encrypted"):
        os.mkdir("./encrypted")
    with open("./encrypted/{}".format(os.path.basename(file)), 'wb') as wf:
        wf.write(iv.encode())
        wf.write(hex_xor(texts, key_stream).encode())

def decryption(encrypted_file, key):
    with open(encrypted_file, 'rb') as rf:
        encrypted_texts = rf.read().decode()
    iv = encrypted_texts[:20]
    encrypted_texts = encrypted_texts[20:]
    key_stream = generation_key(key, iv, len(encrypted_texts))
    if not os.path.exists("./decrypted"):
        os.mkdir("./decrypted")
    with open("./decrypted/{}".format(os.path.basename(encrypted_file)), 'wb') as wf:
        wf.write(binascii.unhexlify(hex_xor(encrypted_texts, key_stream).encode()))

def main():
    with open("key.txt", 'r') as f:
        key = f.read()
    files = os.listdir("./files_to_encrypt")
    for file in files:
        if file[0] == '.':
            del file
    log = open("log.txt", "w")
    for file in files:
        print("encrypting {} ...".format(file))
        st = time.time()
        encryption("./files_to_encrypt/" + file, key)
        en = time.time()
        print("encrypted {} done in {} sec".format(file, en - st))
        log.write("encrypted {} done in {} sec\n".format(file, en - st))
    
    for file in files:
        print("decrypting {} ...".format(file))
        st = time.time()
        decryption("./encrypted/" + file, key)
        en = time.time()
        print("decrypted {} done in {}sec".format(file, en - st))

    for file in files:
        t = (open("./files_to_encrypt/" + file, 'rb'), open("./decrypted/" + file, 'rb'))
        if t[0].read() == t[1].read():
            print("check {} success".format(file))
            log.write("check {} success\n".format(file))
        else: 
            print("check {} fail😭".format(file))
            log.write("check {} fail😭\n".format(file))
        t[0].close()
        t[1].close()
    
    log.close()

if __name__ == "__main__":
    main()
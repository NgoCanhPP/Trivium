import binascii
import os.path
import os
import time

def hex_xor(hex_str1, hex_str2): 
    l = min(len(hex_str1), len(hex_str2))
    a = int(hex_str1[:l], 16)
    b = int(hex_str2[:l], 16)
    c = hex(a ^ b)[2:]
    return '0' * (l - len(c)) + c

def generation_key(key, iv, N):
    key = bin(int(key, 16))[2:]
    iv = bin(int(iv, 16))[2:]
    if len(iv) != 80:
        iv = (80-len(iv)) * '0' + iv
    if len(key) != 80:
        key = (80-len(key)) * '0' + key
    key_stream = ""
    # Init
    rA = iv + 13 * '0'
    rB = key + 4 * '0'
    rC = 108 * '0' + 3 * '1'
    # Warm_up
    for i in range(1152):
        t1 = (int(rA[65]) + int(rA[92]) + int(rA[90]) * int(rA[91])) % 2
        t2 = (int(rB[68]) + int(rB[83]) + int(rB[81]) * int(rB[82])) % 2
        t3 = (int(rC[65]) + int(rC[110]) + int(rC[108]) * int(rC[109])) % 2
        rA = str((int(rA[68]) + t3) % 2) + rA[:-1]
        rB = str((int(rB[77]) + t1) % 2) + rB[:-1]
        rC = str((int(rC[86]) + t2) % 2) + rC[:-1]
    # Gen_key
    for i in range(N*4):
        t1 = (int(rA[65]) + int(rA[92]) + int(rA[90]) * int(rA[91])) % 2
        t2 = (int(rB[68]) + int(rB[83]) + int(rB[81]) * int(rB[82])) % 2
        t3 = (int(rC[65]) + int(rC[110]) + int(rC[108]) * int(rC[109])) % 2
        key_stream = key_stream + str((t1 + t2 + t3) % 2)
        rA = str((int(rA[68]) + t3) % 2) + rA[:-1]
        rB = str((int(rB[77]) + t1) % 2) + rB[:-1]
        rC = str((int(rC[86]) + t2) % 2) + rC[:-1]
    key_stream = hex(int("0b" + key_stream, 2))[2:]
    key_stream = (N-len(key_stream)) * '0' + key_stream
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
# Trivium 

Name: Ngô Trí Cảnh
StudentID: 20220015

## Mô tả cách cài đặt
File trivium.py bao gồm các hàm chính:
1. hex_xor(hex_str1, hex_str2):  
    Hàm nhận vào 2 string là biểu diễn ở dạng hex của một thông tin nào đó.
    Trả về một string là kết quả của phép xor 2 string nhận vào với nhau.
2. generation_key(key, iv, N):
    Hàm nhận vào cặp string (key, iv) là biểu diễn ở dạng hex của (private key, IV); N là độ dài chuỗi khoá dưới dạng hex cần sinh
3. encrypt(file, key):
    Hàm nhận vào đường dẫn tuyệt đối đến file cần mã hoá và private key, random ra IV, sau đó dùng hàm generation_key để tạo ra chuỗi key có độ dài bằng với file cần mã hoá, tiếp đó sử dụng phép xor để mã hoá file
    Lưu trữ file đã mã hoá vào thư mục con tên encrypted
4. decrypt(encrypt_file, key):
    Tương tự hàm encrypt() khi nhận vào tên file cần giải mã và tìm file này trong thư mục encrypt, giải mã file và in ra thư mục decrypted
5. main():
    Hàm main thực hiện 2 nhiệm vụ:
    + Mã hoá:
        - Mã hoá tất cả các file trong thư mục files_to_encrypt
        - Xác định thời gian mã hoá từng file và ghi ra file log.txt
    + Kiểm tra:
        - Giải mã các file vừa mã hoá 
        - Kiểm tra sự nguyên vẹn của dữ liệu sau một vòng mã hoá-giải mã để kiểm tra lỗi của mã nguồn
        - Ghi ra file log.txt thông tin kiểm tra 
        
        
Các file trivium.py, key.txt, log.txt, files_to_endcrypt, encrypted, decrypted được đính kèm trong cùng file nén. 

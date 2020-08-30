import socket
import sys
from itertools import product
from string import digits, ascii_letters


def run(host, port, passwords):
    with socket.socket() as st:
        st.connect((host, port))
        for password in passwords:
            st.send(password.encode())
            if st.recv(1024).decode() == "Connection success!":
                return password


def password_gen(pass_max_len, chars):
    for i in range(1, pass_max_len + 1):
        for p in product(chars, repeat=i):
            yield "".join(p)


def read_lines_from_file(path):
    with open(path) as file:
        return file.read().split("\n")


def dict_based_gen(dictionary):
    for line in dictionary:
        for password in product(*[c + c.upper() for c in line]):  # example:  "hack" -> "hH", "aA", "cC", "kK"
            yield "".join(password)


# try typical passwords first
result = run(sys.argv[1], int(sys.argv[2]), dict_based_gen(read_lines_from_file("dictionaries/typical_passwords.txt")))
if result:
    print(result)
else:
    print(run(sys.argv[1], int(sys.argv[2]), password_gen(12, digits + ascii_letters)))

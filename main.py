from flask import Flask, request, jsonify
import json
import os
import sqlite3
db_name = 'around.db'


def write(tb, values):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    val = "','".join(values)
    cur.execute(f"""INSERT INTO {tb} VALUES('{val}')""")
    con.commit()
    con.close()


def readwhere(tb, col, usl):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cols = ', '.join(col)
    otv = cur.execute(f"""SELECT {cols} FROM {tb} WHERE {usl}""").fetchall()
    con.close()
    return otv


app = Flask(__name__)


@app.route('/', methods=["POST"])
def main():
    response = {}
    event = request.json
    if event['mode'] == 'login':
        lg = event['number'].lstrip('+').replace('-', '')
        ps = event['password']
        users = readwhere("users", ["number", "password"], f"number='{lg}' AND password='{ps}'")
        if len(users) == 0:
            response['login'] = False
        else:
            response['login'] = True
        return response
    elif event['mode'] == 'reg':
        lg = event['number'].lstrip('+').replace('-', '')
        ps = event['password']
        scndps = event['second_password']
        if ps != scndps:
            response['reg'] = False
            response['text'] = "Перепроверьте пароль! Ваши пароли не совпадают."
            return response
        users = readwhere('users', ['number'], f"number={lg}")
        if len(users) != 0:
            response['reg'] = False
            response['text'] = "Ваш номер телефона уже зарегистрирован! Попробуйте войти."
            return response
        write('users', [lg, ps])
        response['reg'] = True
        response['text'] = "Успешная регистрация!"
        return response
        


@app.route('/', methods=['GET'])
def get():
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM users""").fetchall()
    con.close()
    print(result)
    return "ONLY POST"
    


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
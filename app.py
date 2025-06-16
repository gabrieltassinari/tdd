import hashlib
import sqlite3
import base64
import httpx
import os

from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/", defaults={"method": None}, methods=["GET", "POST"])
@app.route("/<method>",                    methods=["GET", "POST"])
def main(method):
    if request.method == "GET" and method is not None:
        url = decode(method)

        if url != "":
            return redirect(url, code=301)
        return "Código Inválido!", 404

    if request.method == "POST" and method == "encode":
        url = request.form.get("url")

        if url is None or url == "":
            return "URL não fornecida", 400

        try:
            httpx.get(url).status_code
        except httpx.ConnectError:
            return "URL Indisponível", 404
        except httpx.UnsupportedProtocol:
            return "URL Inválida", 400

        return render_template(
            "index.html",
            url=encode(url),
            socket=request.url_root
        )

    return render_template("index.html")

def encode(url):
    urlb = url.encode("utf-8")

    m = hashlib.md5()
    m.update(urlb)

    urlmd5 = m.hexdigest().encode("utf-8")
    url64 = base64.b64encode(urlmd5)[:6].decode("utf-8")

    con = sqlite3.connect("banco.sqlite")
    cur = con.cursor()

    sql = f"INSERT INTO url VALUES (null, '{url64}', '{url}');"

    cur.execute(sql)
    con.commit()
    con.close()

    return url64

def decode(url):
    con = sqlite3.connect("banco.sqlite")
    cur = con.cursor()

    sql = f"SELECT url FROM url WHERE url64 = '{url}';"
    res = cur.execute(sql).fetchall()

    return res[0][0] if res != [] else ""

if not os.path.exists("banco.sqlite"):
    con = sqlite3.connect("banco.sqlite")
    cur = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS url(
        id INTEGER PRIMARY KEY,
        url64 STRING,
        url STRING
    );"""

    cur.execute(sql)
    con.close()

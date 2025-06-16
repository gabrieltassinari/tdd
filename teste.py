import pytest

from app import encode, decode, app

@pytest.fixture
def client():
    return app.test_client()

# Garante que o protocolo seja http/https
def test_protocol(client):
    res = client.post("/encode", data={"url": "ftp://www.google.com"})

    assert res.status_code == 400, "Protocoloinválido"

# Verifica se o servidor da URL está disponível (online).
def test_ping(client):
    r1 = client.post("/encode", data={"url": "https://www.google.com"})
    r2 = client.post("/encode", data={"url": "https://www.url-invalida.com"})

    assert r1.status_code == 200 and r2.status_code != 200, "URL Indisponível/Inválida"

# Verifica se o usuário fornece alguma URL.
def test_arg(client):
    r1 = client.post("/encode?url=", data={"url": ""})
    r2 = client.post("/encode?url=", data={"url": '""'})
    r3 = client.post("/encode")

    assert r1 != 400 or r2 != 400 or r3 != 400, "URL não fornecida"

# Como funciona o encode?
# É gerado um código com os 6 primeiros dígitos do md5sum + base64 da URL.
# Logo abaixo está um exemplo que pode ser executado no shell.
#
# Entrada: printf https://www.google.com | md5sum | base64 | cut -c 1-6
# Saida:   OGZmZG
def test_encode():
    url = encode("https://www.google.com")

    assert url == "OGZmZG", "encode falhou."

def test_decode():
    url = decode("OGZmZG")

    assert url == "https://www.google.com", "decode falhou."

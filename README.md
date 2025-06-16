# Dependências / Bibliotecas utilizadas
* flask>=3.1.1
* httpx>=0.28.1
* pytest>=8.4.0
* requests>=2.32.3

# Executação
Para executar a aplicação utilize:

```sh
flask run
```

Para execução dos testes:

> NOTA: Perceba que os testes necessitam de sudo, não sei o motivo ao certo mas
> acredito que deva ser por conta da instanciação do flask em uma porta baixa.

```sh
sudo pytest teste.py
```

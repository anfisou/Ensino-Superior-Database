# English Version

This project was developed for the subject 'Databases' by the students [André Sousa](https://github.com/anfisou) and [Paulo Silva](https://github.com/WrekingPanda) and implements a web app on top of a relational database about portuguese universities.

You need Python 3, a installed pip package manager and a Flask library. You can install them using:

``` sudo apt-get install python3 python3-pip ``` e  ``` pip3 install --user Flask==1.1.4 PyMySQL==1.0.2 cryptography==36.0.0 ```

Edit the database configuration on the ```db.py``` file, do that by changing the parameters DB (database name), USER (username) and PASSWORD (user's password).

Start the application by executing ```python3 server.py``` and interact with it by opening a window on your browser with the adress [__http://localhost:9001/__](http://localhost:9001/) 

```
$ python3 server.py
2021-11-27 15:07:33 - INFO - Connected to database movie_stream
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2021-11-27 15:07:33 - INFO -  * Running on http://0.0.0.0:9001/ (Press CTRL+C to quit)
```

# Versão Portuguesa

Este projeto foi desenvolvido no âmbito da unidade curricular 'Bases de Dados' pelos alunos [André Sousa](https://github.com/anfisou) e [Paulo Silva](https://github.com/Panda-Hacks) e implementa uma aplicação web sobre uma base de dados relacional das instituições de ensino superior portuguesas.


Deve ter o Python 3, o gestor de pacotes pip instalado e a biblioteca flask. Pode instalar os mesmos usando:

``` sudo apt-get install python3 python3-pip ``` e  ``` pip3 install --user Flask==1.1.4 PyMySQL==1.0.2 cryptography==36.0.0 ```

Edite o ficheiro ```db.py``` no que se refere à configuração da sua BD, modificando os parâmetros DB (nome da base de dados), USER (nome do utilizador) e PASSWORD (senha do utilizador).



Inicie a aplicação executando ```python3 server.py``` e interaja com a mesma
abrindo uma janela no seu browser  com o endereço [__http://localhost:9001/__](http://localhost:9001/) 

```
$ python3 server.py
2021-11-27 15:07:33 - INFO - Connected to database movie_stream
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2021-11-27 15:07:33 - INFO -  * Running on http://0.0.0.0:9001/ (Press CTRL+C to quit)

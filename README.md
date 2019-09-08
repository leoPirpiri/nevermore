# nevermore
Aplicação Web de uma rede social para cumprir a carga horária da disciplina de Banco de Dados

#ajuda para instalar requisitos:

Instalação do pip usando python 3:
    sudo apt install python3-pip

Instalação de um ambiente virtual para visualizar as páginas:
    pip3 install virtualenv

Clone o projeto:
    https://github.com/leoPirpiri/nevermore.git

Dentro da pasta do projeto, crie um ambiente virtual para separar execução do projeto da máquina pessoal.

    virtualenv -p python3 venv (Se encontrado erro, execute: sudo apt install virtualenv e repita o comando)

ativando o ambiente virtual:
    . venv/bin/activate

Instalação dos requerimentos:
    venv/bin/pip3 install -r requirements.txt

executar a aplicação:
    python3 run.py
Ative o ambiente virtual:
    No Linux/macOS: 
        source env/bin/activate

    No Windows (caso você precise): 
        .\env\Scripts\activate

Instalação de Dependências
    Instale tkinter e PyInstaller:
    Para garantir que o tkinter esteja presente, instale-o no sistema (não no ambiente virtual):
        sudo apt-get install python3-tk

    Instale o PyInstaller no ambiente virtual:
        pip install pyinstaller

Criação do Executável
    Ainda com o ambiente virtual ativado, execute:
        pyinstaller --onefile --windowed --hidden-import=tkinter joguinho.py

Encontre o arquivo .exe:
    O executável estará dentro da pasta dist criada na pasta do projeto:
        dist/joguinho

Teste o Executável:
    Se você estiver usando Linux e quer rodar o .exe no Windows, copie o arquivo para um computador com Windows.
    Caso esteja no Linux e precise rodar o arquivo .exe via Wine, execute:  
        wine dist/joguinho.exe
# projetoTRX

**Pré-requisitos**
Antes de rodar o script, é necessário ter o Python instalado no seu sistema e alguns pacotes adicionais.

**Pacotes necessários:**
tronpy: Biblioteca para interagir com a blockchain Tron.
mnemonic: Utilizado para gerar uma chave privada a partir de uma frase mnemônica.
bip32: Utilizado para gerar a chave privada seguindo o padrão BIP32.
time: Biblioteca padrão do Python para manipulação de tempo.



**Instalação**
**Instalar o Python 3:** Certifique-se de que o Python 3 está instalado em seu sistema. Você pode verificar isso com o comando:

```bash
python3 --version
```

**Instalar as dependências:** Execute o seguinte comando para instalar os pacotes necessários:
```bash
pip install tronpy mnemonic bip32
```

**Configuração do Script
No script, você verá a variável mnemonic_phrase que contém a frase mnemônica. Substitua isso pela sua própria frase mnemônica para gerar a chave privada corretamente.**
```bash
mnemonic_phrase = "sua frase mnemônica aqui"
```

**Além disso, você pode modificar o endereço de destino (destination_address) para onde deseja enviar o TRX.**
```bash
destination_address = "TDvxRL3y4Gz8UpM4KHFw3dBcvKdUYf7hm4"
```

**Como Rodar o Script**

Execute o script: Com todos os pacotes instalados e o script configurado corretamente, você pode rodar o script com o seguinte comando:
```bash
python script_name.py
```

Saída Esperada
O script exibirá informações no console sobre o processo de verificação de saldo e transferências realizadas:

![image](https://github.com/user-attachments/assets/14d99ea1-5870-42b6-8e6a-44369781f9c5)


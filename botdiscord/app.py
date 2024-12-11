import discord
import asyncio
from tronpy import Tron
from tronpy.keys import PrivateKey
from mnemonic import Mnemonic
from bip32 import BIP32

# Configurações do bot
TOKEN = 'OTMwNjYwMjY3MDA2NzY3MTE0.GRaonn.bcQVfnhFxS1Fl5Cg0dJ6_wFrK8DuBcZA6AmDV8'  # Substitua pelo seu token do bot
CHANNEL_ID = 1316451919790604359  # Substitua pelo ID do canal onde você quer enviar a mensagem

# Frase mnemônica (chave da wallet principal)
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
    return Tron(network='mainnet')

# Verifica se a conta existe e retorna o saldo
def get_account_balance(client, address):
    try:
        account = client.get_account(address)
        balance = account.get("balance", 0) / 1_000_000  # Converte de "sun" para TRX
        return balance
    except Exception as e:
        print(f"Erro ao verificar a conta: {e}")
        return 0

# Classe do bot
class MyClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.saldos = []  # Lista para armazenar os saldos que entram
        self.soma_total = 0  # Soma total dos saldos enviados

    async def on_ready(self):
        print(f'Bot conectado como {self.user}')
        channel = self.get_channel(CHANNEL_ID)

        # Verifica se o canal foi encontrado
        if channel is None:
            print(f"Erro: Canal com ID {CHANNEL_ID} não encontrado ou o bot não tem acesso a ele.")
            return

        client = create_tron_client()
        address = key.public_key.to_base58check_address()

        # Envia a mensagem inicial
        message = await channel.send("Verificando saldo do TRX...")
        
        while True:
            balance = get_account_balance(client, address)
            if balance > 1:  # Se o saldo for maior que 1 TRX
                self.saldos.append(balance)  # Adiciona o saldo à lista
                self.soma_total += balance  # Atualiza a soma total

            # Cria uma string formatada para os saldos
            saldos_str = "\n".join([f"Entrou: {saldo:.6f} TRX" for saldo in self.saldos])
            # Atualiza a mensagem com os saldos e a soma total
            await message.edit(content=f"Saldo atual: {balance:.6f} TRX\n\nEntrou:\n{saldos_str}\n\nSoma total já enviado: {self.soma_total:.6f} TRX")
            await asyncio.sleep(2)  # Atualiza a cada 2 segundos

# Configura os intents
intents = discord.Intents.default()
intents.messages = True  # Ativa o intent para mensagens

# Inicia o bot
client = MyClient(intents=intents)
client.run(TOKEN)
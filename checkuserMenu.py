
import os
import subprocess
import sys
import socket
import urllib.request
import json

cor_vermelha = "\033[91m"
cor_verde = "\033[92m"
cor_amarela = "\033[93m"
cor_azul = "\033[94m"
cor_reset = "\033[0m"

def adicionar_ao_cache(chave, valor):
    cache = carregar_cache()  
    cache[chave] = valor
    salvar_cache(cache)  

def remover_do_cache(chave):
    cache = carregar_cache()  
    if chave in cache:
        del cache[chave]
        salvar_cache(cache) 

def obter_do_cache(chave):
    cache = carregar_cache()  
    return cache.get(chave)

def carregar_cache():
    try:
        with open('/root/checkuser/cache.json', 'r') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {} 
    
def salvar_cache(cache):
    with open('/root/checkuser/cache.json', 'w') as arquivo:
        json.dump(cache, arquivo)


def get_public_ip():
    try:
        url = "https://ipinfo.io"
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = json.loads(response.read().decode("utf-8"))
            if 'ip' in data:
                return data['ip']
            else:
                print("Endereço IP público não encontrado na resposta.")
                return None
        else:
            print("Falha na solicitação ao servidor.")
            return None
    except Exception as e:
        print("Não foi possível obter o endereço IP público:", str(e))
        return None




def verificar_processo(nome_processo):
    try:
        resultado = subprocess.check_output(["ps", "aux"]).decode()
        linhas = resultado.split('\n')
        for linha in linhas:
            if nome_processo in linha and "python" in linha:
                return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar o processo: {e}")
    return False


nome_do_script = "/root/checkuser/checkuser.py"




if __name__ == "__main__":
    while True:
        os.system('clear')


        if verificar_processo(nome_do_script):
            status = f'{cor_verde}ativo{cor_reset} - porta em uso: {obter_do_cache("porta")}'
        else:
            status = f'{cor_vermelha}parado{cor_reset} - porta que será usada: {obter_do_cache("porta")}'
       
        print(f"Status: {status}")

        print(f"")

        print(f"Selecione uma opção:")
        print(f" 1 - ELIMINAR PORTA 5454")
        print(f" 2 - INICIAR CHECKUSER")
        print(f" 3 - PARAR CHECKUSER")
        print(f" 4 - VERIFICAR LINKS")
        print(f" 5 - SOBRE!!")
        print(f" 0 - SAIR DO MENU")

        option = input("Escolha uma opção: ")

        
if option == "1":
    print("Liberando a porta 5454!")

    # Use subprocess para executar o comando 'lsof' e pegar o PID do processo na porta 5454
    try:
        output = subprocess.check_output(["lsof", "-t", "-i:5454"])
        pid = int(output.strip())

        # Use subprocess para matar o processo com o PID obtido
        subprocess.run(["sudo", "kill", str(pid)])

        print("Porta 5454 liberada, volte ao menu e inicie o checkUser na porta 5454")

    input("\nPressione a tecla Enter para voltar ao menu\n\n")
elif option == "2":
    print(f"Observação: Para funcionar com security apenas se usar a porta 5454 !")
            
            adicionar_ao_cache('porta', input("\nDigite a porta que deseja usar !"))

            os.system('clear')
            print(f'Porta escolhida: {obter_do_cache("porta")}')

            os.system(f'nohup python3 {nome_do_script} --port {obter_do_cache("porta")} & ')

            input(f"\nPressione a tecla enter para voltar ao menu\n\n")
elif option == "3":
    if verificar_processo(nome_do_script):

                try:
                    subprocess.run(f'pkill -9 -f "/root/checkuser/checkuser.py"', shell=True)

                        
                except subprocess.CalledProcessError:
                    print("Erro ao executar o comando.")
                remover_do_cache("porta")
            else: 
                print("O Checkuser não está ativo.")
            


            input(f"Pressione a tecla enter para voltar ao menu")
elif option == "4":
    os.system('clear')
            if verificar_processo(nome_do_script):
                print("Abaixo os apps, e os links para cada um: ")
                print("")
                ip = get_public_ip()
                porta = obter_do_cache("porta")
                print(f" DtunnelMod - http://{ip}:{porta}/dtmod  ")
                print(f" GltunnelMod - http://{ip}:{porta}/gl ")
                print(f" AnyVpnMod - http://{ip}:{porta}/anymod ")
                print(f" Conecta4g - http://{ip}:{porta}/checkUser ")
                print(f" AtxTunnel - http://{ip}:{porta}/atx ")
                print("")

                print("Para usar com security (por favor, use apenas esses links com security e conexões que não usam cloudflare para não sobrecarregar nossos servidores)")
                print("")
                print(f" DtunnelMod - http://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/dtmod  ")
                print(f" GltunnelMod - http://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/gl ")
                print(f" AnyVpnMod - http://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/anymod ")
                print(f" Conecta4g - http://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/checkUser ")
                print(f" AtxTunnel - http://painelconecta5g.com/checkuser.php?url=http://{ip}:{porta}/atx ")
                print("")

            else:
                print("\nInicie o serviço primeiro\n")
            input(f"Pressione a tecla enter para voltar ao menu")
elif option == "5":
    os.system('clear')
            print(f"Olá, esse é um multi-checkuser criado por @UlekBR e editado por @donomodderajuda")
            print(f"Com esse checkuser venho trazendo a possibilidade de usar em diversos apps")
            print(f"Apps como: ")
            print(f" - DtunnelMod")
            print(f" - GlTunnelMod")
            print(f" - AnyVpnMod")
            print(f" - Conecta4g")
            print(f"")
            input(f"Pressione a tecla enter para voltar ao menu")
elif option == "0":
    sys.exit(0)
else:
    os.system('clear')
    print(f"Selecionado uma opção inválida, tente novamente !")
    input(f"Pressione a tecla Enter para voltar ao menu")

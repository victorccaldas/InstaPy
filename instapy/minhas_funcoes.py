#from .login_util import login_user
from selenium.webdriver.common.by import By
from datetime import datetime
import requests
import json
import time

from . import util
from . import instapy
from . import xpath_compile

# achar o caminho relativo do insta_bot e importar.
'''from inspect import getsourcefile
from os.path import abspath
exec_path = abspath(getsourcefile(lambda:0))
from exec_path import session
'''

configs_path = 'C:/Users/Victor/Documents/Python/InstaActionBot/configs.json'

class Telegram:
    with open(configs_path, 'r') as f: userConfigs = json.load(f)

    apikey = userConfigs['telegramBotApiKey']
    groupid = userConfigs['telegramGroupId']
        
    def send(msg):
        send_msg = "https://api.telegram.org/bot"+Telegram.apikey+"/sendMessage?chat_id="+Telegram.groupid+"&text="+msg
        r = requests.get(send_msg)
        print("\n [Telegram]: ", msg, '\n')
        return r

    def read_group():
        def get_text(msg):
            try:
                return (msg['message']['text'], msg['message']['date'])
            except:
                pass

        get_updates = 'https://api.telegram.org/bot{}/getUpdates'.format(Telegram.apikey)
        r = requests.get(get_updates)
        r = r.json()
        group_messages = [i for i in r['result'] if str(i['message']['chat']['id']) == Telegram.groupid]
        last_messages = [get_text(i) for i in group_messages]
        last_messages.remove(None)
        return last_messages

def waitPhoneConfirmationResponse(browser):
    '''
    Fica lendo o Telegram, aguardando resposta com o código.
    '''
    Telegram.send("Qual é o código de verificação no seu SMS? O próximo texto do chat será utilizado (mensagem automática)")
    epoch_start = datetime.now().timestamp()

    while True:
        responses = Telegram.read_group()
        
        # mensagens recebidas depois de enviar mensagem pedindo o codigo
        msgs = [msg for msg, epoch in responses if epoch > epoch_start]
        
        # mais recente primeiro
        msgs.reverse()
            
        if not len(msgs):
            print("\n [Telegram]: Aguardando resposta...\n")
            time.sleep(30)
            continue

        # retorna ultima mensagem recebida
        code = msgs[0]
        Telegram.send(f"Código recebido: '{code}'")
        return code
           

def verificar_link(browser):
    '''
    Verifica se a página esperada está aberta, ou caiu no challenge ou tela de login.

    Deve ser usada após acessar algum link, com driver.get() ou comumente
    no instapy, web_address_navigator().
    '''
    url = util.get_current_url(browser)

    if '/challenge' in url:
        print("################ !!! Challenge detectado !!! ################")
        return
        #1. Função pra clicar no botão de SMS ou Email pra enviar;
        #2. Função pra pedir o codigo de verificação por Telegram e enviar print da tela (apenas pra debug?), 
        # e aguardar até receber

        # clicar no botão de email (ou sms?)
        # email = automatizável porém exige credenciais
        # sms = mais rápido pra ser respondido manualmente
    
    if '/login' in url:
        print("################ !!! Deslog detectado !!! ################")
        
        raise instapy.DeslogError("Deslog detectado")

        try:
            '''login_user(browser,
                username,
                password,
                logger,
                logfolder,
                proxy_address,
                security_code_to_phone,
                security_codes,
                want_check_browser,
            )'''
            #Instapy.login()

            print("Re-Login feito.")
        except:
            print("################ !!! Falha no login !!! ################")
            
        return
        # Efetuar login novamente (modificar funçção de login e adicionar argumento 'relog', 
        # pra sair da função e continuar demais atividades assim que relogar quando relog=True)
    
        
# problema: Essa função será executado pelo web_driver_navigator,
# que por sua vez é executada tb quando vai fazer o login.
# portanto deve ficar um loop infinito.

# Solução:
# Chamar fora do navigator (como era antes),
# sempre que verificar tela de login ou challenge levantar Exception específica,
# tentar executar funções e se a Exception especifica por levantada, session.login novamente 
#from .login_util import login_user
from selenium.webdriver.common.by import By

from . import util
from . import instapy
from . import xpath_compile

# achar o caminho relativo do insta_bot e importar.
'''from inspect import getsourcefile
from os.path import abspath
exec_path = abspath(getsourcefile(lambda:0))
from exec_path import session
'''

#class DeslogError(Exception):
#    pass

def sendPhoneConfirmationAndWaitResponse(browser):
    '''
    Envia SMS de confirmação e aguarda resposta no Telegram.
    '''
    # clicar no botão "Send confirmation"
    browser.find_element(By.XPATH, xpath['page_errors']['confirmNumberButton']).click()

    assert "confirmation sent" in browser.title.lower()
    # aguardar resposta do Telegram


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
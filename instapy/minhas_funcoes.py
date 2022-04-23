from .login_util import login_user

def verificar_link(self, url):
    '''
    Verifica se a página esperada está aberta, ou caiu no challenge ou tela de login.

    Deve ser usada após acessar algum link, com driver.get() ou comumente
    no instapy, web_address_navigator().
    '''
    print('Verificando challenge')
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
        
        try:
            login_user(self.browser,
                self.username,
                self.password,
                self.logger,
                self.logfolder,
                self.proxy_address,
                self.bypass_security_challenge_using,
                self.security_codes,
                self.want_check_browser,
                )
            print("Re-Login feito.")
        except:
            print("################ !!! Falha no login !!! ################")
            
        return
        # Efetuar login novamente (modificar funçção de login e adicionar argumento 'relog', 
        # pra sair da função e continuar demais atividades assim que relogar quando relog=True)
    
        

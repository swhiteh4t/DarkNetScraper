from bs4 import BeautifulSoup
import io
import pycurl
#Importing Stem libraries
import stem
from stem import process
from stem import Signal
from stem.control import Controller
from stem.util import term
from fake_useragent import UserAgent
from DarkNetScraper.output.colors import ColoredText

from DarkNetScraper.output.printer import handle_response_code
from DarkNetScraper.parsers.string_parsers import decode_string
from .config import CONFIG_PORT, CONFIG_IP

class TorConnector:
    #Variables
    tor_process = None
    random_agent = None
    

    def __init__(self,ip=CONFIG_IP,authentication=None,port=CONFIG_PORT,random_agent=False) -> None:
        #Authentication not supported yet
        self.port = port
        self.random_agent = random_agent
        
    # Function to renew Tor identity
    def renew_tor_identity(self):
        print(term.format("Renewing Tor identity...", term.Color.GREEN))
        with Controller.from_port(port=CONFIG_PORT+1) as controller:
            controller.authenticate(password="my_password")
            controller.signal(Signal.NEWNYM)
            
    
    def query(self,url):
        """
        Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
        """
        output = io.BytesIO()
        query = pycurl.Curl()
        query.setopt(pycurl.URL, url)
        query.setopt(pycurl.PROXY, 'localhost')
        query.setopt(pycurl.PROXYPORT, self.port)
        query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
        query.setopt(pycurl.WRITEFUNCTION, output.write)
        if self.random_agent:
            query.setopt(pycurl.HTTPHEADER, [
                'accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-language:en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2'])
            user_agent = UserAgent()
            query.setopt(pycurl.USERAGENT, user_agent.random)
        try:
          query.perform()
          response_code = query.getinfo(pycurl.HTTP_CODE) 
          if response_code >= 200 and query.getinfo(pycurl.HTTP_CODE) < 300:
            query.close()
            try:
                r = output.getvalue().decode()
                return r
            except:
                print(ColoredText("[ E ] Error while decoding query!", 'red'))
            return 
          else:
              handle_response_code(response_code)
              return None
        except pycurl.error as exc:
          return "Unable to reach %s (%s)" % (url, exc)
    
    def print_bootstrap_lines(line,a):
        if "Bootstrapped " in a:
            print(term.format(a, term.Color.BLUE))
    
    def check_my_ip(self):
        print(term.format("[ * ] Tor exit note's IP address : " + 
                          self.query("https://ident.me/"), term.Color.BLUE))
from collections import deque
import queue

from DarkNetScraper.output.printer import print_generic
from DarkNetScraper.parsers.string_parsers import is_digits
from .torconnector import TorConnector
from .extractors.extractor import Extractor
from .parsers.parser import Parser
from .output.colors import ColoredText
from .datamodels import DBConnector
from .nlp.nlp import summarize
from .config import CONFIG_IP,CONFIG_PORT

class Binder:
    connector = None
    args = None

    def __init__(self,ip=CONFIG_IP,port=CONFIG_PORT,args=args):
        self.args = args
        random_agent = True if args.anonimity else False
        self.connector  = TorConnector(ip=ip, port=port, random_agent=random_agent)
        self.connector.renew_tor_identity()
        #Show IP
        if args.verbose:
            print(ColoredText("[ * ] Initating the database ", 'blue'))
            #TODO: Implement the graphs
            self.connector.check_my_ip()
        #self.db = DBConnector()

    def run(self, depth, url=None):
        if depth <= 0 or url is None:
            return
        print(ColoredText("[ * ] Making request to " + url,"white"))
        html = self.connector.query(url=url)
        if html is None:
            return 
        e = Extractor(html=html)
        e.extract_do_all()
        print(ColoredText("[ - ] Title : " +e.title,'magenta'))
        p = Parser(e.content_raw)
        if self.args.verbose:
            self._print_metaatr(e.meta)
            self._print_summary(p)
        #Renew the identity in each request
        if self.args.anonimity:
            self.connector.renew_tor_identity()
            if self.args.verbose:
                self.connector.check_my_ip()
        if self.args.mail:
            self._print_mail(p)
        if self.args.phone:
            self._print_phone(p)
        if self.args.additional:
            self._print_additonal(p)
        #Save to database
        #self.db.save_to_file()
        '''self.db.add_entry(
            title=e.title,
            content=e.title,
            category="",
            summary=
            )'''
        #Traverse other links recursive
        for link in e.links:
            self.run(depth=int(depth)-1,url=link)
        #Proccess with machine learning
    

    def stop(self):
        print(ColoredText("[ * ] Commiting changes to the Database...",'blue'))
        self.connector.stop()

    '''Helper funcitons'''
    def _print_phone(self,parser):
        print_generic(key='phone', data=parser.get_phone_numbers())

    def _print_mail(self,parser):
        print_generic(key='mail', data=parser.get_emails())

    def _print_summary(self,parser):
        print(ColoredText(parser.get_sumary(0.1),'darkmagenta'))
    
    def _print_metaatr(self,meta):
        print(ColoredText("[ - ] Meta tags",'magenta'))
        print(ColoredText("[ - ] " + Parser.get_meta(meta)+"\n",'magenta'))

    def _print_additonal(self, p : Parser):
        keys = ['ip4' ,'ip6' ,'cloud', 'crypto']
        ip4,ip6,cloud,crypto = p.get_additional()
        values = [ip4 ,ip6,cloud,crypto]
        for key,value in zip(keys,values):
            print_generic(key=key,data=value)   
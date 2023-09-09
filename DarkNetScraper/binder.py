from collections import deque
import queue
import random

from DarkNetScraper.output.printer import print_generic
from DarkNetScraper.parsers.string_parsers import is_digits
from .torconnector import TorConnector
from .extractors.extractor import Extractor
from .parsers.parser import Parser
from .output.colors import ColoredText
from .datamodels import DBConnector
from .nlp.nlp import summarize
from .config import CONFIG_IP,CONFIG_PORT
import os,json

class Binder:
    connector = None
    args = None
    visited = None

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
        self.db = DBConnector()
        if os.path.exists('visited.json'):
            self.visited = set(json.loads(open('visited.json').read()))
        else:
            self.visited = set() #Load the set

    def run(self, depth, url=None):
        if depth <= 0 or url is None or url in self.visited:
            return
        
        print(ColoredText("[ * ] Making request to " + url,"white"))
        html = self.connector.query(url=url)
        self.visited.add(url)

        if html is None:
            return 
        e = Extractor(html=html)
        e.extract_do_all()
        print(ColoredText("[ - ] Title : " +e.title,'magenta'))
        p = Parser(e.content_raw)
        if self.args.verbose:
            self.__print_metaatr(e.meta)
            if self.__print_summary(p):
                self.__print_content(p)
        #Renew the identity in each request
        if self.args.anonimity or random.randint(1,10) % 10 == 0:
            self.connector.renew_tor_identity()
            if self.args.verbose:
                self.connector.check_my_ip()
        if self.args.mail:
            self.__print_mail(p)
        if self.args.phone:
            self.__print_phone(p)
        if self.args.additional:
            self.__print_additonal(p)
        
        #Save to database
        #self.db.save_to_file()
        if self.args.classify:
            inp = input(ColoredText("[ ! ] Introduce the category : ",'cyan'))
            category = self.__resolve_categorize(inp)
            if int(inp):
                print(ColoredText("Categorized as "+category,'cyan'))
                self.db.add_entry_generate(
                    title=Parser.remove_non_alphanum(e.title),
                    content=p.content,
                    category=category

          )
        else:
            self.db.add_entry(
            title=Parser.remove_non_alphanum(e.title),
            content=p.content,
            category="", #Trained model response
            summary="" #Trained model response
            )
        #Traverse other links recursive
        for link in e.links:
            self.run(depth=int(depth)-1,url=link)
        #Proccess with machine learning
    

    def stop(self):
        print(ColoredText("[ * ] Commiting changes to the Database...",'blue'))
        if self.args.classify:
            self.db.save_to_file()
        with open('visited.txt', 'w') as file:
            file.write(json.dumps(self.visited, cls=SetEncoder))
        self.db.save_db()

    '''Helper funcitons'''
    def __print_phone(self,parser):
        print_generic(key='phone', data=parser.get_phone_numbers())

    def __print_mail(self,parser):
        print_generic(key='mail', data=parser.get_emails())

    def __print_summary(self,parser):
        summary = parser.get_sumary(0.15)
        print(ColoredText(summary,'darkmagenta'))
        return len(summary) < 10
    
    def __print_metaatr(self,meta):
        print(ColoredText("[ - ] Meta tags",'magenta'))
        print(ColoredText("[ - ] " + Parser.get_meta(meta)+"\n",'magenta'))

    def __print_additonal(self, p : Parser):
        keys = ['ip4' ,'ip6' ,'cloud', 'crypto']
        ip4,ip6,cloud,crypto = p.get_additional()
        values = [ip4 ,ip6,cloud,crypto]
        for key,value in zip(keys,values):
            print_generic(key=key,data=value)   

    def __print_content(self,p: Parser):
        print(ColoredText(p.content,'darkmagenta'))
        
    def __resolve_categorize(self,i):
        categories = {
        "0": "Empty",
        "1" : "Pornography",
        "2" : "Bitcoin related services",
        "3" : "Drugs",
        "4" : "Violence",
        "5" : "C. Credit Cards",
        "6" : "C. Money",
        "7" : "C. Personal",
        "8" : "Piracy",
        "9" : "Hacking",
        "10" : "Malware",
        "11" : "Ilegal Marketplace",
        "12" : "Services",
        "14" : "Fraud",
        "15" : "Human-Trafficking",
        "16" : "Leaked documents",
        "17" : "Directory/Wiki",
        "18" : "Art & Music",
        "19" : "Casino & Gambling",
        "20" : "Privacy",
        "21" : "Cryptocurrency",
        "22" : "Forum",
        "23" : "Marketplace",
        "24" : "Library & Books",
        "25" : "Jorunalism",
        "26" : "Personal",
        "27" : "Politics",
        "28" : "Religion",
        "29" : "Hosting & Software"}
        return categories[i]
    
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

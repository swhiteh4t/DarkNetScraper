import re
import json
from .verifier import validate_email
from ..nlp.nlp import remove_stop_words, summarize
from .string_parsers import remove_non_alphanumeric
from .regex import stalker

class Parser:

    def __init__(self,content : str) -> None:
        self.content = Parser.remove_blank(remove_non_alphanumeric(content))
        self.restalk = stalker.reStalker(all=True)



    def get_word_occurrences(self):
        # Initialize a defaultdict to store word occurrences
        word_occurrences = dict(int)

        # Tokenize the input string into words using regex
        words = re.findall(r'\w+', remove_stop_words(self.content.lower()))

        # Count the occurrences of each word
        for word in words:
            if len(word) > 3 and not word.isdigit():
                word_occurrences[word] += 1

        keys_del = []
        for key, value in word_occurrences.items():
            if value < 3:
                keys_del += key

        for key in keys_del:
            del word_occurrences[key]
        return word_occurrences
    
    def sorted_word_ocurrences(self):
        return sorted(self.extract_word_occurrences(self.content).items(), key=lambda x: x[1], reverse=True)
    
    def get_emails(self):
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', self.content)
        checked_emails = []
        for email in emails:
            if validate_email(email):
                checked_emails += email
        return checked_emails

    def get_phone_numbers(self):
        r = []
        r += re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', self.content)
        r += re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', self.content)
        return r
        
    def get_cloud_services(self,strict=False):
        regex_aws_subdomain = r'([a-zA-Z0-9-]+\.s[a-zA-Z0-9-]+\.amazonaws\.com)' if strict else r'([\w.-]+s[\w.-]+\.amazonaws\.com)'
        return re.findall(regex_aws_subdomain, self.content)
    
    def get_crypto_address(self):
        regex_bitcoin = r'\b[13][a-km-zA-HJ-NP-Z0-9]{26,33}\b'
        regex_crypto = r'(?:(?:0x[0-9a-fA-F]{40})|(?:[13][a-km-zA-HJ-NP-Z0-9]{26,33}))'
        return re.findall(regex_bitcoin, self.content) + re.findall(regex_crypto, self.content)
    
    def get_ipv4_address(self):
        regex_ipv4 = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        return re.findall(regex_ipv4, self.content)
    
    def get_ipv6_address(self):
        regex_ipv6 = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
        return re.findall(regex_ipv6, self.content)

    def get_additional(self):
        return self.get_ipv4_address(),self.get_ipv6_address(),self.get_cloud_services(),self.get_crypto_address()
    
    def get_sumary(self,p=0.15):
        return summarize(remove_non_alphanumeric(self.content),p) + "\n"
    
    #Anadir get ocurrences
    
    #Añadir stalker

    
    @staticmethod
    def get_meta(s):
        r = ""
        for index, item in enumerate(s):
            for key, value in item.items():
                r += f"'{key}': '{value}'"
        return r
    
    @staticmethod
    def remove_blank(s):
        return s.replace('\n','').replace('\t','').replace('\r','').replace(',','')
    
    @staticmethod
    def remove_non_alphanum(s):
        return remove_non_alphanumeric(s)
    
    def _remove_duplicates(l):
        return list(dict.fromkeys(l))
    

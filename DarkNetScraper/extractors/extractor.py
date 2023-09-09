from bs4 import BeautifulSoup
from ..parsers.verifier import validate_link, validate_link_onion
from ..parsers.parser import remove_non_alphanumeric

class Extractor:
    title = None # Variable to store the title extracted from HTML content
    description = None # Variable to store the description extracted from HTML conten
    html = None # Variable to store the HTML content,
    content_raw = None # Variable to store the HTML text content without parsing
    main_titles = None #Variable to store the main headers and subheaders h1,h2,h3...
    paragraphs = None 
    meta = None
    link_and_titles = dict()
    links = []

    #The extractor receives the html content
    def __init__(self,html,encoding='utf-8') -> None:
        self.html = BeautifulSoup(html, 'html.parser')

    def extract_properties(self):
        """
        Extracts and assigns the title and description properties from the HTML content.

        This method finds and assigns the title and description properties from the HTML content to
        instance variables 'title' and 'description'. If the 'meta' tag with 'name' attribute equal
        to 'description' contains a 'content' attribute, it will be assigned as the description;
        otherwise, an empty string will be assigned.

        :return: None
        """
        
        self.title = self.html.find('title').text if self.html.find('title') else "No title"
        self.description = self.html.find('meta', attrs={'name': 'description'})
        if "content" in str(self.description):
            self.description = self.description.get("content")
        else:
            self.description = ""


    def extract_content_raw(self):
        if self.content_raw is None:
            self.content_raw = self.html.get_text() 

    def extract_main_titles(self):
        """
        Extracts and combines first, second, and third-order titles from the HTML content.

        :return: A tuple containing concatenated first, second, and third-order titles as strings.
        :rtype: None
        """
        level = 3
        if self.main_titles is not None:
            #Extract as many header titles as the user wants
            headers = []
            for i in range(1,level+1):
                hx = self.html.find_all('h' + str(i))
                hx_all = ""
                for x in range (len(hx)):
                    if x ==  len(hx) -1:
                        hx_all = hx_all + hx[x].text
                    else:
                        hx_all = hx_all + hx[x].text + ". "
            #Set the value of the level of the headers and heards' value
            self.main_titles += hx_all
            self.header_level = level
    
    def extract_paragraph(self):
        """
        Extracts and combines paragraphs from the HTML content.

        :return: A concatenated string containing all paragraphs.
        :rtype: None
        """
        if self.paragraphs is not None:
            p_all = ""
            p = self.html.find_all('p')
            for x in range (len(p)):
                if x ==  len(p)-1:
                    p_all = p_all + p[x].text
                else:
                    p_all = p_all + p[x].text + ". "
            self.paragraphs = ' '.join(p_all)

    def extract_links(self):
        """
        Extracts and returns all valid links from the provided HTML content.

        :param html: The HTML content in which links will be searched.
        :type html: str

        :return: A list of valid link URLs.
        :rtype: list of str
        """
        links = set()
        if not len(self.links):
            for tag in self.html.find_all('a'):
                link = tag.get('href')
                if validate_link_onion(link):
                    links.add(link)
            self.links = list(links)
            
    def extract_meta_tags(self):
        """Retrieve all meta elements from HTML object.

        Returns:
            list: List containing content from meta tags
        """
        meta_tags = self.html.find_all('meta')
        self.meta = []
        for tag in meta_tags:
            self.meta.append(tag.attrs)
    
    def extract_links_titles(self,clean_titles=False):
        """
        Extracts links and their titles from the HTML content.

        Args:
            clean_titles (bool): If True, clean the titles by removing non-alphanumeric characters.

        Returns:
            None
        """
        i = 0
        d = dict()
        for link in self.html.find_all('a'):
            href = link.get('href')
            title = link.get_text()
            if validate_link(href):
            #Check the text of the <a> tag
                if not title.find("https:") or not title.find("http:"):
                    next_sb = link.find_next_sibling(string=True)
                    if  not next_sb is None:
                        title = next_sb.strip()
                    else:
                        title = "not-named" + str(i)
                        i+=1
                title = remove_non_alphanumeric(title) if clean_titles else title
            self.link_and_titles[title] = href
        



    def get_all_content(self):
        """
        Combines various parts of the HTML content into a single string.

        :return: A string containing the title, description, main titles, and paragraphs.
        :rtype: str
        """
        t1, t2, t3 = self.main_titles[0],self.main_titles[1],self.main_titles[2]
        return self.title + " " + self.description + " " + t1 + " " + t2 + " " + t3 + " " + self.get_paragraph()  
    
    def extract_do_all(self):
        # List all functions in the class
        functions = [func for func in dir(self) if callable(getattr(self, func)) and func.startswith('extract_') and func != 'extract_do_all']
        # Call each function in the list
        for func_name in functions:
            func = getattr(self, func_name)
            func()

    
# Example usage:
'''if __name__ == "__main__":
    with open('./examples/ShadowWiki.html','r') as file:
        e = Extractor(file.read())
        print(e.get_all_content())'''
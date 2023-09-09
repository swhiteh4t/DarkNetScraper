import re
import pickle, json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
    
with open('res.txt','r') as file:
    input_string = file.read()
# Define regular expressions to match onion links and titles
onion_link_pattern = r'Making request to (http:\/\/[a-z0-9\.]+\.onion\/)'
title_pattern = r'\[ - \] Title : (.+)'

# Find all matches for onion links and titles
onion_links = re.findall(onion_link_pattern, input_string)
titles = re.findall(title_pattern, input_string)

file = open('visited.json', 'w')
j = json.dumps(onion_links)
print("http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/" in j)
file.write(j)
file.close()
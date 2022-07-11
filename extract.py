#

import re

def classify(info):
    classified_info = {'email': [], 'phone': [], 'address': [], 'info': []}
    for i in info:
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', i):
            classified_info['email'].append(i)
        elif i.lower().startswith('phone'):
            classified_info['phone'].append(i)
        elif re.match('((NE|NW|SE|SW)\s)|(Box|box)\s[0-9]+', i):
            classified_info['address'].append(i)
        else:
            classified_info['info'].append(i)
    return classified_info    

def record(name, info):   
    # Attempt to classify info as email, phone, address, or info
    classified_info = {'name': name, **classify(info)}
    print(classified_info)


def norm(str):
    return re.sub(r'\s+', ' ', str)
    
# The doc is organizes in blocks separated by h4 tags
# parse each block and extract the info
# this is a nice generator to do so
class Extractor:
    def __init__(self, doc):
        self.doc = doc
    
    def __iter__(self):
        self.elems = self.doc.xpath('//h3/following-sibling::h4')
        return self
    
    def __next__(self):
        if not self.elems:
            raise StopIteration
        
        elem = self.elems.pop(0)
        name = norm(elem.text).title()
    
        # Get all info text until the next h4 tag
        info = list()
        nxt = elem.getnext()
        while nxt != None and nxt.tag != 'h4':
            # Exit out if we hit the end (class = "contenttable")
            if nxt.get('class') == 'contenttable':
                break
            
            # Record our info
            info.extend(norm(x.strip()) for x in nxt.xpath('.//text()') if norm(x.strip()))
            nxt = nxt.getnext()
        
        return name, info
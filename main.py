
import re
import os
import csv

import lxml.html
from extract import Extractor
from gender import analyze

def classify(info):
    # Attempt to put info into one of the following categories:
    classified_info = {'email': [], 'phone': [], 'address': [], 'standing': [], 'info': []}
    for i in info:
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', i):
            classified_info['email'].append(i)
            
        elif re.match(r'^(phone|mobile)', i, re.IGNORECASE):
            i = re.sub(r'^(phone|mobile)(:?)', '', i, flags=re.IGNORECASE).strip()
            classified_info['phone'].extend(i.split(','))
            
        elif re.match(r'((NE|NW|SE|SW)\s)|(Box|box)\s[0-9]+', i):
            classified_info['address'].append(i)
            
        elif re.match(r'freshman|sophomore|junior|senior|graduate|lecturer|professor|teach(er|ing)|dean|affiliate|associate|adjunct|faculty|staff|technician|supv|research|lead', i, flags=re.IGNORECASE):
            classified_info['standing'].append(i)
            
        else:
            classified_info['info'].append(i)
    return classified_info    


if __name__ == '__main__':
    # For each file in the inputs directory, extract the info
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'email', 'phone', 'address', 'standing', 'info', 'gender', 'certainty']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for file in os.listdir('inputs'):
            print("Reading input: " + file)
            with open('inputs/' + file, 'r') as f:
                doc = lxml.html.fromstring(f.read())
            
            extractor = Extractor(doc)
            for elem in extractor:
                info = {'name': elem[0]}
                
                # Classify info
                info = {**info, **classify(elem[1])}
                
                # Predict gender
                gender = analyze(elem[0])
                info = {**info, 'gender': gender['result'], 'certainty': gender['diff']}
                
                # Normalize lists
                info = {k: (', '.join(v) if isinstance(v, list) else v) for k, v in info.items()}
                
                # Record info
                writer.writerow(info)  
    print("Done!")
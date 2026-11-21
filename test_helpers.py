import json
import re
import os
import math
import hashlib

def get_hash_seed(s):
    return int(hashlib.md5(s.encode('utf-8')).hexdigest()[:8], 16)

def clean_text_chem(text):
    if not text:
        return ""
    t = text.replace('\t', ' ').replace('\r', '')
    # Replace en-dash with standard hyphen
    t = t.replace('–', '-').replace('—', '-')
    # Normalize spaces
    t = re.sub(r' +', ' ', t)
    return t.strip()

def extract_metadata(raw_text):
    t = clean_text_chem(raw_text)
    
    # 1. Extract C/W accuracy stats
    accuracy_pct = None
    m_c = re.search(r'C\s*[-:]\s*([\d\.]+)\s*W\s*[-:]\s*([\d\.]+)(?:\s*UA\s*[-:]\s*([\d\.]+))?', t, re.I)
    if m_c:
        try:
            accuracy_pct = float(m_c.group(1))
        except:
            pass
        # Remove C-xx W-yy UA-zz from text
        t = re.sub(r'C\s*[-:]\s*[\d\.]+\s*W\s*[-:]\s*[\d\.]+(?:\s*UA\s*[-:]\s*[\d\.]+)?', '', t, flags=re.I)
    
    # 2. Extract exam tag e.g. [6 April, 2023 (Shift-I)] or (JEE Adv. 2017) or (IIT JEE 1983)
    exam_source = None
    m_exam = re.findall(r'(\[(?:\d+\s+[A-Za-z]+,?\s*\d+|\d+\s+[A-Za-z]+|\d+th\s+[A-Za-z]+|\w+\s*\d+)[^\]]*\]|\((?:JEE\s*Adv|JEE\s*Main|IIT\s*JEE|AIEEE)[^\)]*\))', t, re.I)
    if m_exam:
        exam_source = m_exam[-1].strip('[]() ')
        # We can keep exam_source clean
        for tag in m_exam:
            t = t.replace(tag, '')
            
    # Remove leftover headers / page artifacts
    t = re.sub(r'(?:^|\n)\s*(?:JEE-Main|JEE-Advanced|Multiple Correct|Single Correct|Numerical/Integer Types|Fill in the Blanks|True/False|Subjective)\s*', ' ', t)
    t = re.sub(r'(?:^|\n)\s*\d+\s+(?:JEE Main and Advanced Chemistry PYQs|Structure of Atom|Chemical Bonding|Nomenclature.*|Hydrocarbon.*)\s*', ' ', t)
    
    # Normalize spaces again
    t = re.sub(r'\n{3,}', '\n\n', t)
    t = re.sub(r' +', ' ', t).strip()
    return t, accuracy_pct, exam_source

def clean_option(opt):
    if not opt:
        return ""
    opt = clean_text_chem(opt)
    # Split at any subsequent question start or book headers
    opt = re.split(r'\n\s*(?:[A-Z][a-z]+ Leading to|\d+\.|\bJEE-Main|\bStructure of Atom|\bAtomic Structure|\bJEE Main and Advanced)', opt)[0].strip()
    return opt

print("Helper functions defined.")

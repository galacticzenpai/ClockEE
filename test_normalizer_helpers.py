import os
import re
import json
import hashlib
import glob
import pymupdf

def get_hash_int(s, mod):
    h = int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)
    return h % mod

def clean_text_math(text):
    if not text:
        return ""
    text = text.replace('\t', ' ').replace('\r', '')
    # Remove MathType private use area corrupted characters
    text = re.sub(r'[\uf8eb\uf8ec\uf8ed\uf8ee\uf8ef\uf8f0\uf8f1\uf8f2\uf8f3\uf8f4\uf8f5\uf8f6\uf8f7\x08]', '', text)
    # Normalize dashes and spaces
    text = text.replace('–', '-').replace('—', '-')
    text = text.replace('×', r'\times ').replace('÷', r'\div ')
    text = text.replace('≠', r'\neq ').replace('≤', r'\le ').replace('≥', r'\ge ')
    text = text.replace('∈', r'\in ').replace('∉', r'\notin ')
    text = text.replace('⊂', r'\subset ').replace('∩', r'\cap ').replace('∪', r'\cup ')
    text = text.replace('°', r'^\circ ')
    
    # Clean multiple spaces
    text = re.sub(r' +', ' ', text)
    return text.strip()

def extract_exam_source(text):
    exam_source = "JEE Main PYQ"
    # Match patterns like [10 April, 2019 (Shift-II)] or [JEE Adv. 2018]
    m = re.search(r'\[([^\]]*(?:20\d\d|19\d\d|Shift|IIT|JEE)[^\]]*)\]', text)
    if m:
        exam_source = m.group(1).strip()
        text = text[:m.start()] + text[m.end():]
    return text.strip(), exam_source

def clean_option(opt):
    if not isinstance(opt, str):
        return str(opt)
    opt = clean_text_math(opt)
    # Split on bleeding question headers like \n 103. or \nLogarithm\n or \nANSWER KEY
    opt = re.split(r'\n\s*(?:[A-Z][a-zA-Z\s]+)?\n?\s*\d+\.\s+', opt)[0].strip()
    opt = re.split(r'\n\s*ANSWER\s+KEY', opt, flags=re.I)[0].strip()
    opt = re.split(r'\n\s*HINTS', opt, flags=re.I)[0].strip()
    return opt

def extract_fused_question(opt, parent_q):
    m = re.search(r'\n\s*(\d+)\.\s+([A-Z].*?)(?=\n\s*(?:\([a-d1-4]\)|\[|\bANSWER|\Z))', opt, re.DOTALL)
    if not m:
        return None
    qnum = int(m.group(1))
    rest = opt[m.start():]
    
    # Try to find options inside rest
    opt_matches = list(re.finditer(r'(?:^|\n|\t)\s*\(([a-d1-4])\)\s*\t?\s*', rest))
    options = []
    q_text = ""
    if opt_matches:
        q_text = rest[m.start() - opt.find(rest):opt_matches[0].start()].strip()
        for j, om in enumerate(opt_matches):
            ostart = om.end()
            oend = opt_matches[j+1].start() if j+1 < len(opt_matches) else len(rest)
            options.append(clean_option(rest[ostart:oend].strip()))
    else:
        q_text = m.group(2).strip()
    
    # Clean q_text of leading number
    q_text = re.sub(r'^\s*\d+\.\s*', '', q_text).strip()
    
    return {
        'num': qnum,
        'chapter': parent_q.get('chapter'),
        'text': q_text,
        'options': options,
        'referenceBook': parent_q.get('referenceBook', '')
    }

print("Loaded normalization helper prototypes.")

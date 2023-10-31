import re 
from urllib.parse import urlparse


def get_domain(url_text:str) -> str:
    domain = urlparse(url_text).netloc
    return str(domain)


def polish_text(extracted_text: str) -> str:
    excape_words = ['...', 'title=', 'source=', 'product', 'products', '/']
    big_regex = re.compile('|'.join(map(re.escape, excape_words)))
    text_removed_words = big_regex.sub(' ', extracted_text)
    text = re.sub(r'[-{}%=&]', ' ', text_removed_words)
    text = text.strip()
    return re.sub(' +', ' ', text)


def get_raw_after_products(url_text: str) -> list[str]:
    domain = get_domain(url_text)
    text = url_text.split(domain)[-1]
    # products_lst = re.findall(r'/product([a-zA-Z0-9])/[a-zA-Z0-9\u00C0-\u024F-{}/%=&.]+', url_text)
    # products_lst = [item.split('http')[0].split('/product')[-1] for item in set(products_lst)]
    # products_lst = [polish_text(text) for text in products_lst]
    # if len(products_lst) == 0:
    #     products_lst = ['']
    # text = ' '.join(products_lst)
    return polish_text(text)
    # return text 


# def get_raw_before_products(url_text: str) -> list[str]:
#     products_lst = re.findall(r'[a-zA-Z0-9\u00C0-\u024F-{}/%=&.]+/product/', 
#         url_text)
#     domain = urlparse(url_text).netloc + '/'     
#     products_lst = [item.split(domain)[-1].split('products')[0] for item in set(products_lst)]
#     products_lst = [polish_text(text) for text in products_lst]
#     if len(products_lst) == 0:
#         products_lst = ['']
#     text = ' '.join(products_lst)
#     return text

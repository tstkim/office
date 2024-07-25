# extract_options.py

from 스타스포츠.folder_setup import *

def extract_options(product_element):
    options = "옵션 없음".split("\n")
    formatted_options = []
    for option in options:
        if "없음" not in option:
            option = option.replace(" (품절)", "").replace(",", "")
            if "(+" in option:
                name, extra_price = option.split("(+")
                extra_price = extra_price.replace("₩)", "").strip()
                formatted_option = f"{name}=={extra_price}=10000=0=0=0="
            else:
                parts = option.split("==")
                if len(parts) == 2:
                    name, extra_price = parts
                    formatted_option = f"{name}=={extra_price}=10000=0=0=0="
                else:
                    formatted_option = f"{option}==0=10000=0=0=0="
            formatted_options.append(formatted_option)
    return formatted_options

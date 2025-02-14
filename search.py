import requests
from bs4 import BeautifulSoup
from sheet import append_data,sheet

def fetch(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.text
    except requests.exceptions.RequestException as e:
        # print(f"Lỗi khi truy cập {url}: {e}")
        return None
def parse_word(soup):
    word = soup.find('h1',class_='headword')
    return word.text.strip()
def parse_type(soup):
    type = soup.find('span',class_='pos')
    return type.text.strip()

def parse_definitions_examples(soup):
    definitions = []
    # Lặp qua từng phần tử chứa định nghĩa
    for index, sense in enumerate(soup.find_all("li", class_="sense"),1):
        definition = sense.find("span", class_="def")
        if definition:
            # Thêm định nghĩa vào danh sách
            definition_text = str(index)+". " + definition.text.strip()
            definitions.append({"definition": definition_text, "examples": []})

            # Lấy các ví dụ tương ứng với định nghĩa
            examples = sense.find("ul", class_="examples")
            if examples:
                for i, example in enumerate(examples.find_all("li"), 1):
                    example_text = example.text.strip()
                    definitions[-1]["examples"].append(f"{len(definitions)}.{i} {example_text}")

    return definitions

def parse_pronunciation(soup):
    pronunciation = {}
    bristish_phone= soup.find('div',class_='phons_br')
    n_am_phone= soup.find('div',class_='phons_n_am')
    pronunciation['br'] = bristish_phone.find('span',class_='phon').text.strip()
    pronunciation['n_am'] = n_am_phone.find('span',class_='phon').text.strip()
    
    return pronunciation

def parse_idioms(soup):
    idioms = soup.find('div',class_='idioms')
    temp_string = ''
    try:
        for i, idiom in enumerate(idioms.find_all('span',class_='idm-g'),1):
            idm = idiom.find('span',class_='idm')
            sense = idiom.find('span',class_='def')
            temp_string+=str(i) + '. '+ idm.text.strip()+':' +sense.text.strip() + '\n'
        return temp_string
    except: 
        return ''    
def parse_html(html, variants):
    soup = BeautifulSoup(html, "html.parser")
    parsed_response = {}

    if 'definitions_examples' in variants:
        definitions = parse_definitions_examples(soup)
        parsed_response['definitions_examples'] = definitions  # Sử dụng key-value hợp lệ

    if 'pronunciation' in variants:
        pronunciation = parse_pronunciation(soup)
        parsed_response['pronunciation'] = pronunciation

    if 'idioms' in variants:
        idioms = parse_idioms(soup)
        parsed_response['idioms'] = idioms 

    if 'word' in variants:
        p_word = parse_word(soup)
        parsed_response['word'] = p_word 

    if 'type' in variants:
        word_type = parse_type(soup)  # Đổi tên tránh trùng từ khóa
        parsed_response['type'] = word_type

    return parsed_response


def search_word(word):
    base_url = "https://www.oxfordlearnersdictionaries.com/definition/english"
    types = ["_1", "_2", "_3", "_4","_5"]  # Các loại từ phổ biến
    type_success = []
    for i,t in enumerate(types, 1):
        url = f"{base_url}/{word}{t}"
        html = fetch(url)
        if html:
            parsed_data = parse_html(html,['type'])
            type_success.append(t)
            print(f"{i}.Tìm thấy từ '{word}' [{parsed_data['type']}]")

    done = False if len(type_success)>0 else True 
    if not done:
        print("[In vào GoogleSheet]:\n -- nhập 'print' hoặc 'P' để in toàn bộ \n -- nhập số thứ tự để in một từ\n -- nhập 0 để bỏ qua")
        while not done:
            command = ""
            command=input(':')
            if command == 'print' or command == 'P':
                for t in type_success:
                    print('...')
                    url =  f"{base_url}/{word}{t}"
                    get_and_print(url)
                done=True
            elif '_'+command in type_success:
                print('...')
                url = f"{base_url}/{word}_{command}"
                get_and_print(url)
                done = True
            elif command == "0":
                done = True
                print("--Bỏ qua--.")
            else:
                print('sai cú pháp, nhập 0 để bỏ qua.')

def handle_definitions_examples(data):
    definitinons= ''
    examples = ''
    for i,entry in enumerate(data,1):
        # print(f"{i}: {entry['definition']}")
        definitinons+=entry['definition']+'\n'
        for example in entry["examples"]:
            # print(f"{example}")
            examples+=example + '\n'
    return [definitinons,examples]
def get_and_print(url):
    html = fetch(url)
    if html:
        parsed_data = parse_html(html,['word','type','definitions_examples','pronunciation','idioms'])
        [definitions,examples]=handle_definitions_examples(parsed_data['definitions_examples'])
        new_row = [parsed_data['word'],parsed_data['type'],f"UK: {parsed_data['pronunciation']['br']}\nUS: {parsed_data['pronunciation']['n_am']}",definitions,parsed_data['idioms'],examples]
        append_data(sheet,new_row)
        print(f'Đã thêm vào "{parsed_data['word']}"[{parsed_data['type']}] vào google sheet')
            
# Tra cứu từ "run"
# search_word("run")
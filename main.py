from search import search_word

# import asyncio



def convert_string(input_string):
    # Chuyển đổi chuỗi về chữ thường
    lower_string = input_string.lower()
    # Thay thế dấu cách bằng dấu '-'
    result_string = lower_string.replace(' ', '-')
    return result_string

def run_app():
    # new_data = ['word', 'type', 'pronunciation','definition','examples','idioms','examples_with_idioms']
    # append_data(sheet, new_data)
    print('[Oxford - GoogleSheet]')
    quit = False
    while not quit:
        command = input("--- Nhập từ cần tìm. Thoát bằng cách nhập 'q!' ---\n: ")
        if command == "q!":
            quit = True
        else:
            # await mainfunc(command)
            print(f"Đang tìm từ '{command}' ...")
            word = convert_string(command)
            search_word(word)
            # print("\n\n>RETURNING TO MENU:")
    print("--Thoát.")

# asyncio.run(run_app())
run_app()
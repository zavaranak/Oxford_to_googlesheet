import gspread
from google.oauth2.service_account import Credentials
import os
import sys

def get_secret_path():
    # Kiểm tra xem ứng dụng đang chạy dưới dạng file .exe hay không
    if getattr(sys, 'frozen', False):
        # Nếu là file .exe, sử dụng thư mục _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Nếu không, sử dụng thư mục hiện tại
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Trả về đường dẫn đến file secret.json
    return os.path.join(base_path, 'secret.json')
# Cấu hình phạm vi (scopes)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Đường dẫn đến file service account
SERVICE_ACCOUNT_FILE = get_secret_path()

# Khởi tạo xác thực
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Mở Google Sheets bằng ID
sheet_id = '1qTEarY3KpIkSigYCStlZoOTZh3grEqlCanRohKvkugU'
sheet = client.open_by_key(sheet_id).sheet1

# def setup_sheet(sheet):
#     data = sheet.get_all_values()
#     if not data: 
#         header = ['Column 1', 'Column 2', 'Column 3']
#         sheet.update(values=[header], range_name='A1')
#         print("Header đã được thiết lập.")
#     else:
#         print("Bảng đã có dữ liệu.")

# Ghi tiếp dữ liệu vào bảng
def append_data(sheet, new_data):
    sheet.append_row(new_data)
    print("Dữ liệu đã được thêm vào bảng.")


# # Thêm dữ liệu mới
# new_data = ['Data 1', 'Data 2', 'Data 3\nData 4']
# append_data(sheet, new_data)
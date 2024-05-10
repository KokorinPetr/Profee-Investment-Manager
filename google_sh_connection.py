import gspread
from google.oauth2.service_account import Credentials

from pprint import pprint

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1A3la04NEFh3fQA_g-X8n4bdezL2b-86Z87dHvKTy8XY'
sheet = client.open_by_key(sheet_id)

#values_list = sheet.sheet1.cell(6, 1)
values_list_2 = sheet.sheet1.get_all_records()
#pprint(values_list)
currency_cell = sheet.sheet1.find('JPY')

cell_modif = currency_cell.address
price = sheet.sheet1.cell(currency_cell.row, currency_cell.col + 1)

#print(price.numeric_value)
###print(cell_modif)



class GetCurrencyRate:
    import gspread
    from google.oauth2.service_account import Credentials
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets'
    ]

    creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = '1A3la04NEFh3fQA_g-X8n4bdezL2b-86Z87dHvKTy8XY'
    sheet = client.open_by_key(sheet_id)

    def get_rate(self, currency):
        currency_cell = sheet.sheet1.find(currency)
        if currency_cell is None:
            return 'Currency not in our base yet'
        #cell_modif = currency_cell.address
        price = sheet.sheet1.cell(currency_cell.row, currency_cell.col + 1)
        return price.numeric_value

from dotenv import dotenv_values
import gspread

config = dotenv_values('.env')

google_credentials = gspread.service_account(filename=config['CREDENTIALS_TABLE'])
google_sheet = google_credentials.open_by_url(config['URL_TABLE'])
sheet_with_connectors = google_sheet.worksheet(config['WORKSHEET'])

directory_for_photos = config['DIRECTORY_FOR_PHOTOS']

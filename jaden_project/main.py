from google.oauth2 import service_account
from googleapiclient.discovery import build
SERVICE_ACCOUNT_FILE = 'gs_key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1vZVur1ov5SRKKY5tSMH0HbabmpLFHKJOzTvtTAUzbgk'

service = build('sheets','v4',credentials=creds)

sheet = service.spreadsheets()

result = sheet.values().get(spreadsheetId = SAMPLE_SPREADSHEET_ID,range="OutletValidation").execute()

values = result.get('values',[])

print(values[1::])
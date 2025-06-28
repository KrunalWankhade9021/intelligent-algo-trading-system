import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from config import GOOGLE_CREDS_FILE, SHEET_NAME

def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME)

def log_trade(sheet, trade_data):
    sheet.worksheet("Trade Data").append_row(trade_data)

def apply_conditional_formatting():
    # Reuse the same credentials for the Sheets API
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_CREDS_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    # Build the Sheets API service
    service = build('sheets', 'v4', credentials=creds)

    # Open sheet to get spreadsheetId and sheetId
    gc = gspread.authorize(creds)
    sh = gc.open(SHEET_NAME)
    worksheet = sh.worksheet("Trade Log")
    spreadsheet_id = sh.id
    sheet_id = worksheet._properties['sheetId']

    # Build the formatting requests
    requests = [
        # Green text if Return > 0
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startColumnIndex": 1, "endColumnIndex": 2}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=VALUE(REGEXREPLACE(B2, "%", "")) > 0'}]
                        },
                        "format": {"textFormat": {"foregroundColor": {"green": 0.6}}}
                    }
                },
                "index": 0
            }
        },
        # Red text if Return < 0
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startColumnIndex": 1, "endColumnIndex": 2}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=VALUE(REGEXREPLACE(B2, "%", "")) < 0'}]
                        },
                        "format": {"textFormat": {"foregroundColor": {"red": 0.8}}}
                    }
                },
                "index": 1
            }
        },
        # Highlight + Bold if ML Accuracy > 50%
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startColumnIndex": 3, "endColumnIndex": 4}],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{"userEnteredValue": '=VALUE(REGEXREPLACE(D2, "%", "")) > 50'}]
                        },
                        "format": {
                            "backgroundColor": {"red": 1, "green": 1, "blue": 0.6},
                            "textFormat": {"bold": True}
                        }
                    }
                },
                "index": 2
            }
        }
    ]

    # Apply formatting
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}
    ).execute()

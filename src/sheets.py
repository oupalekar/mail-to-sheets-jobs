# sheets.py
# Handles Google Sheets API authentication and writing rows
import utils

class Sheet:
    def __init__(self, spreadsheet_file_name):
        # Use Drive API to find or create the spreadsheet
        self.drive_service = utils.authenticate_google('drive', 'v3')
        self.sheets_service = utils.authenticate_google('sheets', 'v4')
        self.spreadsheet_file_name = spreadsheet_file_name
        self.check_if_sheet_exists()

    def check_if_sheet_exists(self):
        print("Checking if sheet exists...")
        results = self.drive_service.files().list(
            q=f"name='{self.spreadsheet_file_name}' and mimeType='application/vnd.google-apps.spreadsheet'",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        files = results.get('files', [])
        if files:
            spreadsheet_id = files[0]['id']
            self.spreadsheet_id = spreadsheet_id
            print("Sheet exists with ID:", spreadsheet_id)
            return
        else:
            file_metadata = {
                'name': self.spreadsheet_file_name,
                'mimeType': 'application/vnd.google-apps.spreadsheet'
            }
            spreadsheet = self.drive_service.files().create(body=file_metadata, fields='id').execute()
            self.spreadsheet_id = spreadsheet['id']
            print("Sheet created with ID:", self.spreadsheet_id)
            return

    def append_rows(self, rows):
        """
        Append rows to the specified Google Sheet.
        """
        # Appends to the first sheet (Sheet1) starting at A1
        result = self.sheets_service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body={
                'values': rows
            }
        ).execute()
        print(f"Appended {len(rows)} rows to the spreadsheet.")

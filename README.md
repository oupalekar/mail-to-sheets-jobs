# Project: mail-to-sheets-jobs

This project fetches emails from Gmail, analyzes the text, and sends relevant rows to Google Sheets.

## Setup

1. **Google Cloud Project:**
   - Enable Gmail API and Google Sheets API.
   - Download `credentials.json` and place it in the project root.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the project:**
   ```bash
   python main.py
   ```

## File Structure

- `main.py`    : Orchestrates fetching, analyzing, and writing to Sheets
- `email.py`   : Gmail API authentication and fetching emails
- `sheets.py`  : Google Sheets API authentication and writing rows
- `utils.py`   : Helper functions for text analysis
- `requirements.txt` : Python dependencies
- `README.md`  : This file

## Notes
- Place your `credentials.json` file in the project root.
- The first run will prompt for Google authentication and store a token for reuse.

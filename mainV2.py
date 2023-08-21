# cd Summer 2023 Projects - In Use/Goggins/celeb_text.py

import smtplib
import random
from config import SECRET_KEY, quotes, carriers, spreadsheetId
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

#ACTUAL
SPREADSHEET_ID = spreadsheetId
#TEST



# Email details
email = "testerGoggins@gmail.com"
password = SECRET_KEY

chosen_quote = random.choice(quotes)
#chosen_quote = "It's a lot more than mind over matter. It takes relentless self-discipline to schedule suffering into your day, every day."

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    try:

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email, password)


        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        
        data = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A2:E10000").execute().get("values")

        # If range_data is None or empty, there's no data to process
        if not data:
            print("No data found.")
            return
        index = 2
        for row in data:
            timestamp = row[0] #if len(row) > 0 else None
            phone_number = row[1] #if len(row) > 1 else None
            carrier = row[2] #if len(row) > 2 else None
            other_carrier = row[3] #if len(row) > 3 else None
            if len(row) > 4 and len(row[4]) > 0:
                    new_boolean = row[4]
            else:
                new_boolean = None

            print(f"#{index-1}: {timestamp}, {phone_number}, {carrier}, {other_carrier}, {new_boolean}")       

            
            if carrier != "Other":
                if new_boolean == None:
                    carrier_gateway = carriers[str(carrier)]
                    server.sendmail(email, f"{phone_number}@{carrier_gateway}", "Thanks for signing up to the Fake David Goggins Motivational Text Service. Change contact name to Goggins for more motivational impact!")
                    server.sendmail(email, f"{phone_number}@{carrier_gateway}", "To opt-out, reply STOP to any message you receive. Data rates may apply. Expect your first motivational text tomorrow.")
                else:
                    carrier_gateway = carriers[str(carrier)]
                    server.sendmail(email, f"{phone_number}@{carrier_gateway}", chosen_quote)
                #print(f"{timestamp}, {phone_number}, {carrier}, {other_carrier}, {new_boolean}")
             
            if new_boolean == None:
                sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!E{index}",
                                       valueInputOption="USER_ENTERED", body={"values": [[f"FALSE"]]}).execute()
                #print(f"#2: {timestamp}, {phone_number}, {carrier}, {other_carrier}, {new_boolean}\n")
            index+=1
        server.close()
        print("Successful message sent: " + chosen_quote)       

    except HttpError as error:
        print(error)

if __name__ == "__main__":
    main()

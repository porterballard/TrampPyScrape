# # using google sheets api, this code works
# # Install dependencies


# # === IMPORTS ===

# # import time
# # import schedule
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import resend
# # from google.colab import drive

# # drive.mount('/content/drive')

# json_key_path = './creds.json'

# # Upload creds.json once per session
# #uploaded = files.upload()

# import os
# print(os.listdir())




# # === REPLACE WITH YOUR RESEND API KEY ===
# resend.api_key = "re_Au53r3uo_MwCuMDJbKnoecRwNmHkv8EEd"

# # === GOOGLE SHEETS AUTH ===
# scope = ["https://spreadsheets.google.com/feeds",
#          "https://www.googleapis.com/auth/spreadsheets",
#          "https://www.googleapis.com/auth/drive.file",
#          "https://www.googleapis.com/auth/drive"]

# creds = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)

# client = gspread.authorize(creds)

# # Open the sheet
# sheet = client.open_by_key("13b11RItTICI0Rsmwi8A3OgP9e8WL8zgWkreI6dmXoaw").sheet1

# # === MAIN FUNCTION ===
# def scrape_store_and_email():
#     urls = ['https://airbornedraper.com/hours-and-pricing/#6below',
#             'https://airbornelindon.com/hours-and-pricing/']

#     locations_data = {}

#     for url in urls:
#         try:
#             request = requests.get(url)
#             soup = BeautifulSoup(request.content, 'html.parser')
#             prices = [span.text.strip() for span in soup.find_all('span', class_='et_pb_sum')]

#             domain = url.split("//")[1].split(".")[0]
#             location = domain.replace("airborne", "").capitalize()
#             locations_data[location] = prices
#         except Exception as e:
#             print(f"Failed to scrape {url}: {e}")

#     # Get timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Add a row to Google Sheets (feel free to change this format!)
#     for location, prices in locations_data.items():
#         row = [timestamp, location] + prices[:6]  # store up to 6 prices
#         sheet.append_row(row)

#     # === Build the email HTML ===
#     sheet_link = "https://docs.google.com/spreadsheets/d/13b11RItTICI0Rsmwi8A3OgP9e8WL8zgWkreI6dmXoaw/edit?usp=sharing"

#     email_content = """
#     <!DOCTYPE html>
#     <html>
#     <head>
#     <style>
#       body {
#         font-family: 'Arial', sans-serif;
#         background-color: #f7f7f7;
#         padding: 20px;
#         color: #333;
#       }
#       .container {
#         background-color: #fff;
#         padding: 20px;
#         border-radius: 12px;
#         max-width: 600px;
#         margin: auto;
#         box-shadow: 0 0 20px rgba(0,0,0,0.1);
#       }
#       h1 {
#         color: #0b5394;
#         text-align: center;
#       }
#       .location {
#         margin-bottom: 30px;
#       }
#       .section-title {
#         font-weight: bold;
#         margin-top: 10px;
#       }
#       .price {
#         margin-left: 10px;
#       }
#       .footer {
#         margin-top: 30px;
#         font-size: 14px;
#         text-align: center;
#       }
#     </style>
#     </head>
#     <body>
#     <div class="container">
#     <h1>Airborne Daily Price Update</h1>
#     """

#     for location, prices in locations_data.items():
#         email_content += f"<div class='location'><h2>{location}</h2>"
#         if len(prices) >= 6:
#             email_content += f"""
#                 <div class="section-title">5 & Up Prices</div>
#                 <div class="price">Weekday 90 Minutes: {prices[0]}</div>
#                 <div class="price">Weekday All Day: {prices[1]}</div>
#                 <div class="price">Weekend 90 Minutes: {prices[2]}</div>
#                 <div class="price">Weekend All Day: {prices[3]}</div>
#                 <div class="section-title">Ages 0–2 All Day</div>
#                 <div class="price">All Day: {prices[4]}</div>
#                 <div class="section-title">Ages 3–4 All Day</div>
#                 <div class="price">All Day: {prices[5]}</div>
#             """
#         else:
#             email_content += "<p>⚠️ Not enough price data found.</p>"
#         email_content += "</div>"

#     email_content += f"""
#         <div class='footer'>
#         📊 View full data: <a href="{sheet_link}">{sheet_link}</a><br/>
#         Sent at: {timestamp}
#         </div>
#     </div>
#     </body>
#     </html>
#     """

#     # === Send the email via Resend ===
#     resend.Emails.send({
#         "from": "onboarding@resend.dev",
#         "to": ["jeff@ninjakidzparks.com"],  # Add more recipients if needed
#         "subject": "Daily Airborne Pricing Update",
#         "html": email_content
#     })

# # === RUN ONCE IMMEDIATELY ===
# scrape_store_and_email()

# # === SCHEDULE TO RUN DAILY AT 9AM ===
# # schedule.every().day.at("21:08").do(scrape_store_and_email)

# # while True:
# #     schedule.run_pending()
# #     time.sleep(60)

import json
import os


def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    # IF YOU WANT TO CHANGE YOUR KNOWLEDGE DOC
    # UPLOAD A NEW ONE IN THE LEFT HAND PANEL
    # THEN REPLACE "knowledge.docx" BELOW WITH YOUR FILE NAME!
    file = client.files.create(file=open("HopeAIKnowledge.docx", "rb"),
                               purpose='assistants')

    # IF YOU WANT TO CHANGE YOUR INSTRUCTIONS
    # MODIFIY THEM BELOW!
    assistant = client.beta.assistants.create(instructions="""
            The assistant has been programmed to help people who are interested to learn Artificial Intelligence and Data Science in Tamil.

                          A document has been provided with information on the complete Data Science Program that should be used for all queries related to the Course.you should start a  question with to provide their  Name and Phone number to clarify their doubts furthur.  if someone refused to give phone number and name, then reason of asking name and contact number. The reason is if some of the doubts are not clarified by AI chatbot, then Hope AI team will clarify the same for that we need  name and contact number.If anyone asks Hope AI Contact number , then give "+91-6374442932"

            If anyone asks about course fee ask them to watch webinar in which we have covered about the fees. 
            If the user asks questions not related to what is included in the document, the assistant should say that they are not able to answer those questions. The user is chatting to the assistant on Website chatbot, so the responses should be kept brief and concise, sending a dense message suitable for instant messaging via Instagram DMs. Long lists and outputs should be avoided in favour of brief responses with minimal spacing. Also, markdown formatting should not be used. The response should be plain text and suitable for Instagram DMs.

                          Additionally, when the user is wanting to joining the course or has a questions about the program that is not included in the document provided the assistant can ask for the user's lead information so that the Hope AI team can get in touch to help them with their decision. To capture the lead, the assistant needs to ask for their full name and phone number including country code, then analyse the entire conversation to extract the questions asked by the user which will be submitted as lead data also. This should be focussed around concerns and queries they had which the Hope AI team can address on a call, do not mention this question collection step in your responses to the user. To add this to the company CRM, the assistant can call the create_lead function. Collected phone number and name should be returned in the form dictionary.

                          The assistant has been programmed to never mention the knowledge "document" used for answers in any responses. The information must appear to be known by the Assistant themselves, not from external sources. And also  always ask  user to attend our free webinar  which helps them to make decisions to opt this course. Webinar link "https://www.hopelearning.net/webinar105/?utm_source=waichat". 
""",
                                              model="gpt-3.5-turbo-1106",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id


from openai import OpenAI

#response = messages.data[0].content[0]['text']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=OPENAI_API_KEY)


def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):

  response = client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=temperature,
      max_tokens=max_tokens,
  )
  return response.choices[0].message.content


def addLeadToGoogleSheet(dictionary):

  import gspread
  from oauth2client.service_account import ServiceAccountCredentials

  # Define the scope
  scope = ['https://www.googleapis.com/auth/spreadsheets']

  # Add credentials to the account
  creds = ServiceAccountCredentials.from_json_keyfile_name(
      'websiteleadchatgptapi-6de1d5cf867c.json', scope)

  # Authorize the client
  client = gspread.authorize(creds)

  sheet_id = '10GFzMY23X21WsktBuDaoKFX5s9Tr7RhOCxqJmv0wQU8'

  # Authorize the client
  #client = gspread.oauth()

  # Open the spreadsheet using its ID
  spreadsheet = client.open_by_key(sheet_id)

  # Open the spreadsheet by its title
  #spreadsheet = client.open('websiteleaddemo')

  # Select the worksheet where you want to add data (by default, it's the first worksheet - index 0)
  worksheet = spreadsheet.get_worksheet(0)  # Change the index if needed

  # Sample dictionary data
  #data = {"Name": "John Doe", "Age": 30, "Location": "New York"}

  # Convert dictionary keys and values into lists for writing to the sheet
  #keys = list(dictionary.keys())
  values = list(dictionary.values())

  # Append the data to the worksheet
  #worksheet.append_row(keys)
  worksheet.append_row(values)

  print("Data added successfully!")
  msg = "added"
  return msg


def addTranscripitToGoogleSheet(dictionary):

  import gspread
  from oauth2client.service_account import ServiceAccountCredentials

  # Define the scope
  scope = ['https://www.googleapis.com/auth/spreadsheets']

  # Add credentials to the account
  creds = ServiceAccountCredentials.from_json_keyfile_name(
      'websiteleadchatgptapi-6de1d5cf867c.json', scope)

  # Authorize the client
  client = gspread.authorize(creds)

  sheet_id = '1PO5YkaoD8KoKjdM8tkHoUvMo6O7N0eSvtUrztSe3HI8'

  # Authorize the client
  #client = gspread.oauth()

  # Open the spreadsheet using its ID
  spreadsheet = client.open_by_key(sheet_id)

  # Open the spreadsheet by its title
  #spreadsheet = client.open('websiteleaddemo')

  # Select the worksheet where you want to add data (by default, it's the first worksheet - index 0)
  worksheet = spreadsheet.get_worksheet(0)  # Change the index if needed

  # Sample dictionary data
  #data = {"Name": "John Doe", "Age": 30, "Location": "New York"}

  # Convert dictionary keys and values into lists for writing to the sheet
  #keys = list(dictionary.keys())
  values = list(dictionary.values())

  # Append the data to the worksheet
  #worksheet.append_row(keys)
  worksheet.append_row(values)

  print("Transcript added successfully!")
  msg = "Transcript added"
  return msg

import os
from time import sleep
from packaging import version
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import functions
import openai

# Check OpenAI version is correct
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
print(f"OpenAI version: {openai.__version__}")
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if current_version < required_version:
  raise ValueError(f"Error: OpenAI version {openai.__version__}"
                   " is less than the required version 1.1.1")
else:
  print("OpenAI version is compatible.")

# Start Flask app
app = Flask(__name__)

# Init client
#client = OpenAI(
#api_key=OPENAI_API_KEY
#)  # should use env variable OPENAI_API_KEY in secrets (bottom left corner)
#from openai import OpenAI

client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v2"})
# Create new assistant or load existing
assistant_id = functions.create_assistant(client)


# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
  print("Starting a new conversation...")  # Debugging line
  thread = client.beta.threads.create()
  print(f"New thread created with ID: {thread.id}")  # Debugging line
  return jsonify({"thread_id": thread.id})


# Generate response
@app.route('/chat', methods=['POST'])
def chat():
  data = request.json
  thread_id = data.get('thread_id')
  user_input = data.get('message', '')

  if not thread_id:
    print("Error: Missing thread_id")  # Debugging line
    return jsonify({"error": "Missing thread_id"}), 400

  print(f"Received message: {user_input} for thread ID: {thread_id}"
        )  # Debugging line

  # Add the user's message to the thread
  client.beta.threads.messages.create(thread_id=thread_id,
                                      role="user",
                                      content=user_input)

  # Run the Assistant
  run = client.beta.threads.runs.create(thread_id=thread_id,
                                        assistant_id=assistant_id)

  # Check if the Run requires action (function call)
  while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                   run_id=run.id)

    print(f"Run status: {run_status.status}")
    if run_status.status == 'completed':
      break

    sleep(1)  # Wait for a second before checking again

    # Retrieve and return the latest message from the assistant
  messages = client.beta.threads.messages.list(thread_id=thread_id)
  response = messages.data[0].content[0].text.value
  transcript = {
      "user_input": user_input,
      "response": response,
      "tread_id": thread_id
  }
  functions.addTranscripitToGoogleSheet(transcript)
  print(f"Assistant response: {response}")  # Debugging line
  messagess = [{
      "role":
      "system",
      "content":
      "you are a assitant you checks the user_input response contains Name and phone number if it is  convert into the dictionary format you should return only in json format Name: RR, Phone: +918883916171, if user_input doest contain name and phone number then return only in Single character 'N'"
  }, {
      "role": "user",
      "content": user_input
  }]
  lead = functions.get_completion_from_messages(messagess)
  print("Lead msg", lead)

  if lead.find('{') != -1:
    import json
    dict_lead = json.loads(lead)
    print("Lead Type", type(dict_lead))

    if type(dict_lead) is dict:
      msg = functions.addLeadToGoogleSheet(dict_lead)
      print(msg)
    else:
      print("This is not dictionary")
  else:
    print("No Lead captured")

  #if
  return jsonify({"response": response})


# Run server
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

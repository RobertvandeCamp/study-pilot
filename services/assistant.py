from openai import OpenAI
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()
openAIApiKey = os.getenv('OPENAI_API_KEY')
print(f'OPENAI_API_KEY: {openAIApiKey}')

client = OpenAI(api_key=openAIApiKey)
starting_assistant = ""
starting_thread = ""


# Step 1: Create (or retrieve) an Assistant
#An Assistant represents an entity that can be configured to respond to a user's messages using several parameters likemodel, instructions, and tools.
def create_assistant():
    if starting_assistant == "":
        my_assistant = client.beta.assistants.create(
            instructions="You are a helpful assistant.",
            name="MyQuickstartAssistant",
            model="gpt-4o-mini",
        )
    else:
        #Retrieve the assistant by id
        my_assistant = client.beta.assistants.retrieve(starting_assistant)

    return my_assistant

#Step 2: Create a Thread
#A Thread represents a conversation between a user and one or many Assistants. 
# You can create a Thread when a user (or your AI application) starts a conversation with your Assistant.
def create_thread():
    if starting_thread == "":
        thread = client.beta.threads.create()
    else:
        thread = client.beta.threads.retrieve(starting_thread)

    return thread


# Step 3: Add a Message to the Thread
# The contents of the messages your users or applications create are added as Message objects to the Thread. 
# Messages can contain both text and files. 
# There is a limit of 100,000 Messages per Thread and we smartly truncate any context that does not fit into the model's context window.
def send_message(thread_id, message):
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_message


# Step 4: Create a Run
# Once all the user Messages have been added to the Thread, you can Run the Thread with any Assistant. 
# Creating a Run uses the model and tools associated with the Assistant to generate a response. 
# These responses are added to the Thread as assistant Messages.
def run_assistant(thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    return run


def get_newest_message(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data[0]


def get_run_status(thread_id, run_id):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run.status


def main():
    my_assistant = create_assistant()
    my_thread = create_thread()

    while True:
        user_message = input("Enter your message: ")
        if user_message.lower() == "exit":
            break

        send_message(my_thread.id, user_message)
        run = run_assistant(my_thread.id, my_assistant.id)
        while run.status != "completed":
            run.status = get_run_status(my_thread.id, run.id)
            sleep(1)
            print("⏳", end="\r", flush=True)

        sleep(0.5)
        response = get_newest_message(my_thread.id)
        print("Response:", response.content[0].text.value)

if __name__ == "__main__":
    main()

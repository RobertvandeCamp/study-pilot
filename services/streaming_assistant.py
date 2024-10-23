from typing_extensions import override
from openai import AssistantEventHandler
from openai import OpenAI
import time
import random
from dotenv import load_dotenv
import os

load_dotenv()
openAIApiKey = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openAIApiKey)

snape = client.beta.assistants.create(
    name="Snape",
    instructions="You are Professor Snape, a grumpy teacher. Provide feedback on translations and two example sentences using the word. Be critical and slightly irritated in your tone. Prefix example sentences with [USAGE].",
    model="gpt-4-1106-preview"
)

thread = client.beta.threads.create()  

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    pass
      
  @override
  def on_text_delta(self, delta, snapshot):
    pass
    
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
 
def start_conversation():
    def generate():
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=snape.id,
            event_handler=EventHandler(),
        ) as stream:
            for delta in stream:
                yield f"data: {delta.value}\n\n"
    return generate

def send_message(message):
    print(f'Message received [{message}]')
    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=message,
    )
    return thread_message

if __name__ == "__main__":
  send_message("The translation of the word 'Building' to Dutch is 'Gebouw'.")
  start_conversation(snape, thread)

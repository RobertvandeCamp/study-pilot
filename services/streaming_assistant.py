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

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
    
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
 
def start_conversation(assistant, thread):
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

def send_message(thread_id, message):
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_message

if __name__ == "__main__":
  thread = client.beta.threads.create()    
  send_message(thread.id, "The translation of the word 'Building' to Dutch is 'Gebouw'.")
  start_conversation(snape, thread)

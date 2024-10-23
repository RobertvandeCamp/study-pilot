from openai import OpenAI
import time
import random
from dotenv import load_dotenv
import os

load_dotenv()
openAIApiKey = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openAIApiKey)

# Create assistants
student = client.beta.assistants.create(
    name="Alex",
    instructions="You are a student named Alex. Your native language is Dutch. Provide translations for English words to Dutch.",
    model="gpt-4-1106-preview"
)

snape = client.beta.assistants.create(
    name="Snape",
    instructions="You are Professor Snape, a grumpy teacher. Provide feedback on translations and two example sentences using the word. Be critical and slightly irritated in your tone. Prefix example sentences with [USAGE].",
    model="gpt-4-1106-preview"
)

hagrid = client.beta.assistants.create(
    name="Hagrid",
    instructions="You are Hagrid, a friendly and funny teacher. Provide feedback on translations and two example sentences using the word. Be encouraging and lighthearted. Prefix example sentences with [USAGE].",
    model="gpt-4-1106-preview"
)

# Function to run an assistant and get its response
def run_assistant(assistant, thread, user_message=None):
    if user_message:
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    
    while run.status != "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

# Function to conduct a conversation
def conduct_conversation(word):
    thread = client.beta.threads.create()
    
    # Student translation
    student_input = f"Translate the word '{word}' to Dutch"
    student_response = run_assistant(student, thread, student_input)
    print(f"Alex: {student_response}")
    
    # First teacher response (randomly select Snape or Hagrid)
    first_teacher = random.choice([snape, hagrid])
    second_teacher = hagrid if first_teacher == snape else snape
    
    teacher_prompt = f"Provide feedback on the translation of '{word}' to Dutch as '{student_response}'. Then provide two example sentences using the word '{word}'. Remember to prefix your example sentences with [USAGE]."
    first_teacher_response = run_assistant(first_teacher, thread, teacher_prompt)
    print(f"{first_teacher.name}: {first_teacher_response}")
    
    # Second teacher response
    second_teacher_prompt = f"Respond to {first_teacher.name}'s feedback and sentences. Also comment on the student's translation success or failure."
    second_teacher_response = run_assistant(second_teacher, thread, second_teacher_prompt)
    print(f"{second_teacher.name}: {second_teacher_response}")
    
    # Optional: First teacher's final comment
    final_comment_prompt = f"Provide a brief final comment to {second_teacher.name}'s response."
    final_comment = run_assistant(first_teacher, thread, final_comment_prompt)
    print(f"{first_teacher.name}: {final_comment}")

# Example usage
if __name__ == "__main__":
    words = ["Building", "Candy", "Tree"]
    for word in words:
        print(f"\nTranslating the word: {word}")
        conduct_conversation(word)
        print("\n" + "="*50 + "\n")
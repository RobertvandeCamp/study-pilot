import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the assistant personas
teacher_1_persona = "You are a slightly grumpy language teacher who responds concisely and sometimes sarcastically."
teacher_2_persona = "You are a very funny language teacher who makes jokes and is playful in your responses."

def create_conversation_response(prompt, persona):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message

def run_conversation_cycle(word_translation):
    # Step 1: Teacher 1 provides sentences using the translated word
    teacher_1_prompt = f"The student provided the translation: '{word_translation}'. Can you provide some example sentences using this word in the target language?"
    teacher_1_response = create_conversation_response(teacher_1_prompt, teacher_1_persona)
    print("Teacher 1 (Grumpy):", teacher_1_response)

    # Step 2: Teacher 2 reacts to Teacher 1's response
    teacher_2_prompt = f"Teacher 1 said: '{teacher_1_response}'. How would you respond to this in a funny and playful manner?"
    teacher_2_response = create_conversation_response(teacher_2_prompt, teacher_2_persona)
    print("Teacher 2 (Funny):", teacher_2_response)

# Example usage
if __name__ == "__main__":
    student_translation = "apple" # Example word from the student
    run_conversation_cycle(student_translation)

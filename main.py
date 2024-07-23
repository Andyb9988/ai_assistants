import openai
from dotenv import find_dotenv, load_dotenv

load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

#===

personal_trainer_assis = client.beta.assistants.create(
    name="Personal Trainer",
    instructions = """You are the best personal trainer and nutritionist and have trained multiple high-caliber athletes and movie stars.""",
    model=model
)

print(personal_trainer_assis.id)
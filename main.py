import openai
import logging
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

api_key = os.getenv("OPENAI_ASSISTANT_API_KEY")

client = openai.OpenAI(api_key=api_key)
model = "gpt-3.5-turbo-16k"

# personal_trainer_assis = client.beta.assistants.create(
#     name="Personal Trainer",
#     instructions = """You are the best personal trainer and nutritionist and have trained multiple high-caliber athletes and movie stars.""",
#     model=model
# )

# #=== Thread ====
# threads = client.beta.threads.create(
# messages = [
#     {"role":"user",
#      "content": "How do I get started working out to lose fat and build muscle?"}
# ])

# == Hardcode ids ===
asistant_id = "asst_xa6SMXYRMqPTGy79yzeqxRt2"
thread_id = "thread_c1klEIwPwMdaZZknHC5jLJfx"


# == Create a message ===
message = "How much water should I drink a day?"
message = client.beta.threads.messages.create(
    thread_id=thread_id, role="user", content=message
)

# === Run our Assistant ===
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=asistant_id,
    instructions="Please address the user as James Bond",
)

logging.info(f"Started run with ID: {run.id}")


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                logging.info(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


### Run ###
def main():
    wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)


if __name__ == "__main__":
    main()

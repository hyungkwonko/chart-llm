from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")

client = OpenAI()

for file in client.files.list():
    # client.files.delete(file.id)
    print(file)

for model in client.models.list():
    # client.models.delete(model.id)
    print(model)

for model in client.fine_tuning.jobs.list():
    print(model)
    print("==")

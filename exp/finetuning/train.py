import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")

MODELS = ["babbage-002", "davinci-002", "gpt-3.5-turbo-0613"]
NAMES = ["bm", "bmllmp", "bmllmpllmp2", "llmp", "llmp2", "half"]


if __name__ == "__main__":
    client = OpenAI()

    for name in NAMES:
        client = OpenAI()

        train_file = client.files.create(
            file=open(f"exp/finetuning/data/{name}.jsonl", "rb"), purpose="fine-tune"
        )

        print("Uploading Datasets (Sleep for 10 seconds)")

        time.sleep(10)

        response = client.fine_tuning.jobs.create(
            training_file=train_file.id,
            # validation_file=val_file.id,
            model=MODELS[0],
        )

        while True:
            fine_tuning_status = client.fine_tuning.jobs.retrieve(response.id)
            print(f"Fine-tuning job status:\n {fine_tuning_status}")

            if fine_tuning_status.status in ["succeeded", "failed"]:
                break

            time.sleep(60)

        print("Fine-tuning finished.")

        with open(f"exp/finetuning/data/model_{name}.txt", "w") as fp:
            fp.write(fine_tuning_status.fine_tuned_model)

        content = client.files.retrieve_content(fine_tuning_status.result_files[0])
        with open(f"exp/finetuning/data/val_{name}.csv", "w") as file:
            file.write(content)

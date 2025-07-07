from openai import OpenAI, OpenAIError, BadRequestError
import requests
from PIL import Image
import json
import os

# My own libraries
from DB.User import User
from DB.SQLite_Manager import SQLite_Manager

# This function is guaranteed to not throw any errors
def generate(prompt: str, size1: int, size2: int) -> str:
  script_dir = os.path.dirname(__file__)
  secret_path = os.path.abspath(os.path.join(script_dir, "..", "secrets.json"))
  with open(secret_path, "r") as f:
    secrets = json.load(f)
  api_key = secrets.get("OpenAI_API_KEY")

  client = OpenAI(api_key=api_key)

  url = generate_helper(client, prompt, size1, size2)
  # print(url)
  return url

# Currently just generate 1 file.
# TODO: check success status
def generate_helper(client, prompt: str, size1: int, size2: int) -> str:
  sizeString = str(size1) + "x" + str(size2)

  try:
      res = client.images.generate(
          prompt=prompt,  # Ex:  "What you imagine I look like.
          n=1,
          size=sizeString       # Ex:  "256x256"
      )
      return res.data[0].url
      # DEBUG
      return "https://oaidalleapiprodscus.blob.core.windows.net/private/org-ZsReTGnTbHGmTLgyLr6gc9yl/user-sOm1PaJtjhDzaqjAwhuVQZmZ/img-B19ZdHwRjn8OYT2j3QqjQnFF.png?st=2025-06-10T02%3A56%3A21Z&se=2025-06-10T04%3A56%3A21Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=475fd488-6c59-44a5-9aa9-31c4db451bea&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-06-10T03%3A56%3A21Z&ske=2025-06-11T03%3A56%3A21Z&sks=b&skv=2024-08-04&sig=uZ0THJvFNZtoGPME7FHzeTE1FjCIQ9DPeL3csEgtJVk%3D"

  except OpenAIError as e:
      print(f"[OpenAIError] {e}")
      return None

  except Exception as e:
      print(f"[Unexpected Error] {e}")
      return None
import json
import random


class Sentence:
    def __init__(self, id, text):
        self.id = id
        self.text = text


class SentenceGenerator:
    def generate_sentence(self):
        with open("paragraphs.json", "r") as file:
            data = file.read().replace("\n", "")
            paragraphs = json.loads(data)
            random_id = random.randint(0, len(paragraphs) - 1)
            paragraph = paragraphs[random_id]
            return Sentence(int(paragraph["id"]), str(paragraph["text"]))

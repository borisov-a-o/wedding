# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
response = requests.get("https://weddingpost.ru/749611/1066730")

print(response.text)

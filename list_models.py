import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCA9y-RC2g6tEnATjA5iHQuF-vHjzqrsQs")

print("Listing available models...")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

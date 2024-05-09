import pygame
import speech_recognition as sr
import webbrowser  # type: ignore
from gtts import gTTS
from io import BytesIO  # type: ignore
from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate


def speak(text):
  audio = BytesIO()
  tts = gTTS(text=text, lang='en')
  
  tts.write_to_fp(audio)
  audio.seek(0)
  
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.load(audio)
  pygame.mixer.music.play()
  
  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
    
    
def recognize():
  voice = sr.Recognizer()
  with sr.Microphone() as mic:
    voice.adjust_for_ambient_noise(mic)
    audio = voice.listen(mic)
    try:
      print("Recognizing...")
      user = voice.recognize_google(audio, language="en-in")
      print(f"User: {user}")
      return user
    
    except sr.UnknownValueError:
      return "I couldn't understand"
    
conversation = ""
def chat(query):
  #global conversation
  #conversation += f"User: {query}\n MusicGuru: "
    
  config = {'temperature': 0.6, 'threads': 6, 'max_new_tokens': 300}
  llm = CTransformers(model= "model\llama-2-7b-chat.ggmlv3.q4_0.bin", model_type = 'llama', config = config)

  template = """
  You are MusicGuru,a personal music assisstant and an expert in anything related to music. 
  Give precise and short answers, not exceeding 100 words. Respond professionally, so don't include any
  special characters such as '*,#' or emojis and emoticons in your responses. Now, answer {query}.
  """

  prompt = PromptTemplate(template=template, input_variables=['query'])
  

  try:
    response = llm.invoke(prompt.format(query = query))
    speak(response)
    #conversation += f"{response}\n"
    print(response)
    return response
  except Exception as e:
    speak("I couldn't understand")
    return "Please speak again"
    



if __name__ == '__main__':
  speak("I am Music Guru AI. How can I help you today?")
  while True:
    print("Listening...")
    query = recognize().lower()
    
    sites = [["youtube music", "https://music.youtube.com"], ["spotify", "https://spotify.com"], ["apple music", "https://music.apple.com"], 
             ["amazon music", "https://music.amazon.in"], ["gaana", "https://gaana.com"], ["jio music", "https://jiosaavn.com"]]
    for site in sites:  
      if f"Open {site[0]}".lower() in query:
        speak(f"Opening {site[0]}")
        webbrowser.open(site[1])
    
    if "bye" in query or "quit" in query:
      speak("Goodbye!")
      exit()
          
    else:
      print("Chatting...")
      chat(query)



    
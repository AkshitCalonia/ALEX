from flask import Flask, render_template, request, jsonify
import pyttsx3
import speech_recognition as sr
import threading  # Add this line to import the threading module
import subprocess  # Add this line to import subprocess module



app = Flask(__name__)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        r.energy_threshold = 440
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except Exception as e:
        print("Say that again please...")
        return "None"

listening_thread = None  # Define listening_thread globally

@app.route('/')
def index():
    return render_template('index.html')



character = ""
@app.route('/set_character', methods=['POST'])
def set_character():
    global character
    character = request.json['character']
    # Optionally, you can store the character name in a global variable or session for later use
    return jsonify({'status': 'success'})



def takecommand_and_process():
    global mic_result
    mic_result = takecommand()
    # Assuming you have a way to determine the character's name, let's say it's stored in a variable called 'character'
    character_ = character  # Implement this function to determine the character's name
    # Call chatgpt_character.py passing the character's name and mic_result


    subprocess.run(['python', 'chatgpt_character.py', character_, mic_result])


@app.route('/start_listening', methods=['POST'])
def start_listening():
    global listening_thread
    listening_thread = threading.Thread(target=takecommand_and_process)
    listening_thread.start()
    return jsonify({'status': 'success'})


@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    global listening_thread
    listening_thread.join()  # Wait for the thread to complete
    # After the thread completes, mic_result would have been processed by chatgpt_character.py
    # Now you can send mic_result to your front end or store it for later use
    return jsonify({'status': 'success', 'mic_result': mic_result})


if __name__ == '__main__':
    app.run(debug=True)


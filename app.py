import base64
import io
import threading
from flask import Flask, render_template, request, session, redirect, jsonify, url_for
import g4f
import pyttsx3
from io import BytesIO

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use your DB URI
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

 # Set a secret key for session management

system_prompt = (
    "You are an HR interviewer conducting a job interview. "
    "Your role is to assess the candidate's experience, problem-solving skills, stress management, motivation, cultural fit, and career goals. "
    "Ask questions related to these areas and provide feedback based on the responses, highlighting strengths and areas for improvement. "
    "Ensure the conversation flows logically and stays focused on interview topics. "
    "If the candidate deviates from the topic or asks for personal, unrelated matters (like food, casual conversations, or non-interview-related requests), "
    "politely redirect them back to interview-related discussions. "
    "Maintain a professional and friendly tone throughout the interview. "
    "Always respond in English. "
    "Do not generate any non-interview related content or any language other than English. "
    "After every 5 interactions, provide feedback to the candidate based on their performance, "
    "highlighting strengths and areas for improvement. Reset the conversation count after the feedback is provided. "
    "If the candidate requests feedback at any point, offer constructive feedback based on the conversation history. "
    "Only generate responses related to the interview process, and always do so in English."
)

import cv2
from flask import Response

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoCaptureThread(threading.Thread):
    def __init__(self, capture_device):
        threading.Thread.__init__(self)
        self.capture_device = capture_device
        self.frame = None
        self.lock = threading.Lock()

    def run(self):
        while True:
            ret, frame = self.capture_device.read()
            if ret:
                with self.lock:
                    self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame

# Function to generate frames for video streaming
def gen_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow for faster capture (Windows)
    cap.set(3, 320)  # Set width to 320 pixels (adjustable)
    cap.set(4, 240)  # Set height to 240 pixels (adjustable)

    video_thread = VideoCaptureThread(cap)
    video_thread.start()

    while True:
        frame = video_thread.get_frame()
        if frame is None:
            continue

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            # No faces detected, draw a red frame around the screen
            height, width = frame.shape[:2]
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 5)  # Red frame
        else:
            # Draw rectangle around detected faces (blue)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)  # Blue frame

        # Stream the video frame
        frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')


import pyttsx3
import pyaudio

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Set properties for the speech engine
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to convert text to speech and return the audio as a base64-encoded string
def text_to_speech(text):
    """Converts text to speech and returns audio as base64-encoded string."""
    audio_stream = io.BytesIO()
    engine.save_to_file(text, audio_stream)
    audio_stream.seek(0)  # Reset the pointer to the start of the stream
    audio_base64 = base64.b64encode(audio_stream.read()).decode('utf-8')

    # Play the audio using PyAudio
    play_audio(audio_stream)

    return audio_base64

def play_audio(audio_stream):
    """Play the generated audio using pyaudio."""
    audio_stream.seek(0)  # Reset the pointer to the start
    chunk_size = 1024
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    output=True)

    # Read the audio data in chunks and play it
    data = audio_stream.read(chunk_size)
    while data:
        stream.write(data)
        data = audio_stream.read(chunk_size)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()


# Route for the face detection live feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Function to generate responses using GPT-4
def generate_response(user_input, messages, model="gpt-4"):
    """Generate a response using GPT-4 with controlled behavior."""
    try:
        response = g4f.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.6,
            top_p=0.9
        )
        if isinstance(response, str) and response.strip() != "":
            return response
        else:
            return "Chatbot: Received an empty or invalid response from the API."
    except Exception as e:
        return f"Chatbot: Error generating response: {e}"

@app.route('/index')
def landing_page():
    # Reset session on page load to clear chat history
    session.clear()
    return render_template('landing.html')

# Route to render the chat interface
@app.route('/chat1')
def chat_interface():
    print("Navigating to the interview interface")  # Debugging
    if 'conversation_history' not in session:
        session['conversation_history'] = [
            {"role": "system", "content": system_prompt}
        ]
    if 'conversation_count' not in session:
        session['conversation_count'] = 0
    
    return render_template('chat.html', conversation_history=session['conversation_history'])


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')

    
    if 'conversation_history' not in session:
        session['conversation_history'] = [
            {"role": "system", "content": system_prompt}
        ]
    
    if 'conversation_count' not in session:
        session['conversation_count'] = 0
    
    # Handle restart command
    if user_input.lower() == "/restart":
        session['conversation_history'] = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "Interview restarted. Let's begin again."}
        ]
        session['conversation_count'] = 0  # Reset the conversation count
        return render_template('chat.html', conversation_history=session['conversation_history'])

    # Handle exit command
    elif user_input.lower() == "exit":
        session['conversation_history'].append({"role": "user", "content": user_input})
        session['conversation_history'].append({"role": "assistant", "content": "Thank you for your time today. We'll be in touch soon."})
        return render_template('chat.html', conversation_history=session['conversation_history'])

    # Handle feedback request
    elif user_input.lower() == "feedback":
        feedback_prompt = (
            "Based on our conversation, provide constructive feedback on the candidate's performance, "
            "highlighting their strengths and areas for improvement."
        )
        feedback = generate_response(feedback_prompt, session['conversation_history'])
        session['conversation_history'].append({"role": "user", "content": user_input})
        session['conversation_history'].append({"role": "assistant", "content": feedback})

        # Convert feedback to speech and play it
        audio_stream = text_to_speech(feedback)

        return render_template('chat.html', conversation_history=session['conversation_history'], 
                               feedback=feedback, audio_stream=audio_stream)

    # Handle non-interview related inputs (e.g., "I want pizza")
    elif "pizza" in user_input.lower() or "food" in user_input.lower() or "play" in user_input.lower() or "dress" in user_input.lower() or "dance" in user_input.lower()or "sleep" in user_input.lower()or "movie" in user_input.lower()or "song" in user_input.lower():
        session['conversation_history'].append({"role": "user", "content": user_input})
        session['conversation_history'].append({"role": "assistant", "content": "Let's focus on the interview, please."})
        return render_template('chat.html', conversation_history=session['conversation_history'])
    
    
    session['conversation_history'].append({"role": "user", "content": user_input})
    session['conversation_count'] += 1
    
    if session['conversation_count'] >= 5:
        feedback_prompt = (
            "Based on the last 5 interactions, provide feedback on the candidate's performance, "
            "highlighting their strengths and areas for improvement."
        )
        feedback = generate_response(feedback_prompt, session['conversation_history'])
        session['conversation_history'].append({"role": "assistant", "content": feedback})
        session['conversation_count'] = 0  

        
        audio_stream = text_to_speech(feedback)
        response = None  
    else:
        response = generate_response(user_input, session['conversation_history'])
        session['conversation_history'].append({"role": "assistant", "content": response})

        
        audio_stream = text_to_speech(response)

    
    return render_template('chat.html', conversation_history=session['conversation_history'], 
                       response=response if session['conversation_count'] < 5 else feedback,
                       audio_stream=audio_stream)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered! Please log in.', 'danger')
            return redirect(url_for('login'))

        # Hash password and save user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Store user information in the session
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')

            
            return render_template('landing.html') 
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)


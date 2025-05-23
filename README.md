# AI-Powered Interview Assistant

An intelligent interview platform that combines computer vision, natural language processing, and speech synthesis to provide an interactive interview experience.

## Features

- **Real-time Face Detection**: Monitors candidate's presence and engagement
- **AI-Powered Interview**: Conducts intelligent interviews with contextual understanding
- **Text-to-Speech**: Provides voice feedback and questions
- **User Authentication**: Secure login and registration system
- **Interactive Chat Interface**: Real-time interview conversation
- **Performance Analytics**: Tracks and analyzes interview responses

## Technologies & Algorithms

### Computer Vision
- **OpenCV (cv2)**: Real-time face detection and video processing
- **Haar Cascade Classifier**: For face detection using pre-trained models
- **Video Streaming**: Efficient frame capture and processing

### Natural Language Processing
- **GPT-4 (via g4f)**: Contextual understanding and response generation
- **Transformers**: Advanced text processing and understanding
- **SentencePiece**: Text tokenization and processing

### Speech Processing
- **pyttsx3**: Text-to-speech conversion
- **PyAudio**: Audio playback and processing
- **Speech Synthesis**: Natural voice generation

### Web Framework
- **Flask**: Web application framework
- **Flask-SQLAlchemy**: Database ORM
- **Werkzeug**: WSGI utilities

## Dependencies

### Core Dependencies
- `flask==3.0.2`: Web framework
- `flask-sqlalchemy==3.1.1`: Database ORM
- `g4f==0.5.2.0`: GPT-4 API integration
- `pyttsx3==2.90`: Text-to-speech
- `opencv-python==4.9.0.80`: Computer vision
- `pyaudio==0.2.14`: Audio processing
- `werkzeug==3.0.1`: WSGI utilities
- `numpy==1.26.4`: Numerical computing

### Supporting Dependencies
- `aiohttp==3.9.3`: Async HTTP requests
- `brotli==1.1.0`: Compression
- `pycryptodome==3.20.0`: Encryption
- `nest-asyncio==1.6.0`: Async operations
- `requests==2.31.0`: HTTP requests
- `comtypes==1.2.0`: Windows COM support
- `pillow==10.2.0`: Image processing
- `python-dotenv==1.0.1`: Environment management
- `pydantic==2.6.1`: Data validation

### AI/ML Dependencies
- `torch==2.2.0`: Deep learning framework
- `transformers==4.37.2`: NLP models
- `sentencepiece==0.2.0`: Text tokenization
- `protobuf==4.25.2`: Protocol buffers

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
project/
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
├── templates/            # HTML templates
│   ├── chat.html         # Chat interface
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── landing.html      # Landing page
│   └── index.html        # Home page
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Image assets
└── instance/           # Database files
```

## Key Algorithms

### Face Detection
- Uses Haar Cascade Classifier for real-time face detection
- Implements frame-by-frame processing for video feed
- Provides visual feedback with bounding boxes

### Interview Processing
- Implements GPT-4 for contextual understanding
- Uses transformers for response generation
- Maintains conversation history for context

### Speech Synthesis
- Implements text-to-speech conversion
- Uses pyttsx3 for voice generation
- Handles audio playback through PyAudio

## Security Features

- Password hashing with PBKDF2
- Session management
- Secure database operations
- Input validation and sanitization

## Performance Considerations

- Asynchronous video processing
- Efficient database queries
- Optimized AI response generation
- Cached speech synthesis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
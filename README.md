# Smart AI Toolkit

This project is a collection of AI-powered tools bundled into a Django web application. It includes features for face recognition in a photo gallery, image generation from text prompts, text-to-speech conversion, and story generation with PDF download.

## Features

- **Photo Gallery with Face Recognition**: Upload images and the application will automatically group them into albums based on the faces recognized in the photos.
- **Image Generation**: Generate images from text prompts using the Pollinations.ai API.
- **Text-to-Speech**: Convert text into speech using the `edge-tts` library.
- **Story Generation**: Generate stories and download them as PDF files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Django
- `face_recognition`
- `edge-tts`
- `pygame`
- `Pillow`
- `requests`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv myvenv
    source myvenv/bin/activate  # On Windows, use `myvenv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You'll need to create a `requirements.txt` file. See the "Creating requirements.txt" section below)*

4.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

### Creating `requirements.txt`

You can generate a `requirements.txt` file by running the following command in your activated virtual environment:

```bash
pip freeze > requirements.txt
```

This will capture all the necessary packages for this project. Based on the code, you'll at least need:

```
Django
Pillow
face-recognition
edge-tts
pygame
requests
```

## Usage

-   Navigate to `http://127.0.0.1:8000/` to access the photo gallery.
-   Navigate to `http://127.0.0.1:8000/image/` to access the image generator.
-   Navigate to `http://127.0.0.1:8000/tts/` to access the text-to-speech tool.
-   Navigate to `http://127.0.0.1:8000/story/` to access the story generator.

## Screenshots

Here are some screenshots of the application:

### Home Page
![Home Page](screenshots/home.png)

### Gallery
![Gallery](screenshots/gallery.png)

### AI Creator
![AI Creator](screenshots/ai_creator.png)

### AI Creator Result
![AI Creator Result](screenshots/ai_creator_result.png)

### Voice Magic
![Voice Magic](screenshots/voice_magic.png)

### Story Weaver
![Story Weaver](screenshots/story_weaver.png) 
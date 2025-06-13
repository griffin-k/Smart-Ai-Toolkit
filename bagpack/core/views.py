import cv2
from django.shortcuts import render
import os
import subprocess
import pygame
from django.conf import settings


# def gallery_view(request):
#     return render(request, 'gallery.html')

# def tts_view(request):
#     return render(request, 'tts.html')

# def story_view(request):
#     return render(request, 'story.html')

# def image_view(request):
#     return render(request, 'image.html')


import os
import shutil
from django.conf import settings
from django.shortcuts import render, redirect
from PIL import Image
import face_recognition

def gallery_view(request):
    gallery_dir = os.path.join(settings.MEDIA_ROOT, 'gallery')
    os.makedirs(gallery_dir, exist_ok=True)

    if request.method == 'POST':
        images = request.FILES.getlist('images')
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
        os.makedirs(temp_dir, exist_ok=True)

        # Save uploaded images temporarily
        for image in images:
            with open(os.path.join(temp_dir, image.name), 'wb+') as dest:
                for chunk in image.chunks():
                    dest.write(chunk)

        # Process each image
        for img_name in os.listdir(temp_dir):
            img_path = os.path.join(temp_dir, img_name)
            image = face_recognition.load_image_file(img_path)
            face_encodings = face_recognition.face_encodings(image)

            if not face_encodings:
                continue  # Skip if no face found

            current_encoding = face_encodings[0]
            matched = False

            # Compare with existing albums
            for folder in os.listdir(gallery_dir):
                folder_path = os.path.join(gallery_dir, folder)
                for known_img in os.listdir(folder_path):
                    known_img_path = os.path.join(folder_path, known_img)
                    known_image = face_recognition.load_image_file(known_img_path)
                    known_encodings = face_recognition.face_encodings(known_image)
                    if not known_encodings:
                        continue
                    result = face_recognition.compare_faces([known_encodings[0]], current_encoding)
                    if result[0]:
                        shutil.move(img_path, os.path.join(folder_path, img_name))
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                new_folder = os.path.join(gallery_dir, f'person_{len(os.listdir(gallery_dir))+1}')
                os.makedirs(new_folder, exist_ok=True)
                shutil.move(img_path, os.path.join(new_folder, img_name))

        shutil.rmtree(temp_dir)
        return redirect('gallery')

    # Show albums
    albums = []
    media_url = settings.MEDIA_URL + 'gallery/'

    for folder in os.listdir(gallery_dir):
        folder_path = os.path.join(gallery_dir, folder)
        if os.path.isdir(folder_path):
            images = os.listdir(folder_path)
            if images:
                thumbnail = media_url + folder + '/' + images[0]
                albums.append({'name': folder, 'thumbnail': thumbnail})

    return render(request, 'gallery.html', {'albums': albums})



def group_faces(temp_path, base_path):
    known_faces = []
    known_names = []

    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if folder == "temp" or not os.path.isdir(folder_path):
            continue
        for file in os.listdir(folder_path):
            image_path = os.path.join(folder_path, file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_faces.append(encodings[0])
                known_names.append(folder)

    for file in os.listdir(temp_path):
        image_path = os.path.join(temp_path, file)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            match = face_recognition.compare_faces(known_faces, encodings[0], tolerance=0.5)
            if True in match:
                index = match.index(True)
                folder_name = known_names[index]
            else:
                folder_name = f"Person_{len(known_faces) + 1}"
                known_faces.append(encodings[0])
                known_names.append(folder_name)
        else:
            folder_name = "Unknown"

        dest_folder = os.path.join(base_path, folder_name)
        os.makedirs(dest_folder, exist_ok=True)
        cv2.imwrite(os.path.join(dest_folder, file), cv2.imread(image_path))
        os.remove(image_path)  # Clean up temp image






from django.http import Http404

def album_detail(request, album_name):
    album_path = os.path.join(settings.MEDIA_ROOT, 'gallery', album_name)
    if not os.path.exists(album_path):
        raise Http404("Album not found")

    images = []
    for img_file in os.listdir(album_path):
        img_url = settings.MEDIA_URL + f'gallery/{album_name}/{img_file}'
        images.append(img_url)

    return render(request, 'album_detail.html', {
        'album_name': album_name,
        'images': images
    })









import requests
import base64
from django.shortcuts import render
from django.core.files.base import ContentFile
import urllib.parse



def image_view(request):
    image_url = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        if prompt:
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=960&height=720&seed=42&model=flux&nologo=true"

    return render(request, "image.html", {
        "image_url": image_url
    })






import os
import subprocess
from django.conf import settings
from django.shortcuts import render, redirect

DEFAULT_VOICE = "en-CA-LiamNeural"
OUTPUT_DIR = os.path.join(settings.BASE_DIR, "static", "audio")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "message_audio.mp3")

def remove_audio_file():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print("Previous audio removed.")

def generate_audio(text, voice=DEFAULT_VOICE, output=OUTPUT_FILE):
    try:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        command = [
            'edge-tts',
            '--voice', voice,
            '--text', text,
            '--write-media', output
        ]
        subprocess.run(command, check=True, text=True, stderr=subprocess.PIPE)
        print(f"Audio saved at: {output}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def tts_view(request):
    audio_url = None
    selected_voice = DEFAULT_VOICE

    # Handle Generate New button
    if request.method == "POST" and "generate_new" in request.POST:
        remove_audio_file()
        return redirect("tts")  # Replace "tts" with your actual URL name

    # Handle TTS conversion
    if request.method == "POST" and "convert" in request.POST:
        text = request.POST.get("text", "").strip()
        selected_voice = request.POST.get("voice", DEFAULT_VOICE)

        if text:
            success = generate_audio(text, selected_voice)
            if success:
                audio_url = "/static/audio/message_audio.mp3"

    return render(request, "tts.html", {
        "audio_url": audio_url,
        "selected_voice": selected_voice
    })




import requests
from django.conf import settings
from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY = "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"  




def generate_story(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    system_prompt = "You are a creative and engaging storyteller. Generate a compelling, well-structured short story based on the user's prompt. The story should have a beginning, middle, and end, and be written in a descriptive, imaginative tone. and dont use bold style italic or any other use simple style"

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 1024
    }

    response = requests.post(GROQ_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Error generating story."


def story_view(request):
    if "reset" in request.GET:
        request.session.pop("story", None)
        return redirect("story")

    story = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        if prompt:
            story = generate_story(prompt)
            request.session["story"] = story

    story = request.session.get("story", None)
    return render(request, "story.html", {"story": story})


def download_story_pdf(request):
    story = request.session.get("story", "")
    if not story:
        return redirect("story")

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)

    y = 800
    for line in story.split("\n"):
        for subline in [line[i:i+90] for i in range(0, len(line), 90)]:
            if y < 50:
                p.showPage()
                p.setFont("Helvetica", 12)
                y = 800
            p.drawString(50, y, subline)
            y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="story.pdf")


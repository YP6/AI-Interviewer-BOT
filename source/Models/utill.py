from pydub import AudioSegment
from deepface import DeepFace
from keras.models import model_from_json
from AI_Interview_Bot.settings import XML_ROOT, MEDIA_ROOT
import os
import whisper
import opendatasets as od
import cv2
import numpy as np
import os


def toMP3(instance):
        videoPath = instance.videoPath
        
        audioPath = os.path.splitext(videoPath)[0] + '.mp3'
        
        audio = AudioSegment.from_file(videoPath)
        audio.export(audioPath, format='mp3')
        
        return str(audioPath)


def extractEmotions(videoPath,tempPath, interval=5):
    # Open the video file
    cap = cv2.VideoCapture(videoPath)
    # Set the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not cap.isOpened():
        print("Error opening video file")
        return
    # Initialize a hash of counters for emotions
    emotion_counts = {
        'angry': 0,
        'disgust': 0,
        'fear': 0,
        'happy': 0,
        'neutral': 0,
        'sad': 0,
        'surprise': 0
    }
    # Initialize a counter for the total number of frames with detected faces
    total_frames_with_faces = 0
    frame_counter = 0
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame = cv2.resize(frame, (1280, 720))
        if not ret:
            break
        faceDetector = cv2.CascadeClassifier('D:/Code/Repos/AI-Interviewer-BOT/source/Models/haarcascade_frontalface_default.xml')
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces available on camera
        numFaces = faceDetector.detectMultiScale(grayFrame, scaleFactor=1.3, minNeighbors=5)
        cv2.imwrite(tempPath, frame)
        if len(numFaces) != 0:
            # Increment the counter for frames with detected faces
            total_frames_with_faces += 1
            if frame_counter % interval == 0:
                emotionPrediction = DeepFace.analyze(img_path=tempPath, actions=['emotion'], enforce_detection=False)
                dominant_emotion = emotionPrediction[0]['dominant_emotion']
                # Increment the counter for the detected emotion
                emotion_counts[dominant_emotion] += 1
                
        frame_counter += 1
    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
    # Calculate the percentage of frames for each emotion based on frames with detected faces
    emotion_percentages = {emotion: count / frame_counter for emotion, count in emotion_counts.items()}
    return emotion_percentages


def answerExtraction():
    from server.models import InterviewSession
    model = whisper.load_model("base")

    while True:           
        interviews = InterviewSession.objects.filter(processed=False)

        for interview in interviews:
            if interview.videoPath:
                # Extracing answer text from the video.
                audioPath = toMP3(interview) 
                result = model.transcribe(audioPath, language='en', fp16=False)
                interview.answer = result['text']

                # Extracting emotions from the video.
                emotions = extractEmotions(interview.videoPath, 'D:/Code/Repos/AI-Interviewer-BOT/source/assets/tempImage.jpg', interval=30)
                percentSum = sum(emotions.values())

                # calculate adjusted percentages and store in a list of tuples
                adjustedPercentages = [(emotion, count / percentSum * 100) for emotion, count in emotions.items()]

                # sort the adjusted percentages in descending order by percentage
                adjustedPercentages.sort(key=lambda x: x[1], reverse=True)


                for emotion, percentage in adjustedPercentages:
                    print(f"{emotion}: {percentage:.2f}%")
                
                interview.processed = True
                interview.save()


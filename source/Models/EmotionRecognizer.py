import opendatasets as od
import cv2
import numpy as np
from deepface import DeepFace
from keras.models import model_from_json
from AI_Interview_Bot.settings import XML_ROOT, MEDIA_ROOT

faceDetector = cv2.CascadeClassifier(str(XML_ROOT)+'/haarcascade_frontalface_default.xml')

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
        
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # histogram equalization on greyScale image
        grayFrame = cv2.equalizeHist(grayFrame)
        #contrast enhancement using(CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        grayFrame = clahe.apply(grayFrame)
        # median blur to reduce noise
        grayFrame = cv2.medianBlur(grayFrame, 5)
        # detect faces available on camera
        numFaces = faceDetector.detectMultiScale(grayFrame, scaleFactor=1.3, minNeighbors=5)
        cv2.imwrite(tempPath, grayFrame)
        if len(numFaces) != 0:
            
            if frame_counter % interval == 0:
                # Increment the counter for frames with detected faces
                total_frames_with_faces += 1
                # Resize the image to a smaller size for faster computation
                #small_frame = cv2.resize(grayFrame, (0, 0), fx=0.5, fy=0.5)
                emotionPrediction = DeepFace.analyze(img_path=tempPath, actions=['emotion'], enforce_detection=False)
                dominant_emotion = emotionPrediction[0]['dominant_emotion']
                if emotionPrediction[0]['emotion'][dominant_emotion]<50:
                    dominant_emotion='neutral'
                # Increment the counter for the detected emotion
                emotion_counts[dominant_emotion] += 1
                
        frame_counter += 1
    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
    # Calculate the percentage of frames for each emotion based on frames with detected faces
    emotion_percentages = {emotion: count / total_frames_with_faces for emotion, count in emotion_counts.items()}
    return emotion_percentages

def EmotionRecognizer():
    from server.models import InterviewResult
    while True:
        answers = InterviewResult.objects.filter(analysed=False)

        for answer in answers:
            try:
                # Extracting emotions from the video.
                emotions = extractEmotions(str(answer.videoPath), str(MEDIA_ROOT)+'/tempImage'+str(answer.id)+'.jpg', interval=30)
                if emotions:
                    answer.angry = emotions['angry']
                    answer.happy = emotions['happy']
                    answer.disgust = emotions['disgust']
                    answer.fear = emotions['fear']
                    answer.neutral = emotions['neutral']
                    answer.sad = emotions['sad']
                    answer.surprise = emotions['surprise']
                    
                    answer.analysed=True
                    answer.save()
            except Exception as err:
                print("Emotion Recognizer Error:",err)
    
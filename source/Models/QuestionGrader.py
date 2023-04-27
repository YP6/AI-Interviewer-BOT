import tensorflow as tf
import tensorflow_probability as tfp
from AI_Interview_Bot.settings import XML_ROOT
import pandas as pd
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import load_model
import random

# Responses for grades > 90%
responses90 = [
    "Great job, that's an excellent answer!",
    "You nailed it! That's exactly right.",
    "Perfect answer, well done!"
]

# Responses for grades > 80%
responses80 = [
    "Very good answer, you were close to being spot on!",
    "That's a solid answer, well done!",
    "You're on the right track, keep it up!"
]

# Responses for grades > 70%
responses70 = [
    "Good effort, you're getting there!",
    "That's a decent answer, but there's still some room for improvement.",
    "Not bad, keep working on it."
]

# Responses for grades > 60%
responses60 = [
    "Your answer shows promise, but there's still some work to be done.",
    "You're starting to grasp the concept, keep going!",
    "That's a fair attempt, keep practicing."
]

# Responses for grades > 50%
responses50 = [
    "Your answer is a step in the right direction, but needs more work.",
    "You're making progress, but there's still a ways to go.",
    "It's a start, but keep pushing yourself to improve."
]

# Responses for grades > 40%
responses40 = [
    "You're on the right track, but need more practice.",
    "There's some progress, but keep working on it.",
    "Keep practicing, you'll get there eventually."
]

# Responses for grades < 40%
responsesFail = [
    "Your answer needs a lot of work, keep trying.",
    "Keep practicing, you're not there yet.",
    "You need to work on this concept more."
]

def pearson_correlation(y_true, y_pred):
    corr = tfp.stats.correlation(y_true, y_pred)
    return corr

def QuestionGrader():
    from server.models import InterviewSession, InterviewResult, QuestionAnswers
    from .SentencePreprocessor import SentencePreprocessor
    
    
    SP = SentencePreprocessor([],RANKER=pd.read_csv(str(XML_ROOT)+'/ComputerScienceTFIDF_Filtered_Normalized_index.csv'))
    custom_objects = {'pearson_correlation': pearson_correlation}
    GraderModel = load_model(str(XML_ROOT)+'/roberta model 3 0.77', custom_objects=custom_objects, compile=False)
    GraderModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=[pearson_correlation])


    while True:           
        sessions = InterviewSession.objects.filter(processed=True, graded=False)
        for session in sessions:
            try:
                question = session.questionID
                answers = QuestionAnswers.objects.filter(questionID=question)
                grade = 0
                bestGrade = None
                for answer in answers:
                    if len(answer.answer) > 0:
                        SP.clear()
                        SP.data = [answer.answer, session.answer]
                        SP.Preprocess()
                        score = GraderModel.predict([SP.embeddings[0], SP.embeddings[1]]) * 100
                        if score > grade:
                            grade = score
                            bestGrade = SP
                        print(score, grade)
                
                InterviewResult.add(attendanceID=session.attendanceID, questionID=session.questionID, answer=session.answer,
                                                videoPath=session.videoPath, grade=grade, importantWords=str(bestGrade.ExtractImportantWords()[1]), importantSentences=str(bestGrade.ExtractImportantSentences()[1]))

                if score < 50:
                    session.canTryAgain = True

                session.graded=True
                botResponse = ""
                responseIndex = random.randint(0,2)
                if grade >= 90:
                    botResponse = responses90[responseIndex]
                elif grade >= 80:
                    botResponse = responses80[responseIndex]
                elif grade >= 70:
                    botResponse = responses70[responseIndex]
                elif grade >= 60:
                    botResponse = responses60[responseIndex]
                elif grade >= 50:
                    botResponse = responses50[responseIndex]
                elif grade >= 40:
                    botResponse = responses40[responseIndex]
                elif grade < 40:
                    botResponse = responsesFail[responseIndex]

                session.botResponse = botResponse
                session.save()
                
            except Exception as err:
                print("Question Grader Error:")
                SP.Preprocess()
                print("Question Grader Error:",err)
            
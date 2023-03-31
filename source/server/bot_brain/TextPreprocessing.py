import spacy
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numerizer
import tqdm
nlp = spacy.load('en_core_web_md')


def tokenize(s):
    tokens = nlp(s.lower())
    newS = ""
    nouns = set()
    nums = set()
    num_words = set()
    numerizer = tokens._.numerize()
    for num in numerizer:
        number = numerizer.get(num)
        realNumber = False
        try:
            float(number)
            realNumber = True
        except:
            pass
        if realNumber:
            nums.add(number)
        else:
            num_words.add(number)
    for token in tokens:
        lemma = token.lemma_
        if not token.pos_ == 'PUNCT':
            newS += lemma + " "
            if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN' or token.pos_ == 'ADJ') and not token.is_stop:
                nouns.add(lemma)

    return newS, nouns, nums, num_words

model = SentenceTransformer('bert-base-nli-mean-tokens')
model.encode("dimensions").shape

def embedding_similarity(s1, s2):
  e1 = model.encode(s1)
  e2 = model.encode(s2)
  similarity = cosine_similarity([e1], [e2])[0][0]
  return similarity

def embedding_mean(s):
  e = model.encode(s)
  return np.mean(e, axis=0)

def embedding_mean_similarity(l1, l2):
  e1 = np.mean(model.encode(l1),axis=0) if not len(l1) == 0 else np.zeros(768)
  e2 = np.mean(model.encode(l2), axis=0) if not len(l2) == 0 else np.zeros(768)
  similarity = cosine_similarity([e1], [e2])[0][0]
  return similarity

def Similarty(sen1,sen2):
  s1,s1_nouns,s1_nums,s1_num_words=tokenize(sen1)
  s2,s2_nouns,s2_nums,s2_num_words=tokenize(sen2)

  s1_s2_sim = embedding_similarity(s1,s2)

  s1_nouns=list(s1_nouns)
  s2_nouns=list(s2_nouns)
  nouns_sim = embedding_mean_similarity(s1_nouns,s2_nouns)

  nums_mismatches = (len(s1_nums - s2_nums) + len(s2_nums - s1_nums))

  s1_num_words = s1_num_words if not len(s1_num_words) == 0 else [""]
  s2_num_words = s2_num_words if not len(s2_num_words) == 0 else [""]
  s1_num_words=list(s1_num_words)
  s2_num_words=list(s2_num_words)
  num_words_similarity = embedding_mean_similarity(s1_num_words, s2_num_words)

  return s1, s2, s1_nouns, s2_nouns, s1_nums, s2_nums, s1_num_words, s2_num_words, s1_s2_sim, nouns_sim, num_words_similarity, nums_mismatches

import re
import spacy
from spacy.matcher import Matcher
from spacy import displacy
from spacy.tokens import Span
import pandas as pd
import numpy as np
import numerizer
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

class SentencePreprocessor:
  def __init__(self, data,RANKER, nlp= spacy.load('en_core_web_md'), 
               TRANSFORMER_MODEL=SentenceTransformer('roberta-large-nli-stsb-mean-tokens'), 
               MAX_RANK=5000, MAX_WORDS=50, SENTENCE_SIZE=30, truncation=True, padding=True, paddingText='[EMPTY]', minWordsInSentence=2):
      self.truncation = truncation
      self.padding = padding
      self.minWordsInSentence = minWordsInSentence
      self.nlp = nlp
      self.TRANSFORMER_MODEL = TRANSFORMER_MODEL
      self.NOUN_PROPN_PRON_ADJ = ['NOUN', 'PROPN', 'PRON', 'ADJ']
      self.NOUN_VERBS = ['VERB', 'NOUN', 'PROPN', 'PRON', 'ADJ', 'ADV']
      self.VERB_ADVERB = ['VERB', 'ADV']
      self.PATTERNS = [
                  [
                  {'POS': 'PART', 'OP':'?'},
                  {'POS':{"IN":self.NOUN_VERBS},'OP':'{0,4}'},
                  {'POS':'ADJ', 'OP':'{0,2}'},
                  {'POS':{"IN":self.NOUN_PROPN_PRON_ADJ},'OP':'{1,4}'},
                  ],
                  
                  [
                  {'POS': 'PART', 'OP':'?'},
                  {'POS':'VERB', 'OP':'{0,4}'},
                  {'POS':{"IN":self.NOUN_VERBS},'OP':'{0,4}'},
                  {'POS':'ADP', 'OP':'+'},
                  {'POS':{"IN":self.NOUN_VERBS},'OP':'{1,4}'},
                  {'POS':'ADP', 'OP':'*'},
                  {'POS':{"IN":self.NOUN_PROPN_PRON_ADJ},'OP':'{0,4}'},
                  ],
                  [
                  {'POS': 'PART', 'OP':'?'},
                  {'POS':{"IN":self.NOUN_PROPN_PRON_ADJ},'OP':'{0,4}'},
                  {'POS':{"IN":self.VERB_ADVERB},'OP':'{1,4}'},
                  {'POS':{"IN":self.NOUN_VERBS},'OP':'{0,4}'},
                  {'POS':'ADP', 'OP':'{1,4}'},
                  {'POS':{"IN":self.NOUN_VERBS},'OP':'{0,4}'},
                  {'POS':{"IN":self.VERB_ADVERB},'OP':'{1,4}'},
                  {'POS':{"IN":self.NOUN_PROPN_PRON_ADJ},'OP':'{0,4}'},
                  ],
                  [
                  {'POS':'INTJ'},
                  {'POS':{"IN":self.VERB_ADVERB},'OP':'{0,4}'},
                  {'POS':'ADJ', 'OP':'{0,4}'},
                  {'POS':{"IN":self.NOUN_VERBS},'OP':'{0,4}'},
                  {'POS':'ADJ', 'OP':'{0,4}'},
                  {'POS':{"IN":self.VERB_ADVERB},'OP':'{0,4}'},
                  {'POS':{"IN":self.NOUN_PROPN_PRON_ADJ},'OP':'{0,4}'},
                  ]

              ]

      self.MATCHER = Matcher(nlp.vocab)
      self.MATCHER.add('Information Extraction', self.PATTERNS, greedy='LONGEST')
      self.RANKER = RANKER
      self.RANKER = self.RANKER.set_index('word')
      self.data = data

      self.MAX_RANK = MAX_RANK
      self.MAX_WORDS = MAX_WORDS
      self.SENTENCE_SIZE = SENTENCE_SIZE

      self.__text = ""
      self.__preprocessedText = ""
      self.__embeddings = []
      self.__doc = None
      self.__words = []
      self.__nums = []
      self.__sentences =[]
      self.__diff_words = set()
      self.__sentences_ranks = {}
      self.__WORDS_RANKS = {}

      self.texts = []
      self.preprocessedTexts = []
      self.embeddings = []
      self.docs = []
      self.words = []
      self.nums = []
      self.sentences = []
      self.diff_words = []
      self.sentences_ranks = []
      self.WORDS_RANKS = []
      self.originalTexts=[]

      self.paddingText = paddingText

  # Ret: Sentence Rank
  def SentenceRank(self, sentence):
      rank = 0
      for word in sentence.split(' '):
          try:
              rank+=self.WORDS_RANKS[word]
          except:
              pass
      return rank
  
  # Ret: Clean Text
  def Clean(self, text):
      # removing paragraph numbers
      text = re.sub('[0-9]+.[\t|\s]','',str(text))
      # removing new line characters
      text = re.sub('\n ','',str(text))
      text = re.sub('\n','',str(text))
      # removing apostrophes
      text = re.sub("'s",'',str(text))
      # removing hyphens
      text = re.sub("-",' ',str(text))
      text = re.sub("—",'',str(text))
      # removing comma
      text = re.sub(",",'',str(text))
      # removing quotation marks
      text = re.sub('\"','',str(text))
      # removing salutations
      text = re.sub("Mr\.",'Mr',str(text))
      text = re.sub("Mrs\.",'Mrs',str(text))
      # removing any reference to outside text
      text = re.sub("[\(\[].*?[\)\]]", "", str(text))

      text = re.sub("\s\s+", ' ', str(text))
      return text
  # Ret: Text
  def ConditionalStopWordsRemoval(self, token):
      if token.dep_ =='neg' or token.pos_ =='ADP' or token.pos_ =='PART':
          return False
      else:
          return True

  # Ret: Sequence Of Sentences
  def Truncate(self):
      self.__sentences_ranks = {}
      if len(self.__sentences) > self.SENTENCE_SIZE:
          for i in range(len(self.__sentences)):
              self.__sentences_ranks[i] = self.SentenceRank(self.__sentences[i])

          self.__sentences_ranks = dict(sorted(self.__sentences_ranks.items(), key=lambda x : x[1], reverse=True)[:self.SENTENCE_SIZE])
          self.__sentences_ranks = dict(sorted(self.__sentences_ranks.items(), key=lambda x : x[0]))
          sens = [self.__sentences[x] for x in self.__sentences_ranks.keys()]
          self.__sentences = sens
      else:
          return

  # Ret: Sequence Of Sentences
  def Pad(self):
      if len(self.__sentences) >= self.SENTENCE_SIZE:
        return
      else:
        for word in self.__WORDS_RANKS:
          if len(self.__sentences) < self.SENTENCE_SIZE:
            self.__sentences.append(word)
          else:
            return
        return
        self.__sentences = [*self.__sentences, *[self.paddingText for _ in range(self.SENTENCE_SIZE-len(self.__sentences))]] 
  

  def Preprocess(self):
      self.originalTexts=[]
      for text in tqdm(self.data):
          #Clear Vars
          self.__text = ""
          self.__preprocessedText = ""
          self.__embeddings = []
          self.__doc = None
          self.__words = []
          self.__nums = []
          self.__sentences =[]
          self.__diff_words = set()
          self.__WORDS_RANKS = {}
          #Clean Text
          self.__text = self.Clean(text)
          self.originalTexts.append(self.__text)
          self.__doc = self.nlp(self.__text)
          for token in self.__doc:
              if token.is_stop:
                  if self.ConditionalStopWordsRemoval(token):
                      continue
              else:
                  if not token.pos_ == 'PUNCT':
                      try:
                          lastLen = len(self.__diff_words)
                          self.__diff_words.add(token.lemma_.lower())
                          if not lastLen == len(self.__diff_words):
                              rank = self.RANKER.loc[token.lemma_.lower(), 'tf-idf']
                          if rank < self.MAX_RANK:
                              self.__WORDS_RANKS[token.lemma_.lower()] = rank
                      except:
                          self.__WORDS_RANKS[token.lemma_.lower()] = np.random.randint(100)
              num = numerizer.numerize(token.text)
              if num == token.text:
                  try:
                      self.__nums.append(float(num))
                  except:
                      self.__words.append(token.lemma_.lower())
              else:
                  self.__nums.append(num)

          self.__WORDS_RANKS = dict(sorted(self.__WORDS_RANKS.items(), key=lambda x : x[1],reverse=True)[:self.MAX_WORDS])

          self.__doc = spacy.tokens.Doc(self.__doc.vocab, self.__words)
          self.__doc = self.nlp(self.__doc)
          matches = self.MATCHER(self.__doc)
          matches = sorted(matches, key=lambda x : x[2])
          
          if len(matches) < len(self.__sentences)/2:
            self.__sentences.append(*self.__text.split('.'))

          for _, start, end in matches:
              if len(self.__doc[start:end].text.split(' ')) >= self.minWordsInSentence: 
                  self.__sentences.append(self.__doc[start:end].text)
          
          if self.truncation:
              self.Truncate()
          if self.padding:
              self.Pad()


          for s in self.__sentences: 
            if not s == self.paddingText:
              self.__preprocessedText += s + ' . '
          self.__embeddings = np.array(self.TRANSFORMER_MODEL.encode(self.__preprocessedText)).reshape(1,1024,1)

          self.texts.append(self.__text)
          self.preprocessedTexts.append(self.__preprocessedText)
          self.embeddings.append(self.__embeddings)
          self.docs.append(self.__doc)
          self.words.append(self.__words)
          self.nums.append(self.__nums)
          self.sentences.append(self.__sentences)
          self.diff_words.append(self.__diff_words)
          self.sentences_ranks.append(self.__sentences_ranks)
          self.WORDS_RANKS.append(self.__WORDS_RANKS)

  def ExtractImportantWords(self):
    spans = []
    for j, text in enumerate(self.originalTexts):
      span=[]
      for i, word in enumerate(text.split(' ')):
        word = word.replace('.', '')
        if word == '' or not word:
           continue
        word = self.nlp(word)[0].lemma_
        if word in self.WORDS_RANKS[j] and self.WORDS_RANKS[j][word]>100:
          span.append((i, i+1))
      spans.append(span)
    return spans

  def ExtractImportantSentences(self):
    spans = []
    for j, text in enumerate(self.originalTexts):
      span =[]
      text = self.Clean(text)
      text = text.replace('.','')
      text = self.nlp(text)
      text = [t.lemma_.lower() for t in text]
      text = ' '.join(text)
      lastIndex = 0
      for sen in self.sentences[j]:
        sen = sen.replace('+','\+')
        sp = sen.split(' ')
        if len(sp) <= 1:
          continue
        pattern = str(".*".join(sp))
        if lastIndex < len(text):
          m = re.search(pattern, text[lastIndex:])
          if m:
            lastIndex = m.end() + 1
            span.append((m.start(), m.end()))

      spans.append(span)
    return spans
  def clear(self):
      self.texts = []
      self.preprocessedTexts = []
      self.embeddings = []
      self.docs = []
      self.words = []
      self.nums = []
      self.sentences = []
      self.diff_words = []
      self.sentences_ranks = []
      self.WORDS_RANKS = []
      self.originalTexts=[]
from flair.data import Sentence
from flair.models import SequenceTagger
import spacy
import nltk
import cv2 

from HandwritingRecognition import get_answer_text

nltk.download('wordnet')
from nltk.corpus import wordnet

def do_tokenisation(sentence_str: str):
    # load tagger
    tagger = SequenceTagger.load("flair/ner-english-ontonotes")

    # make example sentence
    sentence = Sentence(sentence_str)

    # predict NER tags
    tagger.predict(sentence)

    entities = {}
    for label in sentence.get_labels():
        value = label.shortstring.split('/')[0][1:-1]
        key = label.shortstring.split('/')[1]
        try:
            entities[key].append(value)
        except:
            entities[key] = [value]
    
    return entities

def get_verbs(sentence_str: str) -> list:
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(sentence_str)  # Your text here

    words = []
    for token in doc:
        if token.pos_ == "VERB":
            words.append(token.text)
    
    return words

def process_answer(answer: str):
    entities = do_tokenisation(answer)
    verbs = get_verbs(answer)
    entities['VERBS'] = verbs

    return entities

def check_for_synonyms(word: str, word_list: list) -> bool:
    """Returns True if word_list contains a synonym for word else False"""
    for synset in wordnet.synsets(word):
        for lemma in synset.lemma_names():
            if lemma in word_list and lemma != word:
                return True
    return False

def compare_answer(sample_answer: str, student_entities : dict):
    # Assume Answer is correct
    answer_correct = True
    sample_entities = process_answer(sample_answer)
    print('Sample Entity: ', sample_entities)

    error_message = ""  # Explains why the answer is wrong

    for key, value in sample_entities.items():
        if(key != 'VERBS'):
            if not(set(value).issubset(set(student_entities[key]))):
                for word in value:
                    if word not in set(student_entities[key]):
                        error_message += "You didnt include the " + key + " '" + word + "'. " 
                answer_correct = False
        else:
            for verb in value:
                if not(check_for_synonyms(verb, student_entities[key])):
                    error_message += "You didnt mention the verb '" + verb +"'. "
                    answer_correct = False
    
    return answer_correct, error_message

def check_answer(sample_answers :list, student_answer_img):
    # 1) Get student_answer_in_text
    student_answer = get_answer_text(student_answer_img)
    print("Student Answer after OCR: ", student_answer)

    # 2) Process student_answer_text
    student_entities = process_answer(student_answer)
    print("Student entities: ", student_entities)

    # 3) Check each point in sample answer
    score = 0
    explaination = ""
    for point in sample_answers:
        result, error = compare_answer(point, student_entities)
        print("Result = ", result, "; Error = ", error)
        if result:
            score += 1
        else:
            explaination += error
    
    return score, explaination





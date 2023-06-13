# -*- coding: utf-8 -*-
"""ModelBart.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n96mIc5pz3fU0h8fBlMZTk97JWCWHqNZ
    pip install transformers
"""
from transformers import pipeline


class ModelBart:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.candidate_labels = ['promociones', 'recomendacion', 'restaurantes', 'comedia',
                                 'supermercado', 'viaje', 'tutorial', 'festival', 'beneficios',
                                 'queso', 'comida', 'diversión', 'amigos', 'experiencia']

    def topic_model(self, sequence_to_classify):
        result = self.classifier(sequence_to_classify, self.candidate_labels)
        return result["labels"][0:2]
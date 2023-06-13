from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

if __name__ == '__main__':
    from googletrans import Translator
    translator = Translator()

    texto = "Mitos que te recomendamos para iniciar en este mundo y que encuentras en el súper reservado lambrusco fresco y dulcesito la redonda, nosotros ligero y semidulce reservado dulce tinto frío sabe Deli dulce la cetto Blanc de zinfandel fresco y Flores San Telmo malbec ligero con mucho sabor."
    english = translator.translate(texto, dest='en').text

    candidate_labels = ['wine', 'deals', 'recommendation', 'sale']
    print(classifier(english, candidate_labels))
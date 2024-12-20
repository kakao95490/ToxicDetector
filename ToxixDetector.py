import ast
import tkinter as tk
import spacy
import re  
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pandas as pd

# Chargement du modèle de langue de spaCy
nlp = spacy.load("en_core_web_md")

def remplacer_mots_par_num(phrase):
    return ['num' if any(char.isdigit() for char in mot) else mot for mot in phrase]

def preprocess_text(text):
    # Supprimer les liens (URLs) du texte avec une expression régulière
    cleaned_text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)  # Supprime http://, https://, www.

    # Supprimer les caractères spécifiques comme '\n' et '='
    cleaned_text = cleaned_text.replace('\n', ' ').replace('=', '').replace('\r','')

    # Tokeniser avec spaCy
    doc = nlp(cleaned_text)

    # Conserver les tokens voulus
    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_punct or token.text in {'!', '?'}
    ]
    
    
    return tokens

def convert_with_dico(tokens, dico_df):
    #convert tokens to numbers
    #dico_df is a dataframe with 2 columns: 'word' and 'id'
    tokens_id = []
    for token in tokens:
        try:
            tokens_id.append(dico_df[dico_df['word'] == token]['id'].values[0])
        except:
            tokens_id.append(0)
    return tokens_id

def envoyer_texte():
    # Récupérer la valeur du champ de texte et la stocker dans une variable
    texte_saisi = champ_texte.get("1.0", "end-1c") 
    
    # Prétraiter le texte
    tokens = preprocess_text(texte_saisi)
    tokens = remplacer_mots_par_num(tokens)
    tokens = convert_with_dico(tokens, dico_df)
    #pading
    tokens = pad_sequences([tokens], maxlen=200, padding='post')
    
    # Prédire la toxicité du texte
    prediction = model.predict(tokens)
    
    #6 output toxicity : toxic, severe_toxic, obscene, threat, insult, identity_hate
    
    # Afficher le résultat
    etiquette_resultat.config(text=f"toxic: {prediction[0][0]:.2f}, severe_toxic: {prediction[0][1]:.2f}, obscene: {prediction[0][2]:.2f}, threat: {prediction[0][3]:.2f}, insult: {prediction[0][4]:.2f}, identity_hate: {prediction[0][5]:.2f}")
    

    
    


dico_df = pd.read_csv('./dataset/preprocessed/dico.csv')
model = load_model('./models/categorisedToxicity.keras')

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Interface simple avec Tokenization (spaCy)")

# Récupérer la taille de l'écran
screen_width = fenetre.winfo_screenwidth()
screen_height = fenetre.winfo_screenheight()

# Définir la taille de la fenêtre à la moitié de l'écran
window_width = screen_width // 2
window_height = screen_height // 2

# Appliquer la taille à la fenêtre
fenetre.geometry(f"{window_width}x{window_height}")

# Créer un cadre pour la zone de texte et le bouton
frame = tk.Frame(fenetre)
frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

# Créer un widget Scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

champ_texte = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
champ_texte.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


scrollbar.config(command=champ_texte.yview)

bouton_envoyer = tk.Button(fenetre, text="Envoyer", command=envoyer_texte)
bouton_envoyer.pack(pady=10)

etiquette_resultat = tk.Label(fenetre, text="")
etiquette_resultat.pack(pady=10)


fenetre.mainloop()

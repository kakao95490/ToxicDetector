import tkinter as tk
import spacy
import re  # Pour les expressions régulières

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
        if not token.is_stop and (not token.is_punct or token.text in {'!', '?'})
    ]
    
    
    return tokens

def envoyer_texte():
    # Récupérer la valeur du champ de texte et la stocker dans une variable
    texte_saisi = champ_texte.get("1.0", "end-1c")  # Récupérer tout le texte dans le widget Text
    
    # Prétraiter le texte
    tokens = preprocess_text(texte_saisi)
    tokens = remplacer_mots_par_num(tokens)
    
    # Afficher les tokens dans l'étiquette de l'interface
    print(tokens)

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

# Création de la zone de texte (widget Text) qui occupe presque toute la fenêtre
champ_texte = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
champ_texte.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Lier la barre de défilement à la zone de texte
scrollbar.config(command=champ_texte.yview)

# Création d'un bouton pour envoyer le texte
bouton_envoyer = tk.Button(fenetre, text="Envoyer", command=envoyer_texte)
bouton_envoyer.pack(pady=10)

# Création d'une étiquette pour afficher les résultats
etiquette_resultat = tk.Label(fenetre, text="")
etiquette_resultat.pack(pady=10)

# Lancement de la boucle principale
fenetre.mainloop()

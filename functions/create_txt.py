#imports necessaire
import json
from datetime import datetime
import os
from .treat_reponse import treat_all_url

def format_and_save_data(data_object):
    
    
    #creation du path
    directory = "archives"
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    filename = os.path.join(directory, f"news_letters_{date_str}.txt")
    
    
    content = []
    
    # --- Titre 1: Météo ---
    content.append("=========================================")
    content.append("             MÉTÉO")
    content.append("=========================================")
    
    weather_info = data_object.get('weather', {})
    content.append(f"Statut Météo: {weather_info.get('meteo', 'Information non disponible')}\n")
    
    
    # --- Titre 2: Cryptomonnaies (Bitcoin) ---
    content.append("=========================================")
    content.append("             PRIX BITCOIN (BTC)")
    content.append("=========================================")
    
    crypto_info = data_object.get('crypto', {})
    bitcoin_price = crypto_info.get('bitcoin', 'N/A')
    ethereum_price = crypto_info.get('ethereum', 'N/A')
    
    content.append(f"Bitcoin (BTC): {bitcoin_price}")
    content.append(f"Ethereum (ETH): {ethereum_price}\n")
    
    
    # --- Titre 3: Actualités ---
    content.append("=========================================")
    content.append("             ACTUALITÉS")
    content.append("=========================================")
    
    news_list = data_object.get('news', [])
    
    if news_list:
        
        for i, news_item in enumerate(news_list):
            title = news_item.get('title', f'Article sans titre {i+1}')
            
            # --- DÉBUT DE LA CORRECTION ---
            # 1. Récupère la valeur de 'text' (qui peut être None si elle existe mais est vide)
            raw_text = news_item.get('text')
            
            # 2. Vérifie si la valeur est None
            if raw_text is None:
                text_cleaned = '' # Définit une chaîne vide si c'est None
            else:
                
                # On utilise str() au cas où la valeur serait un autre type que string
                text_cleaned = str(raw_text).replace('\n', ' ').strip()
            # --- FIN DE LA CORRECTION ---
            
            content.append(f"--- ARTICLE {i+1} ---")
            content.append(f"Titre: {title}")
            content.append(f"Description: {text_cleaned}")
            content.append("-" * (len(title) + 7))
        
        content.append(f"\nTotal d'articles d'actualité enregistrés : {len(news_list)}")
        
    else:
        content.append("Aucune actualité trouvée.")

    # Écrire le contenu dans le fichier
    try:
        #crée le dossier 'archives' s'il n'existe pas.
        os.makedirs(directory, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"\n✅ Succès : Les données ont été enregistrées dans le fichier '{filename}'.")
        return os.path.abspath(filename)
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'écriture du fichier : {e}")
        return None



import shutil
import os

def remove_repo():
    repo_name = r"C:\Users\hp\Desktop\Qautomate\archives"

    try:
        #suppression du dossier archives
        shutil.rmtree(repo_name)
        print(f"✅ Le dossier '{repo_name}' a été supprimé.")
        
    except FileNotFoundError:
        print(f"⚠️ Le dossier '{repo_name}' n'existe pas.")
        
    except PermissionError:
        #erreur de permission
        print(f"❌ Erreur de permission : Impossible de supprimer le dossier '{repo_name}'.")
        print("   Vérifiez si des fichiers à l'intérieur sont ouverts par un autre programme.")
        
    except Exception as e:
        # Gère toutes les autres erreurs non prévues, comme un problème de chemin trop long.
        print(f"❌ Erreur inattendue lors de la suppression : {e}")

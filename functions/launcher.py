import schedule
from datetime import datetime, timedelta
from .create_txt import format_and_save_data
from .treat_reponse import treat_all_url
from .send_email import mailer
from .remove import remove_repo 

# --- Variables de Planification Globale ---
job_id = None # Pour suivre la tâche planifiée


def planifier_prochaine_execution(prochaine_heure):
    """Annule l'ancien job et reprogramme le processus principal."""
    global job_id
    
    if job_id:
        schedule.cancel_job(job_id)
        
    print(f"\n[PLANIFICATEUR] Reprogrammation de la tâche pour : {prochaine_heure.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Nous planifions à la minute précise pour plus de flexibilité avec les intervalles courts
    # (Note: schedule n'est précis qu'à la minute)
    heure_minute_str = prochaine_heure.strftime("%H:%M")
    
    # Le planificateur doit être configuré pour s'exécuter à cette heure précise.
    job = schedule.every().day.at(heure_minute_str).do(processus_principal)
    job_id = job


def processus_principal():
    """Exécute la chaîne de traitement, envoi le mail, et planifie la suite."""
    print("-" * 50)
    print(f"[DÉBUT TÂCHE] Heure : {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        # Étape 1 & 2 : Traitement et création du fichier
        data = treat_all_url()
        format_and_save_data(data)

        # Étape 3 : Tentative d'envoi du mail
        if mailer():
            # --- CAS 1: SUCCÈS DE L'ENVOI ---
            remove_repo() # Exécute le nettoyage (suppression du dossier archives)

            # Planifie la prochaine exécution 4 heures plus tard
            heure_prochaine_execution = datetime.now() + timedelta(hours=4)
            planifier_prochaine_execution(heure_prochaine_execution)
            
        else:
            # --- CAS 2: ÉCHEC DE L'ENVOI (Mailer a retourné False) ---
            # Planifie la prochaine tentative pour dans 1 heure
            heure_prochaine_tentative = datetime.now() + timedelta(hours=1)
            planifier_prochaine_execution(heure_prochaine_tentative)
            
    except Exception as e:
        # Gère les erreurs critiques dans treat_all_url ou format_and_save_data
        print(f"❌ Erreur critique dans le processus : {e}. Tentative de relance dans 1 heure.")
        heure_prochaine_tentative = datetime.now() + timedelta(hours=1)
        planifier_prochaine_execution(heure_prochaine_tentative)


    print("-" * 50)
    return schedule.CancelJob



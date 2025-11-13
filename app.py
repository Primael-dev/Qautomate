from datetime import datetime, timedelta
import time
import schedule
from functions.launcher import planifier_prochaine_execution


if __name__ == "__main__":
    
    # AJOUT DE +1 MINUTE POUR GARANTIR QUE LA PREMIÈRE MINUTE NE SOIT PAS MANQUÉE
    heure_demarrage = datetime.now() + timedelta(minutes=1)
        
    planifier_prochaine_execution(heure_demarrage)

    print("Planificateur lancé. Le processus va commencer à :", schedule.get_jobs()[0].next_run.strftime("%H:%M:%S"))

    while True:
        schedule.run_pending()
        time.sleep(1)
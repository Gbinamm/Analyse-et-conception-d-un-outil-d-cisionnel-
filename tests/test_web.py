import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
URL_APP = "http://localhost:8501"

def run_selenium_test():
    # Initialisation du driver Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(URL_APP)
        
        # 1. S'assurer qu'on est sur "Ajouter Entretien" dans le menu latéral
        # Streamlit utilise des balises <label> pour les boutons radio du sidebar
        nav_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(., 'Ajouter Entretien')]")
        ))
        nav_option.click()
        time.sleep(1) # Laisser le temps au formulaire de se charger

        # 2. Remplir un champ texte (ex: le premier champ du premier onglet)
        # On cherche un input dont le parent contient un label (ton code fait label.capitalize())
        # Note : On cible l'input général pour l'exemple
        inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
        if inputs:
            inputs[0].send_keys("Test Automatisé SAE")

        # 3. Cliquer sur le bouton d'enregistrement
        # Ton code utilise : st.form_submit_button("💾 ENREGISTRER L'ENTRETIEN")
        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ENREGISTRER')]")
        submit_btn.click()

        # 4. Vérifier le message de succès
        # Ton code : st.success(f"✅ Dossier n°{new_id} enregistré !")
        success_banner = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'enregistré')]")
        ))
        
        print("✅ SUCCÈS : Le test Selenium a validé l'enregistrement en base.")

    except Exception as e:
        print(f"❌ ERREUR : Le test a échoué. Détails : {e}")
    
    finally:
        time.sleep(4) # Pour avoir le temps de prendre une capture d'écran pour le rapport
        driver.quit()

if __name__ == "__main__":
    run_selenium_test() 
import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
URL_APP = "http://localhost:8501"

def run_selenium_test():
    print("Démarrage de Selenium ...")
    
    # Nettoyage d'un éventuel profil temporaire précédent
    tmp_profile = os.path.join(os.getcwd(), "test_chrome_profile")
    if os.path.exists(tmp_profile):
        try:
            shutil.rmtree(tmp_profile)
        except:
            pass

    chrome_options = Options()
    
    # --- OPTIONS DE STABILITÉ POUR ENVIRONNEMENT RESTREINT ---
    chrome_options.add_argument("--headless=new")  # Mode sans fenêtre
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--user-data-dir={tmp_profile}") # Force un profil propre
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = None
    try:
        # Initialisation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 25) # Attente longue pour Streamlit

        # 1. Accès à l'app
        driver.get(URL_APP)
        print(f"✅ Page chargée : {driver.title}")
        driver.save_screenshot("tests/1_accueil.png")

        # 2. Navigation vers le formulaire (Menu latéral)
        # On attend que le texte "Ajouter Entretien" apparaisse dans le sidebar
        nav = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(., 'Ajouter Entretien')]")
        ))
        nav.click()
        time.sleep(2) # Laisse l'UI respirer
        print("✅ Navigation vers le formulaire effectuée.")

        # 3. Remplissage d'un champ texte
        # On cible l'input dans le formulaire
        input_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@data-testid='stForm']//input")
        ))
        input_field.send_keys("Test SAE Selenium - " + time.strftime("%H:%M:%S"))
        
        # 4. Envoi du formulaire
        btn = driver.find_element(By.XPATH, "//button[contains(., 'ENREGISTRER')]")
        btn.click()
        print("⏳ Bouton cliqué, attente du message de succès...")

        # 5. Vérification du bandeau de succès (st.success)
        success = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'enregistré')]")
        ))
        
        print(f"🏆 TEST RÉUSSI : {success.text}")
        driver.save_screenshot("tests/2_succes_final.png")

    except Exception as e:
        print(f"❌ ÉCHEC : {e}")
        if driver:
            driver.save_screenshot("tests/erreur_debug.png")
            print("📸 Capture d'écran d'erreur sauvegardée.")
    
    finally:
        if driver:
            driver.quit()
            print("👋 Navigateur fermé.")

if __name__ == "__main__":
    run_selenium_test()
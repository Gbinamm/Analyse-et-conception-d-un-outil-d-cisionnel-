import subprocess
import time
import os
import sys
import signal
from Selenium_test_web import run_selenium_test 

def run_app_with_coverage():
    # Chemins
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    app_dir = os.path.join(root_dir, "application")
    app_path = os.path.join(app_dir, "app.py")
    
    # Utilisation du port 8502
    TEST_PORT = "8502"

    print(f"🧹 Nettoyage des anciens processus...")
    if os.name == 'nt':
        subprocess.run("taskkill /f /im streamlit.exe /t", shell=True, capture_output=True)

    print(f"🚀 Lancement de Coverage sur le port {TEST_PORT}...")

    # Ajout du dossier application au PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = app_dir + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [
        sys.executable, "-m", "coverage", "run", 
        f"--source={app_dir}", 
        "-m", "streamlit", "run", app_path, 
        f"--server.port={TEST_PORT}", 
        "--server.headless=true"
    ]
    
    proc = subprocess.Popen(cmd, env=env, stdout=sys.stdout, stderr=sys.stderr, shell=True)
    
    print(f"⏳ Attente de l'initialisation (15s)...")
    time.sleep(15) 
    
    try:
        run_selenium_test()
    except Exception as e:
        print(f"❌ Erreur Test : {e}")
    finally:
        print("🛑 Fermeture du serveur...")
        if os.name == 'nt':
            subprocess.run(["TASKKILL", "/F", "/PID", str(proc.pid), "/T"], capture_output=True)
        else:
            os.kill(proc.pid, signal.SIGINT)
        
        time.sleep(5)
        print("\n📊 GÉNÉRATION DES RAPPORTS...")
        subprocess.run([sys.executable, "-m", "coverage", "report"])
        subprocess.run([sys.executable, "-m", "coverage", "html"])
        print(f"📂 Fichier disponible : {os.path.join(current_dir, 'htmlcov', 'index.html')}")

if __name__ == "__main__":
    run_app_with_coverage()
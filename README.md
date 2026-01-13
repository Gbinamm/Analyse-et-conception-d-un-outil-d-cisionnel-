Pour télécharger les packages, faire : 

pip install -r application/requirements.txt


ou faire : 

pip install -r application/requirements.txt --user


Pour lancer les test web : 

python test_web/Selenium_test_web.py

Pour lancer les tests unitaires : 

pytest tests_unitaires/ --cov=application
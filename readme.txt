From conda:

    - conda create -n DPRM python=3.13      --> CREATE ENVIRONMENT "DPRM"
    - conda activate DPRM                   --> ACTIVATE ENVIRONMENT "DPRM"
    - conda env remove -n DPRM              --> REMOVE ENVIRONMENT "DPRM"
    - conda list -n DPRM                    --> LIST BY ENVIRONMENT "DPRM"

    - conda info                            --> GET ALL INFORMATION FROM CONDA ENV
    - conda env list                        --> GET ALL ENVIRONMENT FROM THIS COMNPUTER

    - pip --version                         --> PIP VERSION
    - pip list| findstr "my"                --> GET LIST OF USED LIBRARY WITH "my"

    From Python:

        - python -m venv tutorial-env       --> CREATE A NEW ENVIRONMENTFROM PYTHON "tutorial-env"
        - tutorial-env\Scripts\activate     --> ACTIVATE NEW ENVIRONMENT "tutorial-env"

        - python -m flask --app board run --port 8000 --debug
    
INSTALL PACKAGE:

    - SQLite3 Editor
    - PDF Viewer
    - Json Editor       --> TO INSTALL
    - HTML Preview      --> TO INSTALL
    - Web Visual Editor --> TO INSTALL

DEFAULT PACKAGE ENVIRONMENT "NEED TO INSTALL"

    - "conda install matplotlib"
    - "conda install -c anaconda requests"
    - "conda install flask"                 OR          "pip install flask"
    - "conda install requests"
    - "conda install xmltodict"
    - "conda install pandas"

    --> TO MYSQL.CONNECTOR --> GO TO CONDA POWERSHELL 

        - conda activate DPRM

            - python -m pip install mysql-connector-python

DEFAULT PACKAGE ENVIRONMENT "-- DO NOT NEED TO INSTALL --"
    
    - "conda install numpy"
    - "conda install sqlite"            
            

Local data base:

        - import sqlite3

        https://www.sqlitetutorial.net
        https://www.sqlitetutorial.net/sqlite-python/creating-database/

GUI application:

        https://www.pythontutorial.net/tkinter/


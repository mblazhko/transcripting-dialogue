# Dialogue Transcriptor

The script getting information from FMP call transcripts and transform it to subtitle.vtt file for subtitles

## How to use

1. Clone the repository:
   ```git clone https://github.com/mblazhko/transcripting-dialogue.git```
2. Navigate to the project directory:
   ```cd transcriprion```
3. Create a virtual environment:
   ```python -m venv env```

4. Activate the virtual environment:
   - For Windows:
   ``` .\env\Scripts\activate```
   - For macOS and Linux:
   ```source env/bin/activate```
5. ```pip install -r requirements.txt```

6. Rename the .env.sample to .env and write here your data:
    
    - API_KEY=API_KEY

7. Run script:

   -  ```python main.py```
   - Enter information what script wants

8. After you will find ready to use subtitles.vtt file in root directory.

    
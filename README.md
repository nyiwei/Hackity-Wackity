# Hackity-Wackity

## Paw Patrol

Paw Patrol is a one stop web application for police officers to analyse crime hotspots and also easily determine the nearest NPC to the crime scene.

**Overview of crime hotspots**

<img width="1415" alt="Screenshot 2024-06-01 at 11 20 17 AM" src="https://github.com/nyiwei/Hackity-Wackity/assets/99710151/aa34686b-a33f-4851-bf8a-eab1b260a27f">

<br><br>
**Easy identification of police to be deployed to the crime scene**
<img width="1431" alt="Screenshot 2024-06-01 at 11 22 42 AM" src="https://github.com/nyiwei/Hackity-Wackity/assets/99710151/adae457a-c8a2-4060-8d8f-f7dad597c1f7">

# Installation

1. Clone the repository <br>
```
git clone https://github.com/yourusername/your-repository.git
```
3. Install dependencies <br>
```
pip install -r requirements.txt
```
5. Set up environment variables <br>
```
export FLASK_APP=app.py
export FLASK_ENV=development
```
5. Run the Flask app
```
flask run
```
6. Access the app in your web browser

# Data Preprocessing
All data used for the solution are retrieved from data.gov.sg and are preprocessed using pandas and geopandas.
As seen below, the data is messy and we needed to preprocessed them for easy accessibility and readibility. 
<br><br>
<img width="528" alt="Screenshot 2024-06-01 at 11 46 19 AM" src="https://github.com/nyiwei/Hackity-Wackity/assets/99710151/4e9962c0-1a65-46c8-9e9b-b318ae5ebf77">

<br><br>

On top of that, we have also utilise oneMap API to determine the nearest NPC to every crime scene.

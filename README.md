# Chess Opening Drills Trainer

Allows users to enter and study chess opening drills using an adapted version of the SuperMemo 2 spaced repetition algorithm utilized by common memorization platforms such as Anki. Easier opening lines are shown less often, maximizing the time-efficiency of daily study. 

## Installation Instructions

First, ensure that python is installed on your machine. Once it is, install the requirements and run the main file from the command line

```
pip install -r requirements.txt
python src/main.py
```

## Usage
Once booted, the program has 4 modes: 

### Add Drills
From this screen, users can play out drills. The circle next to "Color" toggles whether the drill should save as white or black. When the line has been completed, press the save button at the bottom to save the drill to the database

### Study
Every day, the program will open the drill database and find the drills due. Users can practice the drills, stopping anytime to show the answer. Once a drill is complete, the user should select the response option corresponding to their experience (Again, Hard, Good, Easy). For further information, consult the Anki website https://faqs.ankiweb.net/ from which our algorithm was adapted

### Help: 
Overview of available shortcut keys
### Custom: 
Open chess board 

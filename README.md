# Enkibot Prime ST
A companion app built to help enable players to enjoyably participate in the [Four Job Fiesta](https://www.fourjobfiesta.com/), 
a charity event in which participants play through Final Fantasy 5 with randomly selected classes.

This tool is a shameless ripoff of the existing Enkibot Prime project. Now called *ST* because it is 
running in Streamlit, **Enkibot Prime ST** has powerful menus with expanded information and functionality. 

Feel free to visit the public web version of [Enkibot Prime ST](https://enkibot-prime-st.streamlit.app/).

### To Run Enkibot Prime ST Locally
1. Install Python version 3.x
2. Install Streamlit and prerequisites.
  - From a command line, run: `pip install streamlit, pandas, pyyaml` 
  - or from the root of the repository, run: `pip install requirements.txt`.
3. Run: `streamlit run ./main.py`
4. A local web server will start and a web browser with the app will open automatically.

## Features

### Shared with Enkibot Prime

* Generalized and class-specific hints
* Debug option for viewing all class hints

### Unique Features

* Simplified boss stats, vulnerabilities, and weaknesses 
* !Blue magic spellbook and aquisition
* Chemist !Mix resources
* Multi-class selection and live updates to the hint content
* Raw output with copy option and save-to-file button

## Sources

* Blue Magic - https://www.rpgsite.net/feature/11955-final-fantasy-v-blue-magic-how-to-learn-every-spell-for-the-blue-mage
* Bestiary - https://finalfantasy.fandom.com/wiki/Bestiary_(Final_Fantasy_V) 
* !Mix recipes - https://finalfantasy.fandom.com/wiki/Mix_(Final_Fantasy_V) 
* FFV Goons Discord - https://discord.gg/HZc6NCg 
* Career Day Discord
* Streamlit API - https://docs.streamlit.io/library/api-reference

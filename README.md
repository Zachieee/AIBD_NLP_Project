# AIBD_NLP_Project
This repo is a collection of NLP project.

# env
pip install -q -U google-generativeai

pip install sentence-transformers
pip install dateparser

# retrieval.py
sample query: Breaking news in the US in June 2020
sample output:
                                               headline       category                                  short_description         authors       date
4630  John Oliver Rips 'Total F**king Moron' Tucker ...  ENTERTAINMENT  The "Last Week Tonight" host has a blunt quest...        Ed Mazza 2020-06-15
4636  Fox News is Lying About Seattle’s 'Autonomous ...       POLITICS                 It’s more Woodstock than war zone.  Michael Hobbes 2020-06-14
4643  ‘To Say That She’s An Abusive Figure Is An Und...          MEDIA  Sources say Barbara Fedida, a powerful ABC New...      Yashar Ali 2020-06-13
4655  Pulitzer-Winning Pandemic Reporter On Coronavi...       POLITICS  Laurie Garrett warned “most of America seems t...       Lee Moran 2020-06-11
4659  Tucker Carlson Rails Against Elmo And His Dad ...       POLITICS  The Fox News host isn't happy about "Sesame St...        Ed Mazza 2020-06-10
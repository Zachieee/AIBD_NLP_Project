# AIBD_NLP_Project
This repo is a collection of NLP project.

# env
pip install -q -U google-generativeai

pip install sentence-transformers \
pip install dateparser

# retrieval.py
sample query: Breaking news in the US in June 2020 \
sample output:
| Headline                                                                        | Category    | Short Description                                                      | Authors       | Date       |
|---------------------------------------------------------------------------------|-------------|------------------------------------------------------------------------|---------------|------------|
| John Oliver Rips 'Total F**king Moron' Tucker Carlson                          | ENTERTAINMENT| The "Last Week Tonight" host has a blunt quest...                     | Ed Mazza      | 2020-06-15 |
| Fox News is Lying About Seattle’s 'Autonomous Zone'                            | POLITICS    | It’s more Woodstock than war zone.                                     | Michael Hobbes| 2020-06-14 |
| ‘To Say That She’s An Abusive Figure Is An Understatement’                     | MEDIA       | Sources say Barbara Fedida, a powerful ABC News executive, is...      | Yashar Ali    | 2020-06-13 |
| Pulitzer-Winning Pandemic Reporter On Coronavirus Coverage                       | POLITICS    | Laurie Garrett warned “most of America seems to be...                  | Lee Moran     | 2020-06-11 |
| Tucker Carlson Rails Against Elmo And His Dad On 'Sesame Street'               | POLITICS    | The Fox News host isn't happy about "Sesame Street" addressing...      | Ed Mazza      | 2020-06-10 |

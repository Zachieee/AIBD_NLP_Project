# AIBD_NLP_Project
This repo is a collection of NLP project.

# env
pip install -q -U google-generativeai

pip install sentence-transformers

# retrieval.py
sample query: what do people think of apple? \
sample output:


| Index | Original Sentence                                                       | Lemmatized_Text                                                     |
|-------|-------------------------------------------------------------------------|---------------------------------------------------------------------|
| 27    | I'm OVER people bitching about the #iPhone4S.....                        | [["I'm", 'OVER', 'people', 'bitching', 'about', 'the', '#iPhone4S']] |
| 100   | Love my new I0S5 @Apple updates. Just when I thought I'd heard it all... | [['Love', 'my', 'new', 'I0S5', '@Apple', 'updates', 'Just', 'when', 'I', 'thought', 'I'd', 'heard', 'it', 'all']] |
| 26    | RT @imightbewrong: I'm OVER people bitching about the #iPhone4S.......   | [['RT', '@imightbewrong:', "I'm", 'OVER', 'people', 'bitching', 'about', 'the', '#iPhone4S']] |
| 733   | @iancollinsuk @Apple what's incredible, is that...                        | [['@iancollinsuk', '@Apple', "what's", 'incredible', 'is', 'that']]  |
| 781   | @paulbentleymelb @apple I think they call that...                        | [['@paulbentleymelb', '@apple', 'I', 'think', 'they', 'call', 'that']] |
| 701   | Is @Apple's voice #tech really as impressive as they say?                | [['Is', "@Apple's", 'voice', '#tech', 'really', 'as', 'impressive', 'as', 'they', 'say']] |
| 290   | @Apple unhappy again with service/product quality....                    | [['@Apple', 'unhappy', 'again', 'with', 'service', 'product', 'quality']] |

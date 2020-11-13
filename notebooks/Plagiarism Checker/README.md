# Plagiarism Checker using NLTK and Cosine Similarity

This repository consists of files required to create and deploy a Plagiarism Checker as a WebApp using Flask.

### Methodology:
- NLTK library for tokenizing and removing stopwords from the query.  
- Webscrapping for finding articles with similar content as the query.  
- Cosine Similarity to check the similarity content between query and the listed article.  
  
### Files:
| filename | Description |
|----------|-------------|
| requirements.txt | Basic libraries and packages required for execution |
| report.pdf | Complete Document |
| helper.py, app.py | Python scripts for model creation and deployment |
| static/*, templates/* | Front-end (HTML CSS styling) for Webapp |

### Steps to Execute:
- Make sure you have all the libraries and packages as mentioned in the requirements.txt  
- Run `python3 app.py`  
- Open the browser and go to URL : http://127.0.0.1:5000/  
- Enter the text and click on the 'Generate Report' button to get the match percentage and source urls.  

### TestApp:
![Screenshot](how_to_use.gif)
  
##### That's all! Happy Learning :)

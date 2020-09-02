# COVID- 19 data scrapping Using Beautiful Soup

As a first step to understand webscrapping, I have gathered the covid-19 data from the [worldometers](https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/) website. Webscrapping is achieved by using Beautiful Soup. The scrapped data is then cleaned and visualized.

### Pre-requisites:
Scrapping packages : beautifulsoup4, requests  
Handling data: Pandas, Numpy   
Data visualization packages: matplotlib, seaborn  
  
To install: pip install <requirements>

### Results:

1. Scrapped, cleaned data is saved as covid-19-country-data-02082020.csv

2. Chunk of scrapped dataset  
![Screenshot](https://github.com/supria68/Data-Science-Projects/blob/master/notebooks/mini_projects/webscrapping/datachunk.png)
  
3. Top 10 countries worstly affected by Covid-19 pandemic  
![Screenshot](https://github.com/supria68/Data-Science-Projects/blob/master/notebooks/mini_projects/webscrapping/Total_confirm_case.png)
  
4. Number of deaths due to Covid-19 in the top 10 worstly affected countries  
![Screenshot](https://github.com/supria68/Data-Science-Projects/blob/master/notebooks/mini_projects/webscrapping/No_of_deaths.png)
  
5. Percentage of Covid-19 deaths per confirmed cases in each continent  
![Screenshot](https://github.com/supria68/Data-Science-Projects/blob/master/notebooks/mini_projects/webscrapping/death_rate.png)

### Reference:
[Python Tutorial: Web Scraping with BeautifulSoup and Requests](https://www.youtube.com/watch?v=ng2o98k983k)

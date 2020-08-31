# Exploring evolution of Linux ~ Data Manipulation and Cleaning using R

### Introduction:
Version control repositories are a real gold mine for software developers mainly because they contain the changes to the source code including the date (when), the responsible developer (who), as well as little message that describes the intention (what) of that change.
  
In this project, I have analysed the evolution of an open-source project – 'Linux kernel'. The Linux kernel is the heart of Linux distributions like Debian, Ubuntu or CentOS. There exists a mirror of the [Linux repository](https://github.com/torvalds/linux/) on GitHub. It contains the complete history of kernel development for the last 13 years. In this project, I mainly focus on identifying the TOP 10 contributors to the Linux repo and visualize their commits over the years.

### Requirements:
Install [R and R studio](https://techvidvan.com/tutorials/install-r/).  
  
### Dataset Creation:
The dataset was created by using the command git log --encoding=latin-1 --pretty="%at#%aN". The latin-1 encoded text output was saved in a csv file. In this file, each row is a commit entry with the following information:
  
timestamp: the time of the commit as a UNIX timestamp in seconds since 1970-01-01 00:00:00 (Git log placeholder "%at")  
author: the name of the author that performed the commit (Git log placeholder "%aN")  
The columns are separated by the ',' and the complete dataset is saved as git_log.csv.
  
Here's a chunk of dataset:

|   | Timestamp |	Author|
| - |-----------|-------|
| 0 |	1502826583 | Linus Torvalds|
| 1 |	1501749089 | Adrian Hunter |
| 2	| 1501749088 | Adrian Hunter |
| 3	| 1501882480 | Kees Cook |
| 4 |	1497271395 | Rob Clark |
  
### Data Analysis:
In this section, I performed some data cleaning, wrangling and visualizing methods using several R packages namely lubridate, dplyr, ggplot2.
  
### Results:
##### 1. Number of authors commiting to Linux repo over the past 13 years.   
- 17385 authors committed 699071 code changes.  
  
##### 2. Top 10 Contributors to the Linux Repo.  

| Authors | Commits |
|---------|---------|
| Linus Torvalds | 23361 |
| David S. Miller | 9106 |
| Mark Brown | 6802 |
| Takashi Iwai | 6209 |
| Al Viro | 6006 |
| H Hartley Sweeten | 5938 |
| Ingo Molnar | 5344 |
| Mauro Carvalho Chehab | 5204|
| Arnd Bergmann | 4890 |
| Greg Kroah-Hartman | 4580 |  

  
#### 3. Visualizations  
2016 is the year with most commits.

![Screenshot](https://github.com/supria68/Data-Science-Projects/blob/master/R_Programming/r_visualization.png)

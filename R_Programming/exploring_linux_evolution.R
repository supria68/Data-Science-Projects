# R script to perform the data analysis and visualization of the Linux evolution
# Tasks: 
# 1. Identifying the TOP 10 contributors to Linux repository
# 2. Visualizing the commits over the years to Linux repository

#----------------- Reading the dataset

log = read.csv('git_log.csv', header = TRUE, sep = ",")
head(log) # Display first 6 rows of dataset
summary(log) # Summary of the dataset
str(log) # Structure of dataset

#-----------------Part 1: Data Analysis

# 1. calculating number of commits
num.commits <- nrow(log)

# 2. calculating number of authors
num.authors <- length(unique(log$author))
paste(num.authors, ' authors committed ', num.commits,' code changes.')

# 3. TOP 10 contributors that changed the Linux kernel very often.
freq.data <- table(log$author) 
top10 <- as.data.frame(head(sort(freq.data, decreasing = T), 10))
colnames(top10) <- c('Authors', 'Commits')
top10

#----------------Part 2: Data Visualization

# use the information in the timestamp column to create a time series-based column
if (!require("lubridate")) install.packages("lubridate")
library(lubridate)

log$corrected_timestamp <- as.POSIXlt(log$timestamp, origin = "1970-01-01 00:00:00", tz = "UTC")
log$timestamp <- NULL
summary(log)

# Determining first real commit timestamp
first.commit <- tail(log, 1)$corrected_timestamp

# determining the last sensible commit timestamp
last.commit <- today(tzone = "UTC")

# filtering out wrong timestamps
corrected.log <- log[(log$corrected_timestamp >= first.commit) & (log$corrected_timestamp <= last.commit), ]
head(corrected.log)
summary(corrected.log)

# group the commits by year
corrected.log$Year <- year(ymd(as.Date(corrected.log$corrected_timestamp)))
corrected.log

if (!require("dplyr")) install.packages("dplyr")
library(dplyr)
visual.log <- corrected.log %>% group_by(Year) %>% summarise(author = n())

colnames(visual.log) <- c('Year', 'Commits')
visual.log

if (!require("ggplot2")) install.packages("ggplot2")
library(ggplot2)

q <- ggplot(visual.log, aes(x = Year, y = Commits)) +
  geom_line(color="blue", size=1.2) + geom_point() 

q + xlab('Year') + ylab('Commits') +
  ggtitle('Commits to Linux repo over the years ') +
  theme(axis.title.x = element_text(size = 15),
        axis.title.y = element_text(size = 15),
        plot.title = element_text(hjust = 0.5, size = 20))

# removing all the unnecessary data from environment
rm(corrected.log, first.commit, last.commit, freq.data)

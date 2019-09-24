# Scrapy #

The project is a web scraper. It scrapes a website and stores information in a relational database
It uses the "scrapy" framework to extract data from the website. 

Further the natural language processing module "spacy" is used to train the model to process the 
data from the website. 

The website used in the project is "http://news.ycombinator.com/jobs" which get the jobs posted and 
extract the job-title, company and job-location for each job and store it into the database. 

Database used is mysql
Python3 is required for the project 
  

### Step 1 - Install the mysql community server 

Install the mysql community server. Initialized the "jobs" database

Enter the user-name and password for the mysql-server in the "db_connection_config.py" 

### Step 2 - Run the scraper

```sh
$ cd scraper
$ source myenv/bin/activate
$ scrapy runspider jobs_spider.py -o jobs_data.json
```

### Train model

In the start the data process by the spacy natural language library might not be perfect because the model needs to be trained.
The training data and the code is present in the "models/model.py". 

The command used to train the model is, 

```
$ cd models
$ python model.py

```

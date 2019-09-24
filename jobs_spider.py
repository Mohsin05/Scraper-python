import os
import scrapy
import json
import spacy
import time
import mysql.connector
from database import database


class JobsSpider(scrapy.Spider):

    if os.path.exists("jobs_data.json"):
         os.remove("jobs_data.json")

    name = "jobs"
    start_urls = ('http://news.ycombinator.com/jobs',)


    def parse(self, response):

            nlp = spacy.load("./models/en_ycombinator_model")
            db = database()
            job_id = db.getJobId()

            for sel in response.xpath('//tr[@class="athing"]/td/a'):

                job_posting = sel.xpath('text()').extract()[0]
                doc = nlp(job_posting)
                formatData = {'job': job_posting}

                isDuplicateJob = True if db.isDuplicate(job_posting) else False

                if isDuplicateJob == False:
                    for entity in doc.ents:
                        db.insert( job_id, entity.label_,entity.text, job_posting )
                        print( job_id, entity.label_, entity.text )

                yield (formatData)
                job_id = job_id+1


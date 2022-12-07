# sqlalchamy-challenge


## Background
I've decided to take a long holiday vacation in Honoloulu.  To help with trip planning I'm going to do a climate analysis about the area.  

## Overview
This challenge is broken up into 2 different parts. 
- Part 1 | Analyze and Explore the Climate Data
- Part 2 | Design Your Climate App

### Tools/Programs used during this challenge.
- Python
- SQLAlchemy
- Pandas
- Matplotlib
- Jupyter Notebook
- Flask API

## Part 1 | Analyze and Explore the Climate Data
Using Python and SQLALchamey a basic analysis of the climate and a data exploration of the database.
For this I created a jupyter notebook with SQLAlchemy.
A participitation analysis was done using data collected from 9 stations over a year. 

## Part 2 | Design Your Climate App
My analysis is done, now I'm going to create an API that will query the data that I just developed. 
This API show the analysis of precipitation data, station information, most active stations. 


## Personal Impressions
This challenge made me have to dust off the cobwebs on how to do some of the pandas database; and ensuring that my tables were build correctly.

This is hard to do when the Flask portion would allow the Base.prepare(autoload_with=engine). The python file will run once we take out the autoload_with verbage.

Struggling to get the inspector funciton to work. So I ended up taking that portion out.

With the Flask, I was having some connectivity issues, mostly had to do with stored bashes (Thanks to Ian for helping me on that one.) I tried to add the hyperlinks as we talked about those in class, so I did my best. That was a lot of trial and error to make it work correctly. 
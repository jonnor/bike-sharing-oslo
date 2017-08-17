# Bike sharing data exploration

Exploring aspects of bike sharing using data science.

For INF121 class at NMBU, as part of Master in Data Science.

## Status

Just ideas

## Datasets

* [Austin](https://www.kaggle.com/jboysen/austin-bike) (incl weather)
* [New York Citibike](https://cloud.google.com/bigquery/public-data/nyc-citi-bike), [original](https://www.citibikenyc.com/system-data)
* [Bay area](https://cloud.google.com/bigquery/public-data/bay-bike-share)
* [Washington D.C. Capital Bike share](https://www.capitalbikeshare.com/system-data)
* [Washington D.C, Capital Bike incl weather data](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)

Notes

* Maybe use "feels like temperature" (perceputal) instead of just degrees

## Things to explore

### Possible patterns

To and from work.
Social 'area' versus 'work area'
Special events. Concerts, festival . Yearly?
Popularity in different areas

Crime?? ? any relation to bike???
https://www.kaggle.com/jboysen/austin-crime 

https://www.kaggle.com/crailtap/nyc-real-time-traffic-speed-data-feed

Usage differences wrt weather

### Cross-city comparisons

* weather dependency??
Can we compare US and Europa
Big city versus smaller/town

* Do people go to work/home at same time?

### Trends
Development over time

* Usage
* Any of above patterns

### Usage prediction

### Visualization

### Support or challenge existing results


### Related work
Existing work by othters

* https://www.kaggle.com/c/bike-sharing-demand competition

* https://www.kaggle.com/h19881812/data-vizualization/comments/code
Suprising! "People rent bikes more in fall, and much less in spring"
Expected. "People rent bikes more with good weather"

https://www.kaggle.com/benhamner/bike-rentals-by-time/comments/code
"People rent bikes for morning evening commute on weekdays,
and for the daytime in weekend"

Use graph headlines for the (clear) conclusions supported!

* [brandonharris.io: Kaggle Bike sharing]http://brandonharris.io/kaggle-bike-sharing/
Prediction result in to 10% top of the competition. Example code in R, explained

* [A Tale of Twenty-Two Million Citi Bike Rides](http://toddwschneider.com/posts/a-tale-of-twenty-two-million-citi-bikes-analyzing-the-nyc-bike-share-system/)
Anonymizing data is hard. Can uniquely identify 80-90% of trips based on included (anonymized data).
Analyses how many bikes are manually moved between pick-up stations (by staff).
Models usage relative to weather, incl temperature, rain and snow. Found a non-linear threshold wrt temperature, with transition around 60f/15c.

* [Detecting Anomolous Events in Washington DC Bike Sharing Dataset](http://blog.nycdatascience.com/student-works/detecting-anomolous-events-in-washington-dc-bike-sharing-dataset/).
Using random forest to decide the relative influence of different variables. Time (hour and day) influences most, then weather, wind is last.

* [Citibike.es](https://citybik.es/), public API for 400 cities across the world.
Real-time data, no historical data though?
Website has interactive real-time visualization of bike availability.
Includes Oslo, Stavanger, Bergen.

Can also look at other transportation modes?
Like Taxi trips (and Uber etc)



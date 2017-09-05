
## Things that can be explored

### Time-based features

Across time.
To and from work?
Weekday versus weekend versus holiday.
Seasonal changes

### Geography-based features

Geographical.

Where people sleep, where they work, where they socialize.
Time-based classifier for 'to work', 'from work'?

Connectivity: which stations are connected to which.
Symmetrical relationships?
Asymmetrical? Travelling in one direction primarily. Because downhill?
Self (same start/end station)? Glitches or people actually using bike and going back to same place. VS trip length?
Can be counts of number of trips (in time period). Can also normalize to 0-1 to get relative connectivity.

Based on this and the number of bikes in station, how likely is it that bike station is now empty?
This could be a factor which creates 'anomalies' in the data.
People might have planned/wanted to do a trip, but could not because there was no bike available.

Migration patterns.

http://www.cs.cmu.edu/~aarti/Class/10701/readings/Luxburg06_TR.pdf
http://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html#sklearn.cluster.SpectralClustering

Direction vectors. Plot arrows for each trip onto starting point on map.
Can we aggregate nearby vectors to get a better overall view of migration patterns?
What to do with 'contradicting' vectors? Maybe clustering into K direction vectors, dropping vectors that are too small.
K-nearest neighbours?


Note: we only know start and end point, not direction during trip. Danger of misleading viz?

Can migration patterns be visualized as a heat or heightmap (overlayed onto real map)?
Ex: "downhill" means people go that direction.
or, "uphill" means a lot of people have arrived in area.

Intra-region versus inter-region travels.
Can be done with 'apriori' assigment of regions, as defined by local authorities, real-estate agencies or transportation companies.
Maybe more interesting to invert the relationship, and 'define' regions through peoples travels, e.g.
short trips versus longer ones. 
How well does this correspond to existing definitions of regions?

### Weather dependencies

Temperature. Wind. Rainfall. Snowfall.
Perceived temperature.
What are peoples threshold for biking/not?

### Other ideas for patterns

Across time. To and from work.
Social 'area' versus 'work area'

Special events. Concerts, festival . Yearly?
Popularity in different areas

Crime?? ? any relation to bike???
[Austin crime dataset](https://www.kaggle.com/jboysen/austin-crime)

Any relation to traffic patterns?
[New York traffic speed](https://www.kaggle.com/crailtap/nyc-real-time-traffic-speed-data-feed)

Do more/less people get injured/die in traffic with actively used bike sharing system

Detect missing stations (underserved area). Is it possible based on our data? 
Ideally would be based on individual trip (where people walk to afterwards? where they work/live)
Can maybe use statistics of how many people live in areas to decide

Inefficient stations. Often no bikes available?
Almost never being used?

Are there times where the bikes are not available?
Taken in for season etc
Or times of the day where one cannot take bikes out
Maximum time to rent the bike

### Cross-city comparisons

* Weather dependency??
Can we compare US and Europa
Big city versus smaller/town

* Do people go to work/home at same time?

### Trends
Development over time

* Usage
* Any of above patterns

### Usage prediction

### Visualization

Plot activity on map.

### Support or challenge existing results

### Other transportation modes

Can also look at other transportation modes?

Like Taxi trips (and Uber etc).
Public transportation (train, tram, underground).
Could be 'connections' to public transit.

Either to compare, correlate, or to get inspiration for analysis.


### What people would like to know

City transportation office.
Is the stations being efficiently utilized?

Policians.

Impact on resource usage (CO2).
Impact on health. Long term
Commerce, money spending in area. Do people spend more money if bikes are available? 

In general, evaluate impact.
Can one do a 'dragnet' approach to "finding" impacts?
Compare areas/times where bike transport is available versus not,
across range of different factors (based on available data).
Need to get as similar groups as possible, correct for factors
Need to do quality control, avoiding spurious correlations.

## Datasets

Per-trip

* [Austin](https://www.kaggle.com/jboysen/austin-bike). 649231 trips. From December 2013 - July 2017. 500 trips/day average. 84 MB .csv file
* [New York Citibike](https://cloud.google.com/bigquery/public-data/nyc-citi-bike), [original](https://www.citibikenyc.com/system-data)
* [Bay area](https://cloud.google.com/bigquery/public-data/bay-bike-share)
* [Washington D.C. Capital Bike share](https://www.capitalbikeshare.com/system-data)
* [Washington D.C, Capital Bike incl weather data](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
* [Seattle](https://www.kaggle.com/pronto/cycle-share-dataset)
* [Oslo](https://developer.oslobysykkel.no/data).

* [London](https://data.london.gov.uk/dataset/number-bicycle-hires). Daily, from July 2010.
* [Watson Anlaytics Sample Dataset](https://www.ibm.com/communities/analytics/watson-analytics-blog/operations-dem-planning_-bikeshare/)

Real-time availability

* [Citibike.es](https://citybik.es/), public API for 400 cities across the world.
* [motivate.co: Bikeshare feeds for cities in US](https://www.motivateco.com/use-our-data/)
* [General Bikeshare Feed Specification](https://github.com/NABSA/gbfs), a standardized data feed for bike share system availability.

Notes

* Maybe use "feels like temperature" (perceputal) instead of just degrees

## Related work
Existing work by others

* [Kaggle bike sharing prediction competition](https://www.kaggle.com/c/bike-sharing-demand)

* [Kaggle bike sharing analysis 1](https://www.kaggle.com/h19881812/data-vizualization/comments/code)
Suprising! "People rent bikes more in fall, and much less in spring"
Expected. "People rent bikes more with good weather"

* [Kaggle bike sharing analysis by Ben Hamner](https://www.kaggle.com/benhamner/bike-rentals-by-time/comments/code)
"People rent bikes for morning evening commute on weekdays,
and for the daytime in weekend"

Use graph headlines for the (clear) conclusions supported!

* [brandonharris.io: Kaggle Bike sharing](http://brandonharris.io/kaggle-bike-sharing)
Prediction result in to 10% top of the competition. Example code in R, explained

* [A Tale of Twenty-Two Million Citi Bike Rides](http://toddwschneider.com/posts/a-tale-of-twenty-two-million-citi-bikes-analyzing-the-nyc-bike-share-system/)
Anonymizing data is hard. Can uniquely identify 80-90% of trips based on included (anonymized data).
Analyses how many bikes are manually moved between pick-up stations (by staff).
Models usage relative to weather, incl temperature, rain and snow. Found a non-linear threshold wrt temperature, with transition around 60f/15c.

* [Detecting Anomolous Events in Washington DC Bike Sharing Dataset](http://blog.nycdatascience.com/student-works/detecting-anomolous-events-in-washington-dc-bike-sharing-dataset/).
Using random forest to decide the relative influence of different variables. Time (hour and day) influences most, then weather, wind is last.

* [Citibike.es](https://citybik.es/), public API for 400 cities across the world.
Website has interactive real-time visualization of bike availability.

* [bikeshare-research.org](https://bikeshare-research.org/), links to lot of Bike Sharing Systems.
Has API for getting access to data of many of them. Also only real-time, nothing historical?

* [Guardian: Bike share mapping creates beautiful portraits of London, NYC and Berlin](https://www.theguardian.com/cities/2016/aug/09/bike-share-mapping-gps-data-interactive-london-nyc-berlin-cf-city-flows). Pretty visualizations of trips over time

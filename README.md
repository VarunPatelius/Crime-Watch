# Crime Watch

## About
Crime Watch is a simple desktop application that was created for the 2020 Congressional App Challenge. It uses the FBI-NIBRS and Spotcrime APIs to show crime that has occured near you on a map, state crime statistics from 2000 to 2018, and a basic crime breakdown for each major city in that state.

Reddit Post: [Here](https://www.reddit.com/r/Python/comments/iexkwp/crime_watch_an_interactive_way_to_view_crime/)
Youtube Video: [Here](https://www.youtube.com/watch?v=HxjXqmBpjP4)

## Usage
In order to use Crime Watch, after cloning, open a terminal in the directory and enter:

```bash
pip install -r requirements.txt
```
This will install all the libraries necessary in order to run Crime Watch


In addition, you will also need to go to configure.ini file and input the API keys for the corresponding keys:

  - [ipInfo](https://ipinfo.io/signup)
  - [stateData](https://api.data.gov/signup/)
  - [cityData](https://www.opendatanetwork.com)
  
It should look like this:
```bash
[ipInfo]
key=xxxxxxxxxxxxxx

[stateData]
key=xxxxxxxxxxxxxx

[cityData]
key=xxxxxxxxxxxxxx
```

## Running File
Once you have installed all necessary dependencies and have updated configure.ini, you can run the main.py in the file directory
```bash
python3 main.py
```

## Where It Works
Crime Watch works in the continental United States, however some rural areas may not show any data.

## Application
![Home Page](https://github.com/BlastSolar/Crime-Watch/blob/master/src/Image%20Assets/Github/homePage.png?raw=true)
![Address Map](https://github.com/BlastSolar/Crime-Watch/blob/master/src/Image%20Assets/Github/addressMap.png?raw=true)
![City Data](https://github.com/BlastSolar/Crime-Watch/blob/master/src/Image%20Assets/Github/cityChart.png?raw=true)
![State Data](https://github.com/BlastSolar/Crime-Watch/blob/master/src/Image%20Assets/Github/stateGraph.png?raw=true)
![Current Map](https://github.com/BlastSolar/Crime-Watch/blob/master/src/Image%20Assets/Github/currentMap.png?raw=true)

## Credits
- Varun Patel
- Jay Chaplot
- Annelis Irigoyen
- Aditya Gade

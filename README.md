# Tung-Au-Temperature-Visualizer

## Introduction
This is a tool I created to visualize temperature changes in Tung Au Laboratory in Porter Hall at Carnegie Mellon University. I created it for the purposes of 12-301: Civil & Environmental Engineering Projects.

## Features
This tool takes in a csv file, plots the points on a map of Tung Au Lab, and loops the visualization. No parameters can be changed at this point.
The tool merges the data from all the day and merges them into 24 hours. It then loops through each hour, linearly interpolating data between hours if no data was available.

## Usage
### Dependencies
This program has several dependencies.
+ Python 2.7
+ pandas
+ NumPy
+ SciPy
+ matplotlib

The easiest way to install all of these dependencies at once is to install [Anaconda](https://www.continuum.io/downloads), a distribution of python for data science. If you install Anaconda, be sure to install the Python 2.7 version for the purpose of running this program. If you do not wish to install Anaconda, each of these dependencies can be installed individually as well.

### Getting Data
This tool is meant to be used with the unified data from the class, which is recorded in [a Google Sheet](https://docs.google.com/a/andrew.cmu.edu/spreadsheets/d/1hrspVE9td1pjHLXmYTPeIDspb6e5GqtgCfN1QduVqck/edit?usp=sharing). In order to use this data, you must first download the sheet as a csv.
Once you have saved the csv file, run the program
+ On Mac or Linux, open a shell in the directory containing main.py and type `python main.py`
+ On Windows, open a command prompt window in the folder containing main.py and type `python main.py`

You will be prompted to provide the path of the csv file. Provide this path. If you saved the csv file in the same directory as main.py, this is simply the name of the csv file.
A window will pop up with a map of Tung Au Lab with data point, which will change color depending on the temperature at the time indicated by the title of the visualization. The scale ranges from yellow to red, with yellow indicating a temperature of 20°C and red indicating a temperature of 27°C.

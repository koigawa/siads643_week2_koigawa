
**About**:<br>
For this assignment, I have chosen to productionize a data processing script that I had written as part of my Milestone I group project. What the script does is that it takes in a CSV file, which must be downloaded from Kaggle, and then performs preprocessing/cleaning to ensure that format is suitable to make visualizations out of. To be more specific, what the script is doing is taking results of historical football matches, formatting the results so that we have each country's success rating at two most recent iterations of the World Cup tournaments, and then creating visualization using Altair library to sort countries based on historical performances. Given that some of the cleaning was file specific, the scripts are quite specialized, but efforts were taken to generalize when possible and remove assumptions by having the values enter as fixed constants to avoid hardcoding.

**How to set up the environment to run the scripts**:<br>
Required packages:
- vl-convert-python
- altair
- pandas

Required data:
- A file called results.csv from below URL (but also included in git just in case)
https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017?select=results.csv

**How to run the scripts**:<br>
There are two arguments needed to run the script, the input file path and the output file path.
The first input should be a file path, pointing to the csv file to be consumed.
The second input should be a png file, which will contain the graph as output.
It can be run, for example, like this: python3 main.py results.csv output.png

**Description of each scripts functionality**:<br>
Each section of the original Jupyter notebook has been segmented based on what they did:
- load.py : Takes in a CSV and turns it into a DataFrame
- preprocess_clean.py : Takes in a DataFrame and outputs a DataFrame that is a list of countries and their scores
- visualize.py : This takes in a dataframe outputted by preprocess_clean.py and then outputs Altair visual/graph

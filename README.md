## Career Modeling of a B-Tier NBA Player
Web scraping and linear regression project

The purpose of this analysis is to find which aspects of the game lead to most playing time and salary in professsional basketball players. The findings are that increasing shooting percentage across foul shots, 3-pointers, and 2-point shots while reducing fouls committed yield the greatest return in playing time. Once playing time is increased, there is potential for more salary, but it is not guaranteed.  Therefore, a transfer is recommended to a team with higher median salary- 10 are listed.

The [data set](https://github.com/aaronfrederick/B-Tier-Basketball-Career-Modeling/blob/master/master_df.pkl) used samples box score data from basketball-reference.com. It was scraped using code in [bball_scrape.py](https://github.com/aaronfrederick/B-Tier-Basketball-Career-Modeling/blob/master/bball_scrape.py) then stored in a pickled pandas dataframe. [Salary data](https://github.com/aaronfrederick/B-Tier-Basketball-Career-Modeling/blob/master/nba_salaries_1990_to_2018.csv) curated by data.world users was origionally from basketball-reference.com. These dataframes were combined and stored as [another pickled pandas dataframe](https://github.com/aaronfrederick/B-Tier-Basketball-Career-Modeling/blob/master/merged_df.pkl). The [code](https://github.com/aaronfrederick/B-Tier-Basketball-Career-Modeling/blob/master/Project%20Luther%20Dataframe%20Management.ipynb) used to curate these dataframes can be found in the Jupyter Notebook Project Luther Dataframe Management.ipynb.

Once the data was scraped and processed, the bulk of the modeling and visualization was done in the notebook [Project Luther Visualization and Modeling](https://github.com/aaronfrederick/B-Tier-Basketball-Career-Modeling/blob/master/Project%20Luther%20Visualization%20and%20Modeling.ipynb). The notebook contains the data manipulation and graphing tools used to optimize the linear model and experiment with some basic neural network models.




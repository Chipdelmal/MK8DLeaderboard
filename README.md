# MK8DLeaderboard

Webscraping the [MK8D Leaderboard](https://www.speedrun.com/mk8dx#48_Tracks) to do some DataViz.

These scripts scrape the information on the [Mario Kart 8 Deluxe speedrun leaderboards](https://www.speedrun.com/mk8dx#48_Tracks) with Selenium and convert it to a pandas dataframe so that it can be manipulated and analyzed.

##  Usage

To run these scripts, make sure to install the required dependencies first.

### Leaderboard Parser

Download [Selenium's](https://pypi.org/project/selenium/) drivers and place them in the [chromedriver folder](./chromedriver/). After doing that, run the following script:

```bash
python scrape.py CAT SPD ITM
```
with the following options available:

* Categories (CAT): '48', '32', 'Nitro', 'Retro', 'Bonus'
* Speed (SPD): '200cc', '150cc'
* Items (ITM): 'Items', 'NoItems'

For example:

```bash
python scrape.py 48 200cc NoItems
```

This will generate a CSV file for the leaderboard information on the selected options. The CSV contains the following information:

```
Rank, Player, Time, Version, Date
```

for each one the submissions.

Alternatively, run the following command:

```bash
python scrapeAll.py
```

to download all the combinations of the leaderboards in the current date.

### Data Visualizer

UNDER DEVELOPMENT

```bash
python plot.py '2020-09-02_Nitro_200cc_Items.csv'
```


## Dependencies

[seaborn](https://seaborn.pydata.org/), [pandas](https://pandas.pydata.org/), [dateparser](https://dateparser.readthedocs.io/en/latest/), [selenium](https://selenium-python.readthedocs.io/), [matplotlib](https://matplotlib.org/)


## Author

<img src="./media/pusheen.jpg" height="130px" align="middle"><br>

[Héctor M. Sánchez C.](https://chipdelmal.github.io/blog)

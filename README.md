## GDP Growth Forecast

__Authors__:


-Juan Carlos Barroso Ruiz 1388269

-Adrià Colàs Gallardo 1419956

-Lola Pailler García 1430776





The goal of this project is to effectively predict the GDP growth for all countries in the world
using the data provided by the this [database](https://www.kaggle.com/worldbank/world-development-indicators).

The software is executable via the ```cli.py``` script. To train the model just use
```python3 cli.py train``` and to predict use ```python3 cli.py predict -year <the_year_you_want>```. If the year is not available a message will be prompted to your consoles' standard error indicating so.

Prediction is stored in the same database in a table called ```EstimatedGDPGrowth```



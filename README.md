---
title: "GDP Growth Forecast"
output: html_document
authors: Juan
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = FALSE)
```



The goal of this project is to effectively predict the GDP growth for all countries in the world
using the data provided by the this [database](https://www.kaggle.com/worldbank/world-development-indicators).

The software is executable via the ```cli.py``` script. To train the model just use
```python3 cli.py train``` and to predict use ```python3 cli.py predict -year the_year_you_want```.



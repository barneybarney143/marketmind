# engine.py

Contains the `Backtester` class used to simulate trading strategies on historical
data. For each bar it calls the strategy's `next_bar` method, updates equity and
records trades. The backtester supports both single-asset and multi-asset
strategies that return weight dictionaries.

```python
from engine import Backtester
bt = Backtester(my_strategy, price_dataframe)
results = bt.run()
```

The resulting DataFrame includes columns for price, position, emitted signal,
current equity and drawdown.

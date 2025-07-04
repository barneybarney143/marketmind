# streamlit_app.py

Interactive web interface built with Streamlit. Users can select a strategy,
enter parameters and run a back-test or show the latest signal directly in the
browser. The app uses Plotly for charts and displays common performance metrics
(CAGR, maximum drawdown, Sharpe ratio).

Launch with:

```bash
streamlit run streamlit_app.py
```

### Features
- Parameter inputs are generated from the strategy constructor signature.
- Data is cached to speed up repeated runs.
- Buttons allow running back-tests or viewing signals without leaving the page.

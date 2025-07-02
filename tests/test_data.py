import pandas as pd
import pytest
import yfinance as yf

from data import DataDownloader


def test_get_history_raises_on_empty(monkeypatch, tmp_path):
    downloader = DataDownloader(cache_dir=tmp_path)

    def fake_download(*args, **kwargs):
        return pd.DataFrame()

    monkeypatch.setattr(yf, "download", fake_download)

    with pytest.raises(ValueError, match="No data returned for ticker 'NONE'"):
        downloader.get_history("NONE", "2020-01-01", "2020-01-05")

    cache_file = tmp_path / "NONE-2020-01-01-2020-01-05.parquet"
    assert not cache_file.exists()


def test_get_history_single_ticker_columns(monkeypatch, tmp_path):
    downloader = DataDownloader(cache_dir=tmp_path)

    index = pd.date_range("2020-01-01", periods=2, freq="D")
    df = pd.DataFrame(
        {
            "Open": [1, 2],
            "High": [3, 4],
            "Low": [1, 2],
            "Close": [2, 3],
            "Adj Close": [2, 3],
            "Volume": [10, 20],
        },
        index=index,
    )

    def fake_download(*args, **kwargs):
        return df

    monkeypatch.setattr(yf, "download", fake_download)

    result = downloader.get_history("AAPL", "2020-01-01", "2020-01-02")
    assert list(result.columns) == [
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]


def test_get_history_parses_comma_separated(monkeypatch, tmp_path):
    downloader = DataDownloader(cache_dir=tmp_path)

    index = pd.date_range("2020-01-01", periods=1, freq="D")

    def fake_download(ticker: str, *args: str, **kwargs: str) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Open": [1],
                "High": [2],
                "Low": [1],
                "Close": [1],
                "Adj Close": [1],
                "Volume": [1],
            },
            index=index,
        )

    monkeypatch.setattr(yf, "download", fake_download)

    df = downloader.get_history("AAA,BBB", "2020-01-01", "2020-01-02")
    expected_cols = [
        f"aaa_{c}"
        for c in ["open", "high", "low", "close", "adj_close", "volume"]
    ] + [
        f"bbb_{c}"
        for c in ["open", "high", "low", "close", "adj_close", "volume"]
    ]
    assert list(df.columns) == expected_cols

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

import pandas as pd
import boto3
import io
import pytest
from data_loader import DataLoader

def test_load_local(tmp_path):
    # Prepare CSV
    df = pd.DataFrame({"a":[1,2,3]})
    f = tmp_path / "iris.csv"
    df.to_csv(f, index=False)

    loader = DataLoader({"type":"local","path":str(f)})
    out = loader.load()
    pd.testing.assert_frame_equal(out, df)

class DummyBody:
    def __init__(self, data): self._data = data
    def read(self): return self._data

class DummyClient:
    def __init__(self, data): self._data = data
    def get_object(self, Bucket, Key):
        return {"Body": io.BytesIO(self._data)}

class DummySession:
    def __init__(self, data): self._data = data
    def client(self, svc): return DummyClient(self._data)

@pytest.fixture(autouse=True)
def mock_boto(monkeypatch):
    data = b"a,b\n1,2\n3,4\n"
    monkeypatch.setattr(boto3, "Session", lambda profile_name=None: DummySession(data))

def test_load_s3():
    loader = DataLoader({"type":"s3","bucket":"x","key":"y"})
    df = loader.load()
    assert list(df.columns) == ["a","b"]
    assert df.shape == (2,2)

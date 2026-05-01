import os
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import init_db
from src.logic import (
    generate_short_code, is_valid_url, save_url, 
    get_long_url, increment_click, get_stats
)

TEST_DB = "test_database.db"
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    init_db(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

# --- UNIT TESTS (15) ---
def test_u1_len(): assert len(generate_short_code(8)) == 8
def test_u2_alnum(): assert generate_short_code().isalnum()
def test_u3_unique(): assert generate_short_code() != generate_short_code()
def test_u4_v_http(): assert is_valid_url("http://a.com") is True
def test_u5_v_https(): assert is_valid_url("https://a.com") is True
def test_u6_v_invalid(): assert is_valid_url("not_a_url") is False
def test_u7_v_empty(): assert is_valid_url("") is False
def test_u8_save(): assert save_url("https://x.com", "x1", TEST_DB) is True
def test_u9_save_dup(): 
    save_url("https://x.com", "d1", TEST_DB)
    assert save_url("https://y.com", "d1", TEST_DB) is False
def test_u10_get():
    save_url("https://g.com", "g1", TEST_DB)
    assert get_long_url("g1", TEST_DB) == "https://g.com"
def test_u11_get_none(): assert get_long_url("none", TEST_DB) is None
def test_u12_click():
    save_url("https://c.com", "c1", TEST_DB)
    increment_click("c1", TEST_DB)
    assert get_stats("c1", TEST_DB)["clicks"] == 1
def test_u13_click_multi():
    save_url("https://c.com", "m1", TEST_DB)
    increment_click("m1", TEST_DB)
    increment_click("m1", TEST_DB)
    assert get_stats("m1", TEST_DB)["clicks"] == 2
def test_u14_stats():
    save_url("https://s.com", "s1", TEST_DB)
    assert get_stats("s1", TEST_DB)["short_code"] == "s1"
def test_u15_stats_none(): assert get_stats("nil", TEST_DB) is None

# --- INTEGRATION TESTS (7) ---
def test_i1_api_short():
    res = client.post("/api/shorten", json={"long_url": "https://bing.com"})
    assert res.status_code == 200
def test_i2_api_invalid():
    res = client.post("/api/shorten", json={"long_url": "bad"})
    assert res.status_code == 400
def test_i3_redirect():
    save_url("https://p.org", "p1", "url_shortener.db")
    res = client.get("/p1", follow_redirects=False)
    assert res.status_code == 307
def test_i4_red_404(): assert client.get("/err").status_code == 404
def test_i5_stats():
    save_url("https://t.com", "t1", "url_shortener.db")
    assert client.get("/api/stats/t1").status_code == 200
def test_i6_stats_404(): assert client.get("/api/stats/err").status_code == 404
def test_i7_index(): assert client.get("/").status_code == 200
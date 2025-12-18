from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string, random
from fastapi.responses import RedirectResponse
import sqlite3

app = FastAPI(title='URL-Shorter')

class URLItem(BaseModel):
    url: str

# db = {}
conn = sqlite3.connect('urls.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS urls (
            short_url TEXT PRIMARY KEY,
            full_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0)
            """)
conn.commit()

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        cur.execute("SELECT * FROM urls WHERE short_url = ?", (short_id,))
        if cur.fetchone() is None:
            return short_id
        
@app.get("/TestLongURLforCheckRedirectForShortURL")
def test_url():
    return {'text': 'Тест успешен, всё супер!'} 

@app.post("/shorten")
def shorten_url(item: URLItem):
    short_id = generate_short_url()
    cur.execute("INSERT INTO urls (short_url, full_url) VALUES (?, ?)",
                (short_id, item.url))
    conn.commit()
    # db[short_id] = {'url': item.url, 'clicks': 0}
    return {'short_id': short_id}
    
@app.get("/{short_id}")
def redirected_url(short_id: str):
    cur.execute("SELECT full_url, clicks FROM urls WHERE short_url = ?", (short_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="URL not found")
    full_url, clicks = row
    clicks += 1
    cur.execute("UPDATE urls SET clicks = ? WHERE short_url = ?", (clicks, short_id))
    conn.commit()
    # if short_id not in db:
    #     raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(full_url)


@app.get("/stats/{short_id}")
def get_stats(short_id: str):
    cur.execute("SELECT short_url, clicks FROM urls WHERE short_url = ?", (short_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="URL not found")
    short_id, clicks = row
    return {'url': short_id, 'clicks': clicks}

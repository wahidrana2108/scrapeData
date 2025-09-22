from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:21081997@localhost:5432/scraper_db"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM scraped_resources"))
    for row in result:
        print(row)

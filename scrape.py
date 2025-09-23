import requests
from bs4 import BeautifulSoup
import json
import argparse
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
import urllib.robotparser
import re
from models.base import Base

load_dotenv()

DATABASE_URL = None

Base = declarative_base()


class ScrapedResource(Base):
    __tablename__ = "scraped_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    category = Column(String, nullable=True)
    price = Column(String, nullable=True)


def extract_price(price_str):
    match = re.search(r'[\d\.]+', price_str)
    if match:
        return float(match.group())
    return None


def check_robots(url):
    try:
        robots_url = url.split('/')[0] + '//' + url.split('/')[2] + '/robots.txt'
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        can_fetch = rp.can_fetch('*', url)
        return can_fetch
    except Exception as e:
        print(f"if problem arrive when robots.txt: {e}, Assuming Accepted")
        return True



def scrape_books(pages):
    scraped_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, pages + 1):
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"

        if not check_robots(url):
            print(f"No Permission: {url}")
            continue

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for book in soup.find_all('article', class_='product_pod'):
            title = book.find('h3').find('a')['title']
            price_raw = book.find('p', class_='price_color').text
            price = extract_price(price_raw)

            book_url = "http://books.toscrape.com/catalogue/" + book.find('h3').find('a')['href']

            book_response = requests.get(book_url, headers=headers)
            book_soup = BeautifulSoup(book_response.text, 'html.parser')
            breadcrumb = book_soup.find('ul', class_='breadcrumb')
            if breadcrumb and len(breadcrumb.find_all('li')) > 2:
                category = breadcrumb.find_all('li')[2].text.strip()
            else:
                category = "Unknown"

            book_data = {
                'title': title,
                'price': price,
                'category': category,
                'url': book_url
            }
            scraped_data.append(book_data)

    return scraped_data


def save_to_db(data, engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        for book in data:
            scraped_resource = ScrapedResource(
                title=book['title'],
                url=book['url'],
                category=book['category'],
                price=book['price']
            )
            session.add(scraped_resource)
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Books and Save to DB")
    parser.add_argument('--pages', type=int, default=1, help="Number of pages to scrape")
    parser.add_argument('--db', type=str, help="Database connection string")
    args = parser.parse_args()

    DATABASE_URL = args.db or os.getenv("DB_URI")

    if not DATABASE_URL:
        print("Database URI is Not Provided.type --db or set DB_URI on .env file")
        exit(1)

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    print(f"Scraping {args.pages} page(s)...")
    scraped_data = scrape_books(args.pages)

    os.makedirs('samples', exist_ok=True)
    with open('samples/scraped.json', 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, indent=4, ensure_ascii=False)

    save_to_db(scraped_data, engine)
    print(f"Saved {len(scraped_data)} books data to database.")
    print(f"Scraped {len(scraped_data)} books data.")

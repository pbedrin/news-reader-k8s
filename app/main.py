import logging
from datetime import datetime
from contextlib import asynccontextmanager

import trafilatura
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlmodel import Session, select

from models import News
from database import init_db, get_session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/", description="Method for checking service health")
async def index(request: Request):
    return "News extraction service is running"


@app.post("/extract/")
def extract_news(url: str, session: Session = Depends(get_session)):
    if (existing_news := session.exec(select(News).where(News.url == url)).first()):
        logger.info(f"Extracted news from {url=} already exists in the database.")
        return existing_news.model_dump()

    html = trafilatura.fetch_url(url)
    if not html:
        logger.error(f"Error downloading HTML from {url}.")
        raise HTTPException(status_code=400, detail="Failed to fetch URL")

    text = trafilatura.extract(html, url=url, include_comments=False)
    if not text:
        logger.error(f"Error extracting attributes from {url}.")
        raise HTTPException(status_code=400, detail="Failed to extract data")

    metadata = trafilatura.extract_metadata(
        html,
        default_url=None,
        date_config={
            'extensive_search': True,
            'original_date': True,
            'max_date': datetime.now().strftime("%Y-%m-%d"),
            'outputformat': '%Y-%m-%d %H:%M:%S %z',
        },
    )

    news = News(
        url=url,
        title=metadata.title,
        subtitle=metadata.description,
        publication_date=metadata.date,
        text=text,
        author=metadata.author,
        categories=",".join(metadata.categories),
        tags=",".join(metadata.tags),
        source=metadata.sitename
    )

    session.add(news)
    session.commit()
    session.refresh(news)

    logger.info(f"News from {url} has been extracted and saved in the database.")

    return news.model_dump()

from fastapi import APIRouter, Query
from datetime import datetime

router = APIRouter()

# timestamp -> datetime
def parse_timestamp(event_date: int = Query(...,
                    description="Timestamp in seconds")) -> datetime:
    return datetime.utcfromtimestamp(event_date)
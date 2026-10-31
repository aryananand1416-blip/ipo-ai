
from fastapi import APIRouter, HTTPException
from app.services.database import get_connection

router = APIRouter(prefix="/ipos", tags=["IPOs"])


@router.get("/status")
def ipo_status():

    return {
        "status": "ok",
        "service": "IPO database",
        "model_version": "IPO_AI_v1"
    }


@router.get("/")
def get_ipos(limit: int = 50):

    limit = max(1, min(limit, 500))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.ipo_id,
            i.ipo_name,
            i.listing_date,
            i.listing_price,
            i.day1_return,
            i.day2_return,
            p.positive_probability,
            p.predicted_return,
            p.momentum,
            p.ai_score,
            p.risk,
            p.signal,
            p.model_version,
            p.prediction_stage
        FROM ipos i
        LEFT JOIN predictions p
            ON i.ipo_id = p.ipo_id
        ORDER BY COALESCE(p.ai_score, 0) DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    columns = [
        "IPO_ID",
        "IPO_Name",
        "Listing_Date",
        "Listing_Price",
        "Day1_Return",
        "Day2_Return",
        "positive_probability",
        "predicted_return",
        "momentum",
        "ai_score",
        "risk",
        "signal",
        "model_version",
        "prediction_stage"
    ]

    ipos = [
        dict(zip(columns, row))
        for row in rows
    ]

    return {
        "status": "success",
        "count": len(ipos),
        "ipos": ipos
    }


@router.get("/{ipo_id}")
def get_ipo_detail(ipo_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.ipo_id,
            i.ipo_name,
            i.listing_date,
            i.listing_price,
            i.day1_return,
            i.day2_return,
            p.positive_probability,
            p.predicted_return,
            p.momentum,
            p.ai_score,
            p.risk,
            p.signal,
            p.model_version,
            p.prediction_stage
        FROM ipos i
        LEFT JOIN predictions p
            ON i.ipo_id = p.ipo_id
        WHERE i.ipo_id = ?
        ORDER BY p.id DESC
        LIMIT 1
    """, (ipo_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:

        raise HTTPException(
            status_code=404,
            detail=f"IPO {ipo_id} not found"
        )

    columns = [
        "IPO_ID",
        "IPO_Name",
        "Listing_Date",
        "Listing_Price",
        "Day1_Return",
        "Day2_Return",
        "positive_probability",
        "predicted_return",
        "momentum",
        "ai_score",
        "risk",
        "signal",
        "model_version",
        "prediction_stage"
    ]

    return {
        "status": "success",
        "ipo": dict(zip(columns, row))
    }

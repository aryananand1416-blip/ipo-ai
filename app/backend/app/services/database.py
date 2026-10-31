
import sqlite3
import os

DB_PATH = "/content/drive/MyDrive/IPO_AI/app/data/ipo_ai.db"


def get_connection():

    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    return sqlite3.connect(DB_PATH)


def save_prediction(
    ipo_id,
    model_version,
    prediction_stage,
    positive_probability,
    predicted_return,
    momentum,
    ai_score,
    risk,
    signal
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            ipo_id,
            model_version,
            prediction_stage,
            positive_probability,
            predicted_return,
            momentum,
            ai_score,
            risk,
            signal
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ipo_id,
            model_version,
            prediction_stage,
            positive_probability,
            predicted_return,
            momentum,
            ai_score,
            risk,
            signal
        )
    )

    conn.commit()

    prediction_id = cursor.lastrowid

    conn.close()

    return prediction_id


def save_ipo(
    ipo_id,
    ipo_name,
    listing_date,
    listing_price,
    day1_return,
    day2_return
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO ipos (
            ipo_id,
            ipo_name,
            listing_date,
            listing_price,
            day1_return,
            day2_return
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ipo_id,
            ipo_name,
            listing_date,
            listing_price,
            day1_return,
            day2_return
        )
    )

    conn.commit()

    conn.close()


def get_predictions(limit=50):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ipo_id,
            model_version,
            prediction_stage,
            positive_probability,
            predicted_return,
            momentum,
            ai_score,
            risk,
            signal,
            created_at
        FROM predictions
        ORDER BY ai_score DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class IPOPredictionRequest(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow"
    )

    # --------------------------------------------------------
    # IPO identity
    # --------------------------------------------------------

    IPO_ID: Optional[str] = None
    IPO_Name: Optional[str] = None
    Listing_Date: Optional[str] = None
    Listing_Price: Optional[float] = None

    # --------------------------------------------------------
    # Production ML features
    # --------------------------------------------------------

    IPO_Price: float = Field(alias="IPO Price")
    IPO_Size: float = Field(alias="IPO Size")
    Lot: float = Field(alias="Lot")
    P_E: float = Field(alias="P/E")

    QIB: float
    SHNI: float
    BHNI: float
    NII: float
    RII: float
    Total: float

    GMP: float
    GMP_Percent: float

    QIB_NII_Ratio: float
    Retail_NII_Ratio: float
    QIB_Retail_Ratio: float
    Institutional_to_Retail: float

    Subscription_Gap_Total_Retail: float
    Subscription_Gap_QIB_RII: float

    GMP_Absolute_to_Price: float
    GMP_to_Price: float
    GMP_Positive: float

    Subscription_Above_10x: float
    Subscription_Above_20x: float
    Subscription_Above_50x: float
    Subscription_Above_100x: float

    Issue_Size_Log: float
    Subscription_per_Crore: float
    PE_x_GMP: float

    Is_SME: float
    Is_Dual_Listed: float
    Exchange_Count: float
    NSE_Available: float
    BSE_Available: float

    Year: float
    Month: float

    Day1_Return: float
    Day2_Return: float
    Day1_2_Avg_Return: float
    Day1_2_Cumulative: float

    Day1_2_Both_Positive: float
    Day1_2_Both_Negative: float
    Day2_Minus_Day1: float

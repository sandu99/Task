from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator, model_serializer
from typing import List, Optional, Dict

summary_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                        "quantity_sold": 
                        {
                            "mean": 150.5,
                            "median": 145.0,
                            "mode": 140.0,
                            "std_dev": 25.3,
                            "percentile_25": 130.0,
                            "percentile_75": 170.0
                        },
                        "price_per_unit": 
                        {
                            "mean": 25.5,
                            "median": 25.0,
                            "mode": 24.0,
                            "std_dev": 2.5,
                            "percentile_25": 23.5,
                            "percentile_75": 27.0
                        }
                }
            }
        },
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid filters or column names provided."}
            }
        },
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "No data matches the specified filters."}
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {"detail": "An error occurred while processing your request."}
            }
        },
    },
}


class DateRange(BaseModel):
    start_date: str = Field(..., description="Start date for the filter in YYYY-MM-DD format.", \
        example= "2023-01-01")
    end_date:   str = Field(..., description="End date for the filter in YYYY-MM-DD format.", \
        example= "2023-03-30")

    @model_validator(mode='before')
    @classmethod
    def validate_dates(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        
        try:
            if start_date:
                datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD for both start_date and end_date.")
        
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            if start_date_obj > end_date_obj:
                raise ValueError("start_date must be before end_date.")
        
        return values

class Filters(BaseModel):
    date_range: Optional[DateRange] = Field(None, \
        description="Filter data based on a date range.")
    category:   Optional[List[str]] = Field(None, \
        description="List of product categories to include in the filter.", example= ["Electronics", "Stationery"])
    product_ids: Optional[List[int]] = Field(None, \
        description="List of product IDs to include in the filter.", example= [1016, 1017])
    
    @field_validator("product_ids")
    def validate_product_ids(cls, value):
        for element in value:
            if element < 0:
                raise ValueError(f"Element of product_ids cant be less than 0, Element found : {element}.")
        return value

class SummaryRequest(BaseModel):
    columns: Optional[List[str]] = Field(["quantity_sold", "price_per_unit"], \
        description="List of columns for summary statistics. Default includes 'quantity_sold' and 'price_per_unit'.")
    filters: Optional[Filters] = Field(None, description="Filters to apply before computing summary statistics.")

    @field_validator("columns")
    def validate_columns(cls, value):
        available_columns = ["quantity_sold", "price_per_unit"]
        for column in value:
            if column not in available_columns:
                raise ValueError(f"Invalid column: {column}. Must be one of {available_columns}.")
        return value

class ColumnSummary(BaseModel):
    mean:           float = Field(..., description="Mean value of the column")
    median:         float = Field(..., description="Median value of the column")
    mode:           Optional[float] = Field(..., description="Mode value of the column")
    std_dev:        float = Field(..., description="Standard deviation of the column")
    percentile_25:  float = Field(..., description="25th percentile of the column")
    percentile_75:  float = Field(..., description="75th percentile of the column")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mean": 50.5,
                "median": 50.0,
                "mode": 50.0,
                "std_dev": 10.2,
                "percentile_25": 40.0,
                "percentile_75": 60.0
            }
        }

class SummaryResponse(BaseModel):
    summary: Dict[str, ColumnSummary] = Field(
        ...,
        description="Dictionary of column names and their summary statistics"
    )
    
    @model_serializer
    def serialize_model(self) -> Dict[str, ColumnSummary]:
        return self.summary
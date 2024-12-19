from fastapi import Request, APIRouter, HTTPException
from app.schemas import SummaryResponse, SummaryRequest, summary_responses
from app.services import filter_data, calculate_summary_statistics
from typing import Optional

router = APIRouter()


@router.post("/summary", tags=["Summary"], response_model=SummaryResponse, responses=summary_responses)
async def get_summary_statistics(request: Request, request_body: Optional[SummaryRequest]):
    
    try:
        df = request.app.state.df
        filtered_data = filter_data(df, request_body.filters)
        if filtered_data.empty:
            raise HTTPException(status_code=404, \
                detail="No data matches the specified filters.")

        summary = calculate_summary_statistics(filtered_data, request_body.columns)

        return SummaryResponse(summary=summary)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, \
            detail="An error occurred while processing your request.")

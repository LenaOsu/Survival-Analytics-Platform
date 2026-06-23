from pydantic import BaseModel, Field

#block absurd values + protect the endpoint
class SurvivalRequest(BaseModel):
    sex: str = Field(..., pattern="^(male|female)$")
    time: int = Field(..., ge=0, le=5000)
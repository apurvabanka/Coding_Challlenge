from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re


class UserModel(BaseModel):
    id: str = Field(..., min_length=1, max_length=50, description="Unique identifier")
    email: EmailStr = Field(..., description="Valid email address")
    firstName: str = Field(..., min_length=1, max_length=50, description="First name")
    lastName: str = Field(..., min_length=1, max_length=50, description="Last name")
    address: str = Field(..., min_length=1, max_length=200, description="Address")
    entryDate: datetime = Field(..., description="Entry date in ISO format with timezone")

    @field_validator('firstName', 'lastName')
    @classmethod
    def validate_names(cls, v):
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('Name must contain only letters and spaces')
        return v.title()

    @field_validator('address')
    @classmethod
    def validate_address(cls, v):
        if len(v.strip()) < 5:
            raise ValueError('Address must be at least 5 characters long')
        return v.strip()

    @field_validator('entryDate')
    @classmethod
    def validate_date_format(cls, v):
        # Check if the datetime has timezone info
        if v.tzinfo is None:
            raise ValueError('Date must include timezone information')
        
        # Format check for the specific pattern "2014-05-07T17:32:20+00:00"
        expected_format = "%Y-%m-%dT%H:%M:%S%z"
        try:
            # This will raise an error if the format doesn't match
            v.strftime(expected_format)
        except ValueError:
            raise ValueError('Date must be in format: YYYY-MM-DDTHH:MM:SS+00:00')
        
        return v

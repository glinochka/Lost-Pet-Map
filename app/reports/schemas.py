from pydantic import BaseModel, Field, HttpUrl
from datetime import date



class Report(BaseModel):
    description: str = Field(...,max_length=5000 ,description="Описание найденного животного до 5000 символов")
    photo_url: HttpUrl = Field(..., description="Ссылка на фото")

    latitude: float = Field(..., description="Широта")
    longitude: float = Field(..., description="Долгота")

    registered: date = Field(default_factory=date.today, description="Дата создания")

class Patched_report(BaseModel):
    description: str | None  = Field(None, max_length=5000 ,description="Описание найденного животного до 5000 символов")
    photo_url: HttpUrl | None = Field(None, description="Ссылка на фото")

    latitude: float | None = Field(None, description="Широта")
    longitude: float | None = Field(None, description="Долгота")





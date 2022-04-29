from pydantic import BaseModel


class SongResponse(BaseModel):
    name: str
    link: str

    class Config:
        orm_mode = True

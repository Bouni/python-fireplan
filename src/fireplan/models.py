from datetime import datetime

from pydantic import BaseModel, Field


class AlarmDataModel(BaseModel):
    ric: str
    subRIC: str
    einsatznrlst: str
    strasse: str = Field(default="")
    hausnummer: str = Field(default="")
    ort: str = Field(default="")
    ortsteil: str = Field(default="")
    objektname: str = Field(default="")
    koordinaten: str = Field(default="")
    einsatzstichwort: str
    # The API truncates zusatzinfo after 512 characters
    zusatzinfo: str = Field(default="", max_length=512)


class OperationDataModel(BaseModel):
    id: int = Field(default=0)
    einsatzNrLeitstelle: str = Field(default="")
    tagebuchText: str = Field(default="")
    von: str = Field(default="")
    an: str = Field(default="")
    standort: str = Field(default="")
    typ: str = Field(default="")
    timestamp: datetime


class FMSStatusDataModel(BaseModel):
    fzKennung: str = Field(default="")
    status: str = Field(default="")
    statusTime: datetime


class EventDataModel(BaseModel):
    startDate: str | None = None
    endDate: str | None = None
    allDay: bool = False
    subject: str = Field(default="")
    location: str = Field(default="")
    description: str = Field(default="")
    jahr: str | None = None
    monat: str | None = None
    kalenderID: int


class SMSInboundDataModel(BaseModel):
    tstamp: str | None = None
    sender: str | None = None
    text: str | None = None
    modem: str | None = None

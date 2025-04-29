from pydantic import BaseModel, Field


class AlarmDataModel(BaseModel):
    ric: str = Field(default="")
    subRIC: str = Field(default="")
    einsatznrlst: str = Field(default="")
    strasse: str = Field(default="")
    hausnummer: str = Field(default="")
    ort: str = Field(default="")
    ortsteil: str = Field(default="")
    objektname: str = Field(default="")
    koordinaten: str = Field(default="")
    einsatzstichwort: str = Field(default="")
    zusatzinfo: str = Field(default="")


class OperationDataModel(BaseModel):
    id: int = Field(default=0)
    einsatzNrLeitstelle: str = Field(default="")
    tagebuchText: str = Field(default="")
    von: str = Field(default="")
    an: str = Field(default="")
    standort: str = Field(default="")
    typ: str = Field(default="")
    timestamp: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$", default=""
    )


class FMSStatusDataModel(BaseModel):
    fzKennung: str = Field(default="")
    status: str = Field(default="")
    statusTime: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$", default=""
    )


class EventDataModel(BaseModel):
    startDate: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$", default=""
    )
    endDate: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$", default=""
    )
    allDay: bool
    subject: str
    location: str
    description: str
    jahr: str
    monat: str
    kalenderID: int

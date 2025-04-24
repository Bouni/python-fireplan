from datetime import datetime

from pydantic import BaseModel, Field


class AlertDataModel(BaseModel):
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
    timestamp: datetime


class FMSStatusDataModel(BaseModel):
    fzKennung: str = Field(default="")
    status: str = Field(default="")
    statusTime: datetime


# class AlarmdataModel(BaseModel):
#     alarmtext: str = Field(default="")
#     einsatznrlst: str = Field(default="")
#     strasse: str = Field(default="")
#     hausnummer: str = Field(default="")
#     ort: str = Field(default="")
#     ortsteil: str = Field(default="")
#     objektname: str = Field(default="")
#     koordinaten: str = Field(pattern=r"^-?\d+\.\d+,\s?-?\d+\.\d+$", default="")
#     einsatzstichwort: str = Field(default="")
#     zusatzinfo: str = Field(default="")
#     sonstiges1: str = Field(default="")
#     sonstiges2: str = Field(default="")
#     ric: str = Field(default="")
#     subric: str = Field(default="")
#
#
# class StatusdataModel(BaseModel):
#     fzKennung: str = Field(default="")
#     status: str = Field(default="")
#     statusTime: str = Field(
#         pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$", default=""
#     )

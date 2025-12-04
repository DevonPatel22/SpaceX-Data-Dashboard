from sqlmodel import SQLModel, Field, Relationship
from typing import List
from datetime import datetime

class Launch(SQLModel, table = True):
    __tablename__ = "launches"
    id: str | None = Field(default = None, primary_key=True)
    rocketID: str | None = Field(default = None, foreign_key = "rockets.id")
    coreID: str | None = Field(default = None, foreign_key = "cores.id")
    launchDate: datetime
    flightNumber: int
    launchSuccess: bool

    rocket: "Rocket" = Relationship(back_populates = "launches")
    core: "Cores" = Relationship(back_populates="launches")

class Rocket(SQLModel, table = True):
    __tablename__ = "rockets"
    id: str | None = Field(default = None, primary_key=True)
    active : bool
    stages : int
    successRate: int
    costPerLaunch: float
    diameter: float
    mass: float

    launches: List["Launch"] = Relationship(back_populates = "rocket")

class Cores(SQLModel, table = True):
    __tablename__ = "cores"
    id: str | None = Field(default = None, primary_key=True)
    block: int
    status: str
    reuseCount: int
    rtlsLandings: int
    asdsLandings: int

    launches: List["Launch"] = Relationship(back_populates = "core")

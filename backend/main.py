from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlmodel import Session, select, func
from database import getSession
from models import Launch, Rocket, Cores
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(
    title="SpaceX Mission Logistics Database",
    description = "SpaceX data for analyzing success and failure to aid future development"
)

class LaunchResponse(BaseModel):
    id: str
    rocketID: str
    coreID: str
    launchDate: datetime
    flightNumber: int
    launchSuccess: bool

class RocketResponse(BaseModel):
    id: str
    active: bool
    stages: int
    successRate: int
    costPerLaunch: float
    diameter: float
    mass: float

class CoreResponse(BaseModel):
    id: str
    block: int
    status: str
    reuseCount: int
    rtlsLandings: int
    asdsLandings: int

@app.get("/launches/failed")
def get_fails(session: Session = Depends(getSession)):
    statement = select(Launch).where(Launch.success == False).order_by(Launch.id)
    launches = session.exec(statement).all()
    return{
        "count": len(launches),
        "launches": launches
    }

@app.get("/launches/succeeded")
def get_success(session: Session = Depends(getSession)):
    statement = select(Launch).where(Launch.success == True).order_by(Launch.id)
    launches = session.exec(statement).all()
    return{
        "count": len(launches),
        "launches": launches
    }

@app.get("/launches/details")
def get_details(session: Session = Depends(getSession)):
    query = """
            SELECT launches.id  as launch_id, \
                   launches.flightNumber, \
                   launches.launchDate, \
                   launches.launchSuccess, \
                   rockets.id   as rocket_id, \
                   rockets.stages, \
                   rockets.costPerLaunch, \
                   cores.id     as core_id, \
                   cores.status as core_status, \
                   cores.reuseCount \
            FROM launches
                     INNER JOIN rockets ON launches.rocketID = rockets.id \
                     INNER JOIN cores ON launches.coreID = cores.id \
            """
    result = session.exec(query)
    data = [dict(row) for row in result]
    return{
        "count": len(data),
        "launches": data
    }

@app.get("/launches/count")
def get_count(session: Session = Depends(getSession)):
    statement = select(func.count(Launch.id))
    count = session.exec(statement).one()
    return{
        "totalCount": count
    }

@app.get("/launches/countSuccess")
def get_successCount(session: Session = Depends(getSession)):
    statement = select(func.count(Launch.id)).where(Launch.success == True)
    successCount = session.exec(statement).one()
    return{
        "totalSuccessCount": successCount
    }

@app.get("/launches/countFailed")
def get_failCount(session: Session = Depends(getSession)):
    statement = select(func.count(Launch.id)).where(Launch.success == False)
    failCount = session.exec(statement).one()
    return{
        "totalFailCount": failCount
    }

@app.get("/rockets/highStage")
def get_highStage(session: Session = Depends(getSession)):
    maxStatement = select(func.max(Rocket.stages))
    max = session.exec(maxStatement).one()

    statement = select(Rocket).where(Rocket.stages == max)
    rockets = session.exec(statement).all()

    return{
        "highStage": max,
        "count": len(rockets),
        "rockets": rockets
    }

@app.get("/rockets/stagesAscending")
def get_stagesAscending(
        limit : int = Query(2),
        session: Session = Depends(getSession)):
    statement = select(Rocket).order_by(Rocket.stages.asc()).limit(limit)
    rockets = session.exec(statement).all()
    return{
        "limit" : limit,
        "count": len(rockets),
        "rockets": rockets
    }

@app.get("/cores/reuseCount")
def get_reuseCount(
        limit : int = Query(3),
        session: Session = Depends(getSession)):
    statement = select(Cores).order_by(Cores.reuseCount.asc()).limit(limit)
    cores = session.exec(statement).all()
    return{
        "limit" : limit,
        "count": len(cores),
        "cores": cores
    }

@app.get("/launches/byRocketID/{rocket_ID}")
def get_launch(
        rocket_ID: str = Path(),
        session: Session = Depends(getSession)):
    statement = select(Launch).where(Launch.rocketID == rocket_ID)
    launches = session.exec(statement).all()

    if not launches:
        raise HTTPException(status_code=404, detail="Rocket has no launches yet")
    return{
        "rocketID": rocket_ID,
        "count": len(launches),
        "launches": launches
    }

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
    statement = select(Launch).where(Launch.launchSuccess == False).order_by(Launch.id)
    launches = session.exec(statement).all()
    return{
        "count": len(launches),
        "launches": [launch.model_dump() for launch in launches]
    }

@app.get("/launches/succeeded")
def get_success(session: Session = Depends(getSession)):
    statement = select(Launch).where(Launch.launchSuccess == True).order_by(Launch.id)
    launches = session.exec(statement).all()
    return{
        "count": len(launches),
        "launches": [launch.model_dump() for launch in launches]
    }


@app.get("/launches/details")
def get_details(session: Session = Depends(getSession)):
    launches = session.exec(select(Launch)).all()

    result = []
    for launch in launches:
        rocket = session.exec(select(Rocket).where(Rocket.id == launch.rocketID)).first()
        core = session.exec(select(Cores).where(Cores.id == launch.coreID)).first()

        if rocket and core:
            result.append({
                "launch_id": launch.id,
                "flightNumber": launch.flightNumber,
                "launchDate": launch.launchDate,
                "launchSuccess": launch.launchSuccess,
                "rocket_id": rocket.id,
                "stages": rocket.stages,
                "costPerLaunch": rocket.costPerLaunch,
                "core_id": core.id,
                "core_status": core.status,
                "reuseCount": core.reuseCount
            })

    return {
        "count": len(result),
        "launches": result
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
    statement = select(func.count(Launch.id)).where(Launch.launchSuccess == True)
    successCount = session.exec(statement).one()
    return{
        "totalSuccessCount": successCount
    }

@app.get("/launches/countFailed")
def get_failCount(session: Session = Depends(getSession)):
    statement = select(func.count(Launch.id)).where(Launch.launchSuccess == False)
    failCount = session.exec(statement).one()
    return{
        "totalFailCount": failCount
    }

@app.get("/rockets/highStage")
def get_highStage(session: Session = Depends(getSession)):
    maxStatement = select(func.max(Rocket.stages))
    maxStages = session.exec(maxStatement).one()

    statement = select(Rocket).where(Rocket.stages == maxStages)
    rockets = session.exec(statement).all()

    return{
        "highStage": maxStages,
        "count": len(rockets),
        "rockets": [rocket.model_dump() for rocket in rockets]
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
        "rockets": [rocket.model_dump() for rocket in rockets]
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
        "cores": [core.model_dump() for core in cores]
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
        "launches": [launch.model_dump() for launch in launches]
    }

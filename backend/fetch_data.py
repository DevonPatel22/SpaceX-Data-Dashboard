import requests
from fastapi.openapi.utils import status_code_ranges
from sqlmodel import Session
from database import engine, createTable
from models import Launch, Rocket, Cores
from datetime import datetime

def fetchRockets():
    print("Fetching Rockets")
    url = "https://api.spacexdata.com/v4/rockets"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetchCores():
    print("Fetching Cores")
    url = "https://api.spacexdata.com/v4/cores"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetchLaunch():
    print("Fetching Launch")
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def populateDatabase():
    print("Populating Database")
    createTable()

    rocketsdata = fetchRockets()
    coresdata = fetchCores()
    launchdata = fetchLaunch()

    print(f"Found {len(rocketsdata)} rockets")
    print(f"Found {len(coresdata)} cores")
    print(f"Found {len(launchdata)} launch")

    with Session(engine) as session:

        print("\nAdding Rockets to database...")
        for rockets_data in rocketsdata[:10]:
            rocket = Rocket(
                id= rockets_data['id'],
                active = rockets_data.get('active', False),
                stages = rockets_data.get('stages', 0),
                successRate = rockets_data.get('success_rate_pct', 0),
                costPerLaunch = float(rockets_data.get('cost_per_launch', 0)),
                diameter=float(rockets_data['diameter']['meters']) if rockets_data.get('diameter') else 0.0,
                mass=float(rockets_data['mass']['kg']) if rockets_data.get('mass') else 0.0,
            )
            session.add(rocket)

        session.commit()
        print(f"Added {len(rocketsdata[:10])} rockets")

        print("Adding cores to database...")
        for cores_data in coresdata[:50]:

            blockValue = cores_data.get('block')
            if blockValue is None:
                blockValue = 0

            cores = Cores(
                id= cores_data['id'],
                block = blockValue,
                status = cores_data.get('status', 'unknown'),
                reuseCount = cores_data.get('reuse_count', 0),
                rtlsLandings = cores_data.get('rtls_landings', 0),
                asdsLandings = cores_data.get('asds_landings', 0),
            )
            session.add(cores)

        session.commit()
        print(f"Added {len(coresdata[:50])} cores to database")

        print("Adding Launches to database...")
        for launch_data in launchdata[:100]:

            if not launch_data.get('cores') or len(launch_data['cores']) == 0:
                continue

            if not launch_data.get('rocket'):
                continue

            core_id = launch_data['cores'][0].get('core')
            if not core_id:
                continue

            date_str = launch_data.get('date_utc')
            if not date_str:
                continue

            try:
                launch_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                continue

            launch = Launch(
                id= launch_data['id'],
                rocketID = launch_data['rocket'],
                coreID = core_id,
                launchDate = launch_date,
                flightNumber = launch_data.get('flight_number', 0),
                launchSuccess = launch_data.get('success', False)
            )
            session.add(launch)

        session.commit()
        print(f"Added {len(launchdata[:100])} launches to database")

    print("\nDatabase populated")

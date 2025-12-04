import requests
from sqlmodel import Session
from database import engine, createTable
from models import Launch, Rocket, Cores
from datetime import datetime  # Added!


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
    print(f"Found {len(launchdata)} launches")

    with Session(engine) as session:

        print("\nAdding Rockets to database...")
        for rockets_data in rocketsdata[:10]:
            rocket = Rocket(
                id=rockets_data['id'],
                active=rockets_data.get('active', False),
                stages=rockets_data.get('stages', 0),
                successRate=rockets_data.get('success_rate_pct', 0),
                costPerLaunch=float(rockets_data.get('cost_per_launch', 0)),
                diameter=float(rockets_data['diameter']['meters']) if rockets_data.get('diameter') else 0.0,
                mass=float(rockets_data['mass']['kg']) if rockets_data.get('mass') else 0.0,
            )
            session.add(rocket)

        session.commit()
        print(f"✓ Added {len(rocketsdata[:10])} rockets")

        print("\nAdding cores to database...")
        cores_added = 0
        for cores_data in coresdata[:50]:

            blockValue = cores_data.get('block')  # Fixed: removed underscore
            if blockValue is None:
                blockValue = 0

            cores = Cores(
                id=cores_data['id'],
                block=blockValue,
                status=cores_data.get('status', 'unknown'),
                reuseCount=cores_data.get('reuse_count', 0),
                rtlsLandings=cores_data.get('rtls_landings', 0),
                asdsLandings=cores_data.get('asds_landings', 0),
            )
            session.add(cores)
            cores_added += 1

        session.commit()
        print(f"✓ Added {cores_added} cores to database")

        print("\nAdding Launches to database...")
        launches_added = 0

        for launch_data in launchdata[:100]:

            if not launch_data.get('cores') or len(launch_data['cores']) == 0:
                continue

            if not launch_data.get('rocket'):
                continue

            core_id = launch_data['cores'][0].get('core')
            if not core_id:
                continue

            # Parse date - CRITICAL FIX
            date_str = launch_data.get('date_utc')
            if not date_str:
                continue

            try:
                launch_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                continue

            launch = Launch(
                id=launch_data['id'],
                rocketID=launch_data['rocket'],
                coreID=core_id,
                launchDate=launch_date,  # Now a datetime object
                flightNumber=launch_data.get('flight_number', 0),
                launchSuccess=launch_data.get('success', False) if launch_data.get('success') is not None else False
            )
            session.add(launch)
            launches_added += 1

            if launches_added >= 15:
                break

        session.commit()
        print(f"✓ Added {launches_added} launches to database")

    print("\n✅ Database populated successfully!")


if __name__ == "__main__":
    try:
        populateDatabase()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
print("=" * 50)
print("SCRIPT STARTING")
print("=" * 50)

import requests

print("✓ Imported requests")

from sqlmodel import Session

print("✓ Imported Session")

from database import engine, createTable

print("✓ Imported database")

from models import Launch, Rocket, Cores

print("✓ Imported models")

from datetime import datetime

print("✓ Imported datetime")


def fetchRockets():
    print("\n[FETCH ROCKETS] Starting...")
    url = "https://api.spacexdata.com/v4/rockets"
    response = requests.get(url)
    print("[FETCH ROCKETS] Got response")
    response.raise_for_status()
    data = response.json()
    print(f"[FETCH ROCKETS] Got {len(data)} rockets")
    return data


def fetchCores():
    print("\n[FETCH CORES] Starting...")
    url = "https://api.spacexdata.com/v4/cores"
    response = requests.get(url)
    print("[FETCH CORES] Got response")
    response.raise_for_status()
    data = response.json()
    print(f"[FETCH CORES] Got {len(data)} cores")
    return data


def fetchLaunch():
    print("\n[FETCH LAUNCHES] Starting...")
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    print("[FETCH LAUNCHES] Got response")
    response.raise_for_status()
    data = response.json()
    print(f"[FETCH LAUNCHES] Got {len(data)} launches")
    return data


def populateDatabase():
    print("\n" + "=" * 50)
    print("POPULATE DATABASE FUNCTION")
    print("=" * 50)

    print("\n[1] Creating tables...")
    createTable()
    print("✓ Tables created")

    print("\n[2] Fetching data from API...")
    rocketsdata = fetchRockets()
    coresdata = fetchCores()
    launchdata = fetchLaunch()
    print("✓ All data fetched")

    print("\n[3] Opening database session...")
    with Session(engine) as session:
        print("✓ Session opened")

        print("\n[4] Adding rockets...")
        rocket_count = 0
        for rockets_data in rocketsdata[:10]:
            print(f"  Processing rocket {rocket_count + 1}")
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
            rocket_count += 1

        print(f"  Committing {rocket_count} rockets...")
        session.commit()
        print(f"✓ Added {rocket_count} rockets")

        print("\n[5] Adding cores...")
        cores_count = 0
        for cores_data in coresdata[:50]:
            if cores_count % 10 == 0:
                print(f"  Processing core {cores_count + 1}")

            blockValue = cores_data.get('block')
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
            cores_count += 1

        print(f"  Committing {cores_count} cores...")
        session.commit()
        print(f"✓ Added {cores_count} cores")

        print("\n[6] Adding launches...")
        launches_added = 0

        for i, launch_data in enumerate(launchdata[:100]):
            if i % 10 == 0:
                print(f"  Checking launch {i + 1}")

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
                id=launch_data['id'],
                rocketID=launch_data['rocket'],
                coreID=core_id,
                launchDate=launch_date,
                flightNumber=launch_data.get('flight_number', 0),
                launchSuccess=launch_data.get('success', False) if launch_data.get('success') is not None else False
            )
            session.add(launch)
            launches_added += 1

            if launches_added >= 15:
                print(f"  Reached 15 launches, stopping")
                break

        print(f"  Committing {launches_added} launches...")
        session.commit()
        print(f"✓ Added {launches_added} launches")

    print("\n" + "=" * 50)
    print("✅ DATABASE POPULATED SUCCESSFULLY!")
    print("=" * 50)


if __name__ == "__main__":
    print("\n[MAIN] Starting execution...")
    try:
        populateDatabase()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()

    print("\n[MAIN] Script finished")
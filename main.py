import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import logging

logging.getLogger("fastf1").setLevel(logging.CRITICAL)

driverListe = [] 
driverListeTelemetry = []

print("You're on a Formula One tracker")
print("Choose your option")
print("")

def selectYear():
    while True:
        year = input("1. Select the year you want (1950-2026): ")
        print("")
        try:
            year = int(year)
            if year >= 1950 and year <= 2026:
                print("You choose " + str(year))
                return year
            print("ERROR: The value must be in the range of 1950-2026")
            print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")


def selectGP(year):
    print("2. Select the grand prix you want: ")
    print("")
    schedule = fastf1.get_event_schedule(year)
    j = 1
    essaie = 0
    for i in range(len(schedule["RoundNumber"])):
        if schedule['EventFormat'][i] != 'testing':
            print(str(j) + ".", schedule["Country"][i], "(" + schedule["EventName"][i] + ")")
            j += 1
        else:
            essaie += 1
    j -= 1
    print("")
    while True:
        gp = input("Enter a number (1-" + str(j) + "): ")
        print("")
        try:
            gp = int(gp)
            if gp <= j and gp >= 1:
                print("You choose the " + schedule["Country"][gp + essaie - 1] + " Grand Prix (" + schedule["EventName"][gp + essaie - 1] + ")")
                print("")
                return gp + essaie - 1
            print("ERROR: The value must be in the range of (1-" + str(j) + ")")
            print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")

def selectPractice():
    sessionListe = ["FP1", "FP2", "FP3", "Q", "R"]
    sessionListeName = ["Free Practice 1", "Free Practice 2", "Free Practice 3", "Qualifying", "Race"]

    print("3. Select the session: ")
    print("")
    for i in range(len(sessionListe)):
        print(str(i+1) + ". " + sessionListeName[i])
    print("")
    while True:
        session = input("Enter a number (1-5): ")
        print("")
        try:
            session = int(session)
            if session >= 1 and session <= 5:
                print("You choose " + sessionListeName[session - 1])
                print("")
                return sessionListe[session - 1]
            print("ERROR: The value must be in the range of (1-5)")
            print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")
        

###############################################################################################
year = selectYear()
gp = selectGP(year)
practice = selectPractice()

session = fastf1.get_session(year, gp, practice)

session.load()

###############################################################################################

def selectDriver():
    print("4. Select the driver you want: ")
    print("")
    j = 0
    for i in range(len(session.results)):
        print(str(i+1) + ". " + session.results["FullName"].iloc[i])
        j += 1
    print("")
    while True:
        driver = input("Enter a number (1-" + str(j) + "): ")
        print("")
        try:
            driver = int(driver)
            if driver >= 1 and driver <= j:
                print("You choose " + session.results["FullName"].iloc[driver-1])
                print("")
                return session.results["Abbreviation"].iloc[driver-1]
            print("ERROR: The value must be in the range of (1-" + str(j) + ")")
            print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")
###############################################################################################

driver = selectDriver()
driverListe.append(driver)

###############################################################################################

def selectOtherDriver():
    while True:
        print("5. You need to select all the driver you want the data")
        print("")
        print("Select your choice: ")
        print("")
        print("1. Another driver")
        print("2. Continue to have the data")
        print("")
        n = input("Select a number (1-2): ")
        print("")
        try:
            n = int(n)
            if n == 1:
                driver = selectDriver()
                if driver in driverListe:
                    print("Driver already in the list. Choose another one or leave")
                    print("")
                else:
                    driverListe.append(driver)
            elif n == 2:
                return
            else:
                print("ERROR: The value must be 1 or 2")
                print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")

selectOtherDriver()

for driver in driverListe:
    telemetry = session.laps.pick_drivers(driver).pick_fastest().get_telemetry()
    best_lap = session.laps.pick_drivers(driver).pick_fastest()
    dico = {"name": driver, "time": telemetry["Time"], "speed": telemetry["Speed"], "distance": telemetry["Distance"], "color": fastf1.plotting.get_driver_color(driver, session), "lapTime": best_lap["LapTime"], "bestLap": best_lap}
    driverListeTelemetry.append(dico)

def whatShow():
    print("6. What do you want to see")
    print("")
    print("1.Graph")
    print("2.Stats")
    print("3.Both")
    print("")
    while True:
        n = input("Select your choice (1-3): ")
        print("")
        try:
            n = int(n)
            if n >=1 and n <= 3:
                return n
            else:
                print("ERROR: The value must be in the range of (1-3)")
                print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")

def whichGraph():
    print("7. You need to choose which graph you want to see")
    print("")
    print("1. Speed as a function of time")
    print("2. Time as a function of time")
    print("3. Both")
    print("")
    while True:

        n = input("Select your choice (1-3): ")
        print("")
        try:
            n = int(n)
            if n == 1:
                fig, ax = plt.subplots()
                for driver in driverListeTelemetry:
                    ax.plot(driver["distance"], driver["speed"], color=driver["color"], label=driver["name"])
                ax.set_title("Speed comparison between selected drivers")
                ax.set_xlabel("Distance (m)")
                ax.set_ylabel("Speed (Km/h)")
                ax.legend()
                value = saveGraphOption()
                if value:
                    fig.savefig("distance.png")
                plt.show()
                return
            elif n == 2:
                fig, ax = plt.subplots()
                for driver in driverListeTelemetry:
                    ax.plot(driver["distance"], driver["time"].dt.total_seconds(), color=driver["color"], label=driver["name"])
                ax.set_title("Lap Time comparison between selected drivers")
                ax.set_xlabel("Distance (m)")
                ax.set_ylabel("Time (s)")
                ax.legend()
                value = saveGraphOption()
                if value:
                    fig.savefig("time.png")
                plt.show()
                return
            elif n == 3:
                fig, ax = plt.subplots()
                for driver in driverListeTelemetry:
                    ax.plot(driver["distance"], driver["speed"], color=driver["color"], label=driver["name"])
                fig2, ax2 = plt.subplots()
                for driver in driverListeTelemetry:
                    ax2.plot(driver["distance"], driver["time"].dt.total_seconds(), color=driver["color"], label=driver["name"])
                ax.set_title("Speed comparison between selected drivers")
                ax.set_xlabel("Distance (m)")
                ax.set_ylabel("Speed (Km/h)")
                ax2.set_title("Lap Time comparison between selected drivers")
                ax2.set_xlabel("Distance (m)")
                ax2.set_ylabel("Time (s)")
                ax.legend()
                ax2.legend()
                value = saveGraphOption()
                if value:
                    fig.savefig("distance.png")
                    fig2.savefig("time.png")
                plt.show()
                return
            else:
                print("ERROR: The value must be in the range of (1-3)")
                print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")
        

def saveGraphOption():
    print("8.Do you want to Export Graph")
    print("")
    print("1. Export Graph")
    print("2. Leave")
    print("")
    while True:
        n = input("Select your choice (1-2): ")
        print("")
        try:
            n = int(n)
            if n == 1:
                return True
            elif n == 2:
                return False
            else:
                print("ERROR: The value must be in the range of (1-2)")
                print("")
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")



def formatLapTime(time):
    total = time.total_seconds()

    minutes = int(total // 60)
    seconds = total % 60 

    return f"{minutes}:{seconds:06.3f}"


def showGap():
    fasterDriver = driverListeTelemetry[0]
    faster = driverListeTelemetry[0]["lapTime"]
    for driver in driverListeTelemetry:
        if driver["lapTime"] < faster:
            faster = driver["lapTime"]
            fasterDriver = driver
    print(f"Driver: {fasterDriver['name']}")
    print(f"Top speed: {fasterDriver['speed'].max()} km/h")
    print(f"Average speed: {fasterDriver['speed'].mean():.2f} km/h")
    print(f"Best lap time: {formatLapTime(fasterDriver['lapTime'])}")
    print(f"S1: {(fasterDriver['bestLap']['Sector1Time']).total_seconds():.3f}s")
    print(f"S2: {(fasterDriver['bestLap']['Sector2Time']).total_seconds():.3f}s")
    print(f"S3: {(fasterDriver['bestLap']['Sector3Time']).total_seconds():.3f}s")
    print(f"Gap: +{0:.3f}s")
    print("")
    for driver in driverListeTelemetry:
        if driver["name"] != fasterDriver["name"]:
            print(f"Driver: {driver['name']}")
            print(f"Top speed: {driver['speed'].max()} km/h")
            print(f"Average speed: {driver['speed'].mean():.2f} km/h")
            print(f"Best lap time: {formatLapTime(driver['lapTime'])}")
            print(f"S1: {(driver['bestLap']['Sector1Time']).total_seconds():.3f}s")
            print(f"S2: {(driver['bestLap']['Sector2Time']).total_seconds():.3f}s")
            print(f"S3: {(driver['bestLap']['Sector3Time']).total_seconds():.3f}s")
            gap = (driver['lapTime'] - faster).total_seconds()
            print(f"Gap: +{gap:.3f}s")
            print("")

def showRanking():
    ranking = sorted(driverListeTelemetry, key=lambda d: d['lapTime'])

    print("===RANKING===")
    for i in range(len(ranking)):
        print(f"{i+1}. {ranking[i]['name']} - {formatLapTime(ranking[i]['lapTime'])}")

n = whatShow()
if n == 1:
    whichGraph()
elif n == 2:
    showGap()
    showRanking()
else:
    whichGraph()
    showGap()
    showRanking()
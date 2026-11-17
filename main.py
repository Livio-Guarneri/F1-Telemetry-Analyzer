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
    year = input("1. Select the year you want (1950-2026): ")
    print("")
    try:
        year = int(year)
    except ValueError:
        print("ERROR: The value must be an integer")
        print("")
        return selectYear()
    if year < 1950 or year > 2026:
        print("ERROR: The value must be in the range of 1950-2026")
        print("")
        return selectYear()
    print("You chose " + str(year))
    print("")
    return year


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
    gp = input("Enter a number (1-" + str(j) + "): ")
    print("")
    try:
        gp = int(gp)
    except ValueError:
        print("ERROR: The value must be an integer")
        print("")
        return selectGP(year)
    if gp > j or gp < 1:
        print("ERROR: The value must be in the range of (1-" + str(j) + ")")
        print("")
        return selectGP(year)

    print("You choose the " + schedule["Country"][gp + essaie - 1] + " Grand Prix (" + schedule["EventName"][gp + essaie - 1] + ")")
    print("")
    return gp + essaie - 1

def selectPractice():
    sessionListe = ["FP1", "FP2", "FP3", "Q", "R"]
    sessionListeName = ["Free Practice 1", "Free Practice 2", "Free Practice 3", "Qualifying", "Race"]

    print("3. Select the session: ")
    print("")
    for i in range(len(sessionListe)):
        print(str(i+1) + ". " + sessionListeName[i])
    print("")

    session = input("Enter a number (1-5): ")
    print("")
    try:
        session = int(session)
    except ValueError:
        print("ERROR: The value must be an integer")
        print("")
        return selectPractice()
    if session > 5 or session < 1:
        print("ERROR: The value must be in the range of (1-5)")
        print("")
        return selectPractice()
    print("You choose " + sessionListeName[session - 1])
    print("")
    return sessionListe[session - 1]

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
    driver = input("Enter a number (1-" + str(j) + "): ")
    print("")
    try:
        driver = int(driver)
    except ValueError:
        print("ERROR: The value must be an integer")
        print("")
        return selectDriver()
    if driver < 1 or driver > j:
        print("ERROR: The value must be in the range of (1-" + str(j) + ")")
        print("")
        return selectDriver()
    print("You choose " + session.results["FullName"].iloc[driver-1])
    print("")
    return session.results["Abbreviation"].iloc[driver-1]
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
        except ValueError:
            print("ERROR: The value must be an integer")
            print("")
            return selectOtherDriver()
        if n > 2 or n < 1:
            print("ERROR: The value must be 1 or 2")
            print("")
            return selectOtherDriver()
        if n == 1:
            driver = selectDriver()
            if driver in driverListe:
                print("Driver already in the liste choose another one or leave")
                print("")
                return selectOtherDriver()
            else:
                driverListe.append(driver)
        else:
            return

selectOtherDriver()

for driver in driverListe:
    telemetry = session.laps.pick_driver(driver).pick_fastest().get_telemetry()
    dico = {"name": driver, "time": telemetry["Time"], "speed": telemetry["Speed"], "distance": telemetry["Distance"], "color": fastf1.plotting.get_driver_color(driver, session)}
    driverListeTelemetry.append(dico)


distanceMax = []
for driver in driverListeTelemetry:
    distanceMax.append(driver["distance"].max())

def whichGraph():
    print("6. You need to choose which graph you want to see")
    print("")
    print("1. Speed as a function of time")
    print("2. Time as a function of time")
    print("3. Both")
    print("")
    n = input("Select your choice (1-3): ")
    print("")
    try:
        n = int(n)
    except ValueError:
        print("ERROR: The value must be an integer")
        print("")
        return whichGraph()
    if n > 3 or n < 1:
        print("ERROR: The value must be in the range of (1-3)")
        print("")
        return whichGraph()
    if n == 1:
        fig, ax = plt.subplots()
        for driver in driverListeTelemetry:
            ax.plot(driver["distance"], driver["speed"], color=driver["color"], label=driver["name"])
        ax.set_title("Speed comparison between selected driver")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Speed (Km/h)")
        ax.legend()
        plt.show()
        value = saveGraphOption()
        if value:
            fig.savefig("distance.png")
        
    elif n == 2:
        fig, ax = plt.subplots()
        for driver in driverListeTelemetry:
            ax.plot(driver["distance"], driver["time"].dt.total_seconds(), color=driver["color"], label=driver["name"])
        ax.set_title("Lap Time comparison between selected driver")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Time (s)")
        ax.legend()
        plt.show()
        value = saveGraphOption()
        if value:
            fig.savefig("time.png")
        
    else:
        fig, ax = plt.subplots()
        for driver in driverListeTelemetry:
            ax.plot(driver["distance"], driver["speed"], color=driver["color"], label=driver["name"])
        fig2, ax2 = plt.subplots()
        for driver in driverListeTelemetry:
            ax2.plot(driver["distance"], driver["time"].dt.total_seconds(), color=driver["color"], label=driver["name"])
        ax.set_title("Comparaison vitesse tour VER-HAM")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Speed (Km/h)")
        ax2.set_xlabel("Distance (m)")
        ax2.set_ylabel("Time (s)")
        ax.legend()
        ax2.legend()
        plt.show()
        value = saveGraphOption()
        if value:
            fig.savefig("distance.png")
            fig2.savefig("time.png")
        

def saveGraphOption():
    print("7.Do you want to Export Graph")
    print("")
    print("1. Export Graph")
    print("2. Leave")
    print("")
    n = input("Select your choice (1-2): ")
    print("")
    try:
        n = int(n)
    except ValueError:
        print("ERROR: The value must be an integer")
        print("")
        return saveGraphOption()
    if n > 2 or n < 1:
        print("ERROR: The value must be in the range of (1-2)")
        print("")
        return saveGraphOption()
    if n == 1:
        return True
    return False

whichGraph()
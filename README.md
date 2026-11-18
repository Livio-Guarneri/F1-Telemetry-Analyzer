# F1 Telemetry Analyzer

Python application using FastF1 to retrieve and compare Formula 1 telemetry data.

## Features

- Season selection (1950-2026)
- Grand Prix selection
- Session selection:
  - FP1
  - FP2
  - FP3
  - Qualifying
  - Race
- Single or multi-driver comparison
- Speed analysis
- Lap time analysis
- Driver ranking
- Gap to leader calculation
- Sector analysis (S1, S2, S3)
- Top speed statistics
- Average speed statistics
- Graph export as PNG
- Input validation

## Technologies

- Python
- FastF1
- Matplotlib
- NumPy

## Installation

### Clone the repository

```bash
git clone https://github.com/Livio-Guarneri/F1-Telemetry-Analyzer.git
cd F1-Telemetry-Analyzer
```

### Install dependencies

```bash
pip install fastf1 matplotlib numpy
```

### Run the application

```bash
python main.py
```

## Usage

1. Select a season.
2. Select a Grand Prix.
3. Select a session.
4. Select one or more drivers.
5. Choose:
   - Graphs
   - Statistics
   - Both
6. Analyze the results.

## Statistics Available

For each selected driver:

- Best lap time
- Gap to the fastest driver
- Sector 1 time
- Sector 2 time
- Sector 3 time
- Top speed
- Average speed

## Graphs Available

- Speed vs Distance
- Lap Time vs Distance
- Multi-driver comparison

## Example Output

```text
Driver: VER
Top speed: 337 km/h
Average speed: 229.81 km/h
Best lap time: 1:24.582
S1: 27.518s
S2: 33.942s
S3: 23.122s
Gap: +0.000s
```

## Future Improvements

- Graphical User Interface (GUI)
- Additional telemetry analysis
- Interactive visualizations

## Purpose

This project was created to improve my skills in:

- Python development
- Data analysis
- Data visualization
- API integration
- Software design

## Author

**Livio Guarneri**
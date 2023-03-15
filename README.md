# SpringConcertMatchingProgram
The Spring Concert Matching Program (SCMP) is based off of the program used to match medical students to residency programs in the US (the National Residency Matching Program, or NRMP).

This is written in Python 3, so to run the program type:
```
python3 assign_concert.py
```

Currently the program reads member piece preference data from preferences.csv, and song leader preferences in players from songleaderpref.csv.  These file names are hard coded in, but it might be better to make them command line arguments.

Furthermore, adding a GUI, and making the program able to read data from Google sheets directly will probably make the continued use of this program more sustainable.

# Overseer Software's Minimalist ASTRA Simulator

## Warning

**Do NOT merge this branch to `master`!**
This branch is not intended to have the source files for Overseer, nor should its contents be necessary for the ongoing development in `master`.

## Installation

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Setup

Modify the configurations in `cutdown.py`. To be specific, there are a couple of configurations that are useful for our purposes:

- `launchSiteLat`
- `launchSiteLon`
- `launchSiteElev`
- `dateAndTime`
- `balloonGasType`
- `balloonModel`
- `nozzleLift`
- `payloadTrainWeight`
- `parachuteModel`
- `cutdownAltitude`
- `maxFlightTime`

It is recommended to abstain from adding extra fields to construction, but feel free to modify anything else (nothing's stopping you).

Then, to run the script:

```
python3 cutdown.py

# check directory for output files, debug logs, etc.
cat cutdown_output/out.csv # for example
```

## Credits

All of the work was done by [@sobester](https://github.com/sobester/astra_simulator) from the University of Southampton. If they decide they want this branch to be taken down at any point, this branch will cease to exist and be wiped from the repository's history.

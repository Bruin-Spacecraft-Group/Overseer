# -*- coding: utf-8 -*-
# @Date:   2022-01-04 19:43:00
# @Last Modified by:   Sweeney Ngo
# pyright: reportMissingImports=false
# pyright: reportUndefinedVariable=false

if __name__ == "__main__":
    
    from datetime import datetime, timedelta
    import sys
    import os
    from astra.simulator import *

    sys.path.append(os.path.abspath('../astra'))

    # Environment parameters (descriptor)
    # Launch site: Daytona Beach, FL
    #        time: tomorrow, this time

    launchSiteLat = 29.2108                             # deg
    launchSiteLon = -81.0228                            # deg
    launchSiteElev = 4                                  # meters
    dateAndTime = datetime.now() + timedelta(days=1)

    simEnvironment = forecastEnvironment(launchSiteLat,    
                                         launchSiteLon,    
                                         launchSiteElev,        
                                         dateAndTime,
                                         forceNonHD=True,
                                         debugging=True)
    
    # Flight load parameters (descriptor)
    # Launch site: Daytona Beach, FL
    #        time: tomorrow, this time

    balloonGasType = 'Helium'
    balloonModel = 'TA100'
    nozzleLift = 0.6                                    # kg
    payloadTrainWeight = 0.38                           # kg

    simFlight = flight(balloonGasType,
                      balloonModel,
                      nozzleLift,
                      payloadTrainWeight,
                      environment=simEnvironment,
                      parachuteModel='SPH36',
                      numberOfSimRuns=3,
                      cutdown=True,
                      cutdownAltitude=14000,
                      maxFlightTime=5*60*60,
                      outputFile=os.path.join('.', 'cutdown_output'),
                      debugging=True,
                      log_to_file=True)

    # Run the simulation
    simFlight.run()

# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401
from collections.abc import Callable

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    Vector,
    config,
)
from vendeeglobe.utils import distance_on_surface


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = "Oops"  # This is your team name
        # This is the course that the ship has to follow
        # self.course = [
        #     Checkpoint(latitude=43.797109, longitude=-11.264905, radius=50),
        #     Checkpoint(longitude=-29.908577, latitude=17.999811, radius=50),
        #     Checkpoint(latitude=-11.441808, longitude=-29.660252, radius=50),
        #     Checkpoint(longitude=-63.240264, latitude=-61.025125, radius=50),
        #     Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1990.0),
        #     Checkpoint(latitude=-62.052286, longitude=169.214572, radius=50.0),
        #     Checkpoint(latitude=-15.668984, longitude=77.674694, radius=1190.0),
        #     Checkpoint(latitude=-39.438937, longitude=19.836265, radius=50.0),
        #     Checkpoint(latitude=14.881699, longitude=-21.024326, radius=50.0),
        #     Checkpoint(latitude=44.076538, longitude=-18.292936, radius=50.0),
        #     Checkpoint(
        #         latitude=config.start.latitude,
        #         longitude=config.start.longitude,
        #         radius=5,
        #     ),
        # ]
        self.course = [
                Checkpoint(latitude=27.9774487576345, longitude=-65.06541454115296, radius=50),
                Checkpoint(latitude=16.873075857719087, longitude=-68.60776449857379, radius=50),
                Checkpoint(latitude=9.860317266029469, longitude=-80.59116055518038, radius=50),
                Checkpoint(latitude=6.682150603618609, longitude=-78.71306517737868,radius=50), # Panama canal finished
                Checkpoint(latitude=5.480840563786344, longitude=-79.23386963026627,radius=50),
                Checkpoint(latitude=4.483046736485534, longitude=-85.89829886898251,radius=50),
                Checkpoint(latitude=4.329411363655353, longitude=-92.71681895714882,radius=50),
                Checkpoint(latitude=21.169951623924405, longitude=-125.4226017529291,radius=50),
                Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1990.0),
                Checkpoint(latitude=-10.87087353243254, longitude=176.29833966664899,radius=50),
                Checkpoint(latitude=-14.544656972551849, longitude= 156.51634646127724, radius=50),
                
                Checkpoint(latitude=-10.046146579226453, longitude=143.8149413578435, radius=50),
                Checkpoint(latitude=-10.129639677271195, longitude=141.12707427918457, radius=50),

                Checkpoint(latitude=-9.767229959907766, longitude=129.13605663448448, radius=50),
                Checkpoint(latitude=-21.78615493499045, longitude=106.48197686273187, radius=50),
                Checkpoint(latitude=-15.668984, longitude=77.674694, radius=1190.0),
                Checkpoint(latitude=-15.21712273073814, longitude=72.29546916338663, radius=50),
                Checkpoint(latitude=-46.062101844576055, longitude= 8.30307281868545, radius=50),
                Checkpoint(latitude=51.46837407604826, longitude=-39.2634677797800, radius=50),

                Checkpoint(
                    latitude=config.start.latitude,
                    longitude=config.start.longitude,
                    radius=5,
            ),
        ]

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: Callable,
        world_map: Callable,
    ) -> Instructions:
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            Method to query the weather forecast for the next 5 days.
            Example:
            current_position_forecast = forecast(
                latitudes=latitude, longitudes=longitude, times=0
            )
        world_map:
            Method to query map of the world: 1 for sea, 0 for land.
            Example:
            current_position_terrain = world_map(
                latitudes=latitude, longitudes=longitude
            )

        Returns
        -------
        instructions:
            A set of instructions for the ship. This can be:
            - a Location to go to
            - a Heading to point to
            - a Vector to follow
            - a number of degrees to turn Left
            - a number of degrees to turn Right

            Optionally, a sail value between 0 and 1 can be set.
        """
        # Initialize the instructions
        instructions = Instructions()

        # TODO: Remove this, it's only for testing =================
        current_position_forecast = forecast(
            latitudes=latitude, longitudes=longitude, times=0
        )
        current_position_terrain = world_map(latitudes=latitude, longitudes=longitude)
        # ===========================================================

        # Go through all checkpoints and find the next one to reach
        for ch in self.course:
            # Compute the distance to the checkpoint
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            # Consider slowing down if the checkpoint is close
            jump = dt * np.linalg.norm(speed)
            if dist < 2.0 * ch.radius + jump:
                instructions.sail = min(ch.radius / jump, 1)
            else:
                instructions.sail = 1.0
            # Check if the checkpoint has been reached
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break

        return instructions

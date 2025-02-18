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
        self.team = "PyCon Taiwan"  # This is your team name
        # This is the course that the ship has to follow
        # self.course = []
        self.course = [
            # France
            Checkpoint(latitude=43.797109, longitude=-11.264905, radius=50),

            # France West South
            # Checkpoint(latitude=17.999811, longitude=-29.908577, radius=50),

            # Brazil East
            # Checkpoint(latitude=-11.441808, longitude=-29.660252, radius=50),

            # Argentina South
            # Checkpoint(latitude=-61.025125, longitude=-63.240264, radius=50),

            # Panama
            Checkpoint(latitude=20.3477869, longitude=-70.4968647, radius=50),
            Checkpoint(latitude=20.3477869, longitude=-73.4968647, radius=50),
            Checkpoint(latitude=18, longitude=-75, radius=50),
            Checkpoint(latitude=9.36, longitude=-80.013, radius=50),
            Checkpoint(latitude=9.11595, longitude=-79.70804, radius=50),
            Checkpoint(latitude=8.8, longitude=-79.5, radius=50),
            Checkpoint(latitude=3, longitude=-79.5, radius=50),

            # Check point 1
            Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1990.0),

            # South of NZ
            # Checkpoint(latitude=-62.052286, longitude=169.214572, radius=50.0),
            # North of NZ
            Checkpoint(latitude=-31.3536, longitude=-195.8203, radius=50.0),
            Checkpoint(latitude=-48.8068, longitude=-210.5859375, radius=50.0),

            # South of India (very far)
            # Check point 2
            Checkpoint(latitude=-15.668984, longitude=77.674694, radius=1190.0),

            # South of Africa
            Checkpoint(latitude=-39.438937, longitude=19.836265, radius=50.0),

            # West of Africa
            Checkpoint(latitude=14.881699, longitude=-21.024326, radius=50.0),

            # West of Spain (a bit far)
            Checkpoint(latitude=44.076538, longitude=-18.292936, radius=50.0),

            # Start.
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=0,
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
        #current_position_forecast = forecast(
        #    latitudes=latitude, longitudes=longitude, times=0
        #)
        #current_position_terrain = world_map(latitudes=latitude, longitudes=longitude)
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

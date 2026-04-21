# complete your tasks in this file
import sys
import unittest
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10 ** 6)


@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float


@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str  # "ocean","mountains","forest","other"


@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float


region_conditions = [
    RegionCondition(Region(GlobeRect(34.90, 35.80, -121.35, -119.47), "San Luis Obispo County", "mountains"), 2013,
                    275710, 1776510),
    RegionCondition(Region(GlobeRect(18.9, 22.2, 154.8, 160.2), "Hawaii State", "ocean"), 2020, 1455270, 17100000),
    RegionCondition(Region(GlobeRect(40.5, 45.02, 71.86, 79.76), "New York State", "mountains"), 2025, 20002430,
                    305070000),
    RegionCondition(Region(GlobeRect(4.6, 4.8, 74, 74.2), "Bogota, Colombia", "other"), 2017, 8080730, 11421720)]




def emissions_per_capita(rc: RegionCondition) -> float:
    """
    Calculates the rate of greenhouse gas emissions generated per person per year.

    Parameters:
        - rc (RegionCondition): A valid RegionCondition object

    Returns:
        - float: The rate of greenhouse gas emissions that are created by the given region.
        If the population of the region is 0 returns 0.

    Example:
        emissions_per_capita(RegionCondition(Region(GlobeRect(10, 20,170,-170), "Test", "ocean"), 2020,10000,20000))
        will return 2
    """

    if type(rc) != RegionCondition:
        raise TypeError("Invalid input")
    if rc.pop == 0:
        return 0
    elif rc.pop < 0:
        raise ValueError("Invalid population size")
    else:
        return rc.ghg_rate / rc.pop


def area(gr: GlobeRect) -> float:
    """
    Calculates the surface area of a region of the earth.

    Parameters:
        - gr (GlobeRect): A valid GlobeRect object

    Returns:
        - float: The surface area in km^2 formed by the coordinates of the input.

    Example:
        area(GlobeRect(10, 20,170,-170))
        will return approximately 2390891.090078632
    """

    if type(gr) != GlobeRect:
        raise TypeError("Invalid input")
    if gr.hi_lat > 90 or gr.hi_lat < -90 or gr.lo_lat > 90 or gr.lo_lat < -90 or gr.east_long > 180 or gr.east_long < -180 or gr.west_long > 180 or gr.west_long < -180:
        raise ValueError("Invalid coordinates")
    longitude = gr.east_long - gr.west_long
    if longitude < 0:
        longitude += 360
    return (6378.1 ** 2) * math.radians(longitude) * abs(
        math.sin(math.radians(gr.hi_lat)) - math.sin(math.radians(gr.lo_lat)))


def emissions_per_square_km(rc: RegionCondition) -> float:
    """
    Calculates the rate that greenhouse gas emissions are generated per square km per year.

    Inputs:
        - rc (RegionCondition)

    Outputs:
        - float

    Example:
        emissions_per_square_km(RegionCondition(Region(GlobeRect(10, 20,170,-170), "Test", "ocean"), 2020,10000,20000))
        will return approximately 0.008365081990975272
    """
    if type(rc) != RegionCondition:
        raise TypeError("Invalid input")
    return rc.ghg_rate / area(rc.region.rect)


def densest(rc_list: list[RegionCondition]) -> str:
    """
    Finds and returns the name of the region in the list of RegionConditions with the highest population density.

    Inputs:
        - rc_list (list[RegionCondition]) A list of RegionCondition objects

    Outputs:
        - str: The name of the region with the highest population density.

    Example:
        densest(region_conditions)
        will return "Bogota, Colombia"
    """

    if len(rc_list) == 0:
        raise TypeError("Invalid input")

    def density_helper(rc_list: list[RegionCondition]) -> RegionCondition:

        if len(rc_list) == 1:
            return rc_list[0]

        most_dense = density_helper(rc_list[1:])

        if rc_list[0].pop / area(rc_list[0].region.rect) > most_dense.pop / area(most_dense.region.rect):
            return rc_list[0]
        else:
            return most_dense

    return density_helper(rc_list).region.name


def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    """
    Projects the values of a regions population and greenhouse gas emission rates .

    Inputs:
        - rc (RegionCondition) The original regions condition

        - years (int) the amount of years later to project

    Outputs:
        - RegionCondition: A new RegionCondition object with the projected data stored within.

    Example:
        project_condition(RegionCondition(Region(GlobeRect(10, 20,170,-170), "Test", "ocean"), 2020,10000,20000))
        returns RegionCondition(Region(GlobeRect(10, 20,170,-170), "Test", "ocean"),2025,10005,20010)
    """

    if type(rc) != RegionCondition or type(years) != int:
        raise TypeError("Invalid input")
    if years <= 0:
        raise ValueError("Invalid year amount")

    def scale_rc(rc: RegionCondition, scale: float, years: int) -> RegionCondition:
        new_pop = round(rc.pop * (scale ** years))
        emission_scale = new_pop/rc.pop
        return RegionCondition(rc.region, rc.year + years, new_pop,
                               rc.ghg_rate * emission_scale)

    if rc.region.terrain == "ocean":
        return scale_rc(rc, 1.0001, years)

    elif rc.region.terrain == "mountains":
        return scale_rc(rc, 1.0005, years)

    elif rc.region.terrain == "forest":
        return scale_rc(rc, 0.99999, years)

    elif rc.region.terrain == "other":
        return scale_rc(rc, 1.0003, years)

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
                    275713, 1776511.0),
    RegionCondition(Region(GlobeRect(18.9, 22.2, 154.8, 160.2), "Hawaii State", "ocean"), 2020, 1455271, 17100000),
    RegionCondition(Region(GlobeRect(40.5, 45.02, 71.86, 79.76), "New York State", "mountains"), 2025, 20002427,
                    305070000),
    RegionCondition(Region(GlobeRect(4.6, 4.8, 74, 74.2), "Bogota, Colombia", "other"), 2017, 8080734, 11421724.32)]


def emissions_per_capita(rc: RegionCondition) -> float:
    if rc.pop == 0:
        return 0
    else:
        return rc.ghg_rate / rc.pop


def area(gr: GlobeRect) -> float:
    longitude = gr.east_long - gr.west_long
    if longitude < 0:
        longitude += 360
    return (6378.1 ** 2) * longitude * abs(gr.hi_lat - gr.lo_lat)


def emissions_per_square_km(rc: RegionCondition) -> float:
    return rc.ghg_rate / area(rc.region.rect)


def densest(rc_list: list[RegionCondition]) -> str:


    def density_helper(rc_list: list[RegionCondition]) -> RegionCondition:

        if len(rc_list) == 1:
            return rc_list[0]

        most_dense = density_helper(rc_list[:1])


        if rc_list[0].pop / area(rc_list[0].region.rect) > most_dense.pop/area(most_dense.region.rect):
            return rc_list[0]
        else:
            return most_dense

    return density_helper(rc_list).region.name


def project_condition(rc: RegionCondition, years: int) -> RegionCondition:

    def scale_rc(rc: RegionCondition, scale: float, years: int) -> RegionCondition:
        return RegionCondition(rc.region, rc.year+years, math.ceil(rc.pop*(scale**years)), rc.ghg_rate*(scale**years))

    if rc.region.terrain == "ocean":
        return scale_rc(rc, 1.0001, years)

    elif rc.region.terrain == "mountains":
        return scale_rc(rc, 1.0005, years)

    elif rc.region.terrain == "forest":
        return scale_rc(rc, 0.99999, years)

    elif rc.region.terrain == "other":
        return scale_rc(rc, 1.0003, years)

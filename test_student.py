import unittest

import proj1
from proj1 import *


# proj1.py should contain your data class and function definitions
# these do not contribute positivly to your grade.
# but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.test_rect = proj1.GlobeRect(10, 20,170,-170)
        self.test_region = proj1.Region(self.test_rect, "Test", "ocean")
        self.test_region_conditions = proj1.RegionCondition(self.test_region, 2020,10000,20000)

    def test_emmisions_per_capita(self):
        expected = 2
        result = proj1.emissions_per_capita(self.test_region_conditions)
        self.assertEqual(result,expected)

    def test_area(self):
        result = proj1.area(self.test_rect)

        expected = (6378.1 **2) * math.radians(20) * abs(math.sin(math.radians(20))-math.sin(math.radians(10)))
        self.assertAlmostEqual(result,expected,3)

    def test_emissions_per_square_km(self):
        result = proj1.emissions_per_square_km(self.test_region_conditions)
        expected = self.test_region_conditions.ghg_rate / proj1.area(self.test_rect)

        self.assertAlmostEqual(result,expected,9)

    def test_densest(self):
        result = proj1.densest(proj1.region_conditions)
        expected = "Bogota, Colombia"
        self.assertEqual(result, expected)

    def test_project_condition(self):
        result_condition = proj1.project_condition(self.test_region_conditions,5)
        expected_condition = RegionCondition(self.test_region,2025,10005,20010)
        self.assertEqual(result_condition,expected_condition)
if __name__ == '__main__':
    unittest.main()

import unittest
import math

from core.location.ObjectLocation import Location, ObjectLocation, NamedLocation


class LocationTestCase(unittest.TestCase):
    def test_location(self):
        _latitude = Location(degree=40, minute=42, second=51, locationType=Location.LATITUDE)
        _longitude = Location(degree=-74, minute=0, second=21, locationType=Location.LONGITUDE)
        _nyc = ObjectLocation(longitude=_longitude, latitude=_latitude, height=0)
        self.assertEqual(math.isclose(_nyc.longitude.toDecimal(), -74.00583333, abs_tol=0.01), True)
        self.assertEqual(math.isclose(_nyc.latitude.toDecimal(), 40.714, abs_tol=0.01), True)

    def test_named_location(self):
        _latitude = Location(degree=40, minute=42, second=51, locationType=Location.LATITUDE)
        _longitude = Location(degree=-74, minute=0, second=21, locationType=Location.LONGITUDE)
        _nLoc = NamedLocation(longitude=_longitude, latitude=_latitude, height=0, name='nyc')
        self.assertEqual(_nLoc.name, 'nyc')
        self.assertEqual(math.isclose(_nLoc.objectLocation.longitude .toDecimal(), -74.00583333, abs_tol=0.01), True)
        self.assertEqual(math.isclose(_nLoc.objectLocation.latitude.toDecimal(), 40.714, abs_tol=0.01), True)

    def test_add_locations(self):
        _latitude1 = Location(degree=40, minute=42, second=51, locationType=Location.LATITUDE)
        _latitude2 = Location(degree=20, minute=12, second=3, locationType=Location.LATITUDE)
        _newLatitude = _latitude1 + _latitude2
        self.assertEqual(_newLatitude.degree, 60)
        self.assertEqual(_newLatitude.minute, 54)
        self.assertEqual(_newLatitude.second, 54)

        _latitude3 = Location(degree=30, minute=20, second=20, locationType=Location.LATITUDE)
        _newLatitude1 = _latitude1 + _latitude3
        self.assertEqual(_newLatitude1.degree, 71)
        self.assertEqual(_newLatitude1.minute, 3)
        self.assertEqual(_newLatitude1.second, 11)

        _latitude4 = Location(degree=90, minute=20, second=20, locationType=Location.LATITUDE)
        _newLatitude2 = _latitude4 + _latitude3
        self.assertEqual(_newLatitude2.second, 40)
        self.assertEqual(_newLatitude2.minute, 40)
        self.assertEqual(_newLatitude2.degree, 30)

        _longitude1 = Location(degree=74, minute=0, second=21, locationType=Location.LONGITUDE)
        _longitude2 = Location(degree=120, minute=0, second=21, locationType=Location.LONGITUDE)
        _longitude3 = _longitude2 + _longitude1
        self.assertEqual(_longitude3.second, 42)
        self.assertEqual(_longitude3.minute, 0)
        self.assertEqual(_longitude3.degree, 14)


if __name__ == '__main__':
    unittest.main()

import unittest

from core.location.ObjectLocation import Location, ObjectLocation, NamedLocation


class LocationTestCase(unittest.TestCase):
    def test_location(self):
        _longitude = Location(degree=40, minute=42, second=51)
        _latitude = Location(degree=74, minute=0, second=21)
        _nyc = ObjectLocation(longitude=_longitude, latitude=_latitude, height=0)
        self.assertEqual(_nyc, False)


if __name__ == '__main__':
    unittest.main()

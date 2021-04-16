import json
import math

from utils.jsonutils import CustomEncoder


class Location:

    LATITUDE: int = 1
    LONGITUDE: int = 2

    _DEGREES = {
        LATITUDE: 90,
        LONGITUDE: 180
    }

    def __init__(self, degree: float, minute: float, second: float, locationType: int):
        self._degree = degree
        self._minute = minute
        self._second = second
        self._locationType = locationType

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, value: float):
        self._degree = value

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value: float):
        self._minute = value

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value: float):
        self._second = value

    @property
    def locationType(self):
        return self._locationType

    @locationType.setter
    def locationType(self, value: int):
        self._locationType = value

    def _copy(self):
        _newObj = Location(degree=self.degree, minute=self.minute, second=self.second,
                           locationType=self.locationType)
        return _newObj

    def _addDegrees(self, degrees: float):
        _newDegree = self.degree + degrees
        if _newDegree > self._DEGREES[self.locationType]:
            self.degree = _newDegree - self._DEGREES[self.locationType]
        else:
            self.degree += degrees

    def _addMinutes(self, minutes: float):
        if self.minute + minutes > 60:
            self._addDegrees(degrees=1)
            self.minute = self.minute + minutes - 60
        else:
            self.minute += minutes

    def _addSeconds(self, seconds: float):
        if self.second + seconds > 60:
            self._addMinutes(minutes=1)
            self.second = self.second + seconds - 60
        else:
            self.second += seconds

    def __add__(self, other):
        assert isinstance(other, type(self))
        assert self.locationType == other.locationType
        assert other.second >= 0
        assert other.minute >= 0

        _newObj = self._copy()
        _newObj._addSeconds(other.second)
        _newObj._addMinutes(other.minute)
        _newObj._addDegrees(other.degree)

        return _newObj

    def toDecimal(self):
        _sign = self.degree/math.fabs(self.degree)
        return _sign * (math.fabs(self.degree) + ((self.minute * 60.0) + self.second)/3600.0)

    def __repr__(self):
        return f'{type(self)}:[{self.degree},{self.minute},{self.second}]'

    def __str__(self):
        return f'[{self.degree},{self.minute},{self.second}]'


class ObjectLocation:

    def __init__(self, longitude: Location, latitude: Location, height: float):
        self._latitude: Location = latitude
        self._longitude: Location = longitude
        self._height: float = height

    @property
    def latitude(self) -> Location:
        return self._latitude

    @property
    def longitude(self) -> Location:
        return self._longitude

    @property
    def height(self) -> float:
        return self._height

    def __repr__(self) -> str:
        return f'{type(self)}[{self.longitude},{self.latitude},{self.height}]'

    def x_direction(self) -> tuple:
        return (-1, 'WEST') if self.longitude.degree < 0 else (1, 'EAST')

    def y_direction(self) -> tuple:
        return (-1, 'SOUTH') if self.latitude.degree < 0 else (1, 'NORTH')

    def toJson(self) -> str:
        return json.dumps({'x': self.longitude, 'y': self.latitude, 'z': self.height},
                          cls=CustomEncoder)


class NamedLocation:

    def __init__(self, longitude: Location, latitude: Location, height: float, name: str):
        self._objectLocation: ObjectLocation = ObjectLocation(longitude=longitude,
                                                              latitude=latitude,
                                                              height=height)
        self._name = name

    @property
    def objectLocation(self) -> ObjectLocation:
        return self._objectLocation

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self):
        _ol = self._objectLocation
        return f'{type(self)}[{self._name}:[{_ol.longitude},{_ol.latitude},{_ol.height}]'

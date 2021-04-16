import json

from utils.jsonutils import CustomEncoder


class Location:

    def __init__(self, degree: float, minute: float, second: float):
        self._degree = degree
        self._minute = minute
        self._second = second

    @property
    def degree(self):
        return self._degree

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    def toDecimal(self):
        return self.degree + ((self.minute * 60.0) + self.second)/3600.0

    def __repr__(self):
        return f'{type(self):[{self.degree},{self.minute},{self.second}]}'

    def __str__(self):
        return f'[{self.degree},{self.minute},{self.second}]'


class ObjectLocation:

    def __init__(self, longitude: Location, latitude: Location, height: Location):
        self._latitude = latitude
        self._longitude = longitude
        self._height = height

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def height(self):
        return self._height

    def __repr__(self):
        return f'{type(self)}[{self.longitude},{self.latitude},{self.height}]'

    def x_direction(self):
        return (-1, 'WEST') if self.longitude.degree < 0 else (1, 'EAST')

    def y_direction(self) -> tuple:
        return (-1, 'SOUTH') if self.latitude.degree < 0 else (1, 'NORTH')

    def toJson(self):
        return json.dumps({'x': self.longitude, 'y': self.latitude, 'z': self.height},
                          cls=CustomEncoder)


class NamedLocation:

    def __init__(self, longitude: Location, latitude: Location, height: Location, name: str):
        self._objectLocation: ObjectLocation = ObjectLocation(longitude=longitude,
                                                              latitude=latitude,
                                                              height=height)
        self._name = name

    def __repr__(self):
        _ol = self._objectLocation
        return f'{type(self)}[{self._name}:[{_ol.longitude},{_ol.latitude},{_ol.height}]'

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import warnings

from KicadModTree.util.kicad_util import formatFloat


class Point2D(object):
    r"""Representation of a 2D Point in space

    :Example:

    >>> from KicadModTree import *
    >>> Point2D(0, 0)
    >>> Point2D([0, 0])
    >>> Point2D((0, 0))
    >>> Point2D({'x': 0, 'y':0})
    >>> Point2D(Point2D(0, 0))
    """
    def __init__(self, coordinates=None, y=None):
        # parse constructor
        if coordinates is None:
            coordinates = {}
        elif type(coordinates) in [int, float]:
            if y is not None:
                coordinates = [coordinates, y]
            else:
                raise TypeError('you have to give x and y coordinate')
        elif isinstance(coordinates, Point2D):
            # convert Point2D as well as Point3D to dict
            coordinates = coordinates.__dict__()

        # parse points with format: Point2D({'x':0, 'y':0})
        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0.))
            self.y = float(coordinates.get('y', 0.))
            return

        # parse points with format: Point2D([0, 0]) or Point2D((0, 0))
        if type(coordinates) in [list, tuple]:
            if len(coordinates) == 2:
                self.x = float(coordinates[0])
                self.y = float(coordinates[1])
                return
            else:
                raise TypeError('invalid list size (2 elements expected)')

        raise TypeError('invalid parameters given')

    def round_to(self, base):
        r"""Round to a specific base (like it's required for a grid)

        :param base: base we want to round to
        :return: rounded point

        >>> from KicadModTree import *
        >>> p = Point2D(0.1234, 0.5678).roundTo(0.01)
        """
        if base == 0:
            return self

        return Point2D({'x': round(self.x / base) * base,
                        'y': round(self.y / base) * base})

    @staticmethod
    def __arithmetic_parse(value):
        if isinstance(value, Point2D):
            return value
        elif type(value) in [int, float]:
            return Point2D([value, value])
        else:
            return Point2D(value)

    def __add__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x + other.x,
                        'y': self.y + other.y})

    def __sub__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x - other.x,
                        'y': self.y - other.y})

    def __mul__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x * other.x,
                        'y': self.y * other.y})

    def __div__(self, value):
        other = Point2D.__arithmetic_parse(value)

        return Point2D({'x': self.x / other.x,
                        'y': self.y / other.y})

    def __truediv__(self, obj):
        return self.__div__(obj)

    def __dict__(self):
        return {'x': self.x, 'y': self.y}

    def render(self, formatcode):
        warnings.warn(
            "render is deprecated, read values directly instead",
            DeprecationWarning
        )
        return formatcode.format(x=formatFloat(self.x),
                                 y=formatFloat(self.y))

    def __repr__(self):
        return "Point2D (x={x}, y={y})".format(**self.__dict__())

    def __str__(self):
        return "(x={x}, y={y})".format(**self.__dict__())


class Point3D(Point2D):
    r"""Representation of a 3D Point in space

    :Example:

    >>> from KicadModTree import *
    >>> Point3D(0, 0, 0)
    >>> Point3D([0, 0, 0])
    >>> Point3D((0, 0, 0))
    >>> Point3D({'x': 0, 'y':0, 'z':0})
    >>> Point3D(Point2D(0, 0))
    >>> Point3D(Point3D(0, 0, 0))
    """

    def __init__(self, coordinates=None, y=None, z=None):
        # we don't need a super constructor here

        # parse constructor
        if coordinates is None:
            coordinates = {}
        elif type(coordinates) in [int, float]:
            if y is not None:
                if z is not None:
                    coordinates = [coordinates, y, z]
                else:
                    coordinates = [coordinates, y]
            else:
                raise TypeError('you have to give at least x and y coordinate')
        elif isinstance(coordinates, Point2D):
            # convert Point2D as well as Point3D to dict
            coordinates = coordinates.__dict__()

        # parse points with format: Point2D({'x':0, 'y':0})
        if type(coordinates) is dict:
            self.x = float(coordinates.get('x', 0.))
            self.y = float(coordinates.get('y', 0.))
            self.z = float(coordinates.get('z', 0.))
            return

        # parse points with format: Point3D([0, 0]), Point3D([0, 0, 0]) or Point3D((0, 0)), Point3D((0, 0, 0))
        if type(coordinates) in [list, tuple]:
            if len(coordinates) >= 2:
                self.x = float(coordinates[0])
                self.y = float(coordinates[1])
            else:
                raise TypeError('invalid list size (to small)')

            if len(coordinates) == 3:
                self.z = float(coordinates[2])
            else:
                self.z = 0.

            if len(coordinates) > 3:
                raise TypeError('invalid list size (to big)')

        else:
            raise TypeError('dict or list type required')

    def round_to(self, base):
        r"""Round to a specific base (like it's required for a grid)

        :param base: base we want to round to
        :return: rounded point

        >>> from KicadModTree import *
        >>> p = Point3D(0.123, 0.456, 0.789).roundTo(0.01)
        """
        if base == 0:
            return self

        return Point3D({'x': round(self.x / base) * base,
                        'y': round(self.y / base) * base,
                        'z': round(self.z / base) * base})

    @staticmethod
    def __arithmetic_parse(value):
        if isinstance(value, Point3D):
            return value
        elif type(value) in [int, float]:
            return Point3D([value, value, value])
        else:
            return Point3D(value)

    def __add__(self, value):
        other = Point3D.__arithmetic_parse(value)

        return Point3D({'x': self.x + other.x,
                        'y': self.y + other.y,
                        'z': self.z + other.z})

    def __sub__(self, value):
        other = Point3D.__arithmetic_parse(value)

        return Point3D({'x': self.x - other.x,
                        'y': self.y - other.y,
                        'z': self.z - other.z})

    def __mul__(self, value):
        other = Point3D.__arithmetic_parse(value)

        return Point3D({'x': self.x * other.x,
                        'y': self.y * other.y,
                        'z': self.z * other.z})

    def __div__(self, value):
        other = Point3D.__arithmetic_parse(value)

        return Point3D({'x': self.x / other.x,
                        'y': self.y / other.y,
                        'z': self.z / other.z})

    def __truediv__(self, obj):
        return self.__div__(obj)

    def __dict__(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def render(self, formatcode):
        warnings.warn(
            "render is deprecated, read values directly instead",
            DeprecationWarning
        )
        return formatcode.format(x=formatFloat(self.x),
                                 y=formatFloat(self.y),
                                 z=formatFloat(self.z))

    def __repr__(self):
        return "Point3D (x={x}, y={y}, z={z})".format(**self.__dict__())

    def __str__(self):
        return "(x={x}, y={y}, z={z})".format(**self.__dict__())


class Point(Point3D):
    def __init__(self, coordinates=None, y=None, z=None):
        Point3D.__init__(self, coordinates, y, z)
        warnings.warn(
            "Point is deprecated, use Point2D or Point3D instead",
            DeprecationWarning
        )

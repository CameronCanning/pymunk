__docformat__ = "reStructuredText"

from typing import Any, List, Sequence, Type

from .vec2d import Vec2d


class ContactPoint(object):
    """Contains information about a contact point.

    point_a and point_b are the contact position on the surface of each shape.

    distance is the penetration distance of the two shapes. Overlapping
    means it will be negative. This value is calculated as
    dot(point2 - point1), normal) and is ignored when you set the
    Arbiter.contact_point_set.
    """

    __slots__ = ("point_a", "point_b", "distance")

    def __init__(
        self, point_a: Sequence[float], point_b: Sequence[float], distance: float
    ) -> None:
        self.point_a = point_a
        self.point_b = point_b
        self.distance = distance

    def __repr__(self) -> str:
        return "ContactPoint(point_a={}, point_b={}, distance={})".format(
            self.point_a, self.point_b, self.distance
        )


class ContactPointSet(object):
    """Contact point sets make getting contact information simpler.

    normal is the normal of the collision

    points is the array of contact points. Can be at most 2 points.
    """

    __slots__ = ("normal", "points")

    def __init__(self, normal: Sequence[float], points: List[ContactPoint]) -> None:
        self.normal = normal
        self.points = points

    def __repr__(self) -> str:
        return "ContactPointSet(normal={}, points={})".format(self.normal, self.points)

    @classmethod
    def _from_cp(cls: Type, _points: Any) -> "ContactPointSet":
        normal = Vec2d._fromcffi(_points.normal)

        points = []
        for i in range(_points.count):
            _p = _points.points[i]
            p = ContactPoint(
                Vec2d._fromcffi(_p.pointA), Vec2d._fromcffi(_p.pointB), _p.distance
            )
            points.append(p)

        return cls(normal, points)

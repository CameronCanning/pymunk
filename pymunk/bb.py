__docformat__ = "reStructuredText"

import copy

from . import _chipmunk_cffi

lib = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi
from ._pickle import PickleMixin
from .vec2d import Vec2d


class BB(PickleMixin, object):
    """Simple bounding box.

    Stored as left, bottom, right, top values.
    """

    _pickle_attrs_init = PickleMixin._pickle_attrs_init + [
        "left",
        "bottom",
        "right",
        "top",
    ]

    def __init__(self, *args) -> None:
        """Create a new instance of a bounding box.

        Can be created with zero size with bb = BB() or with four args defining
        left, bottom, right and top: bb = BB(left, bottom, right, top)
        """
        if len(args) == 0:
            self._bbp = ffi.new("cpBB *")
            self._bb = self._bbp[0]
        elif len(args) == 1:
            self._bb = args[0]
        else:
            self._bbp = ffi.new("cpBB *", args)
            self._bb = self._bbp[0]

    @staticmethod
    def newForCircle(p, r: float) -> "BB":
        """Convenience constructor for making a BB fitting a circle at
        position p with radius r.
        """

        bb_ = lib.cpBBNewForCircle(p, r)
        return BB(bb_)

    def __repr__(self):
        return "BB(%s, %s, %s, %s)" % (self.left, self.bottom, self.right, self.top)

    def __eq__(self, other):
        return (
            self.left == other.left
            and self.bottom == other.bottom
            and self.right == other.right
            and self.top == other.top
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    left = property(lambda self: self._bb.l)
    bottom = property(lambda self: self._bb.b)
    right = property(lambda self: self._bb.r)
    top = property(lambda self: self._bb.t)

    def intersects(self, other: "BB") -> bool:
        """Returns true if the bounding boxes intersect"""
        return bool(lib.cpBBIntersects(self._bb, other._bb))

    def intersects_segment(self, a, b) -> bool:
        """Returns true if the segment defined by endpoints a and b
        intersect this bb."""
        return bool(lib.cpBBIntersectsSegment(self._bb, tuple(a), tuple(b)))

    def contains(self, other: "BB") -> bool:
        """Returns true if bb completley contains the other bb"""
        return bool(lib.cpBBContainsBB(self._bb, other._bb))

    def contains_vect(self, v) -> bool:
        """Returns true if this bb contains the vector v"""
        return bool(lib.cpBBContainsVect(self._bb, tuple(v)))

    def merge(self, other: "BB") -> "BB":
        """Return the minimal bounding box that contains both this bb and the
        other bb
        """
        return BB(lib.cpBBMerge(self._bb, other._bb))

    def expand(self, v) -> "BB":
        """Return the minimal bounding box that contans both this bounding box
        and the vector v
        """
        return BB(lib.cpBBExpand(self._bb, tuple(v)))

    def center(self) -> Vec2d:
        """Return the center"""
        v = lib.cpBBCenter(self._bb)
        return Vec2d(v.x, v.y)

    def area(self) -> float:
        """Return the area"""
        return lib.cpBBArea(self._bb)

    def merged_area(self, other: "BB") -> float:
        """Merges this and other then returns the area of the merged bounding
        box.
        """
        return lib.cpBBMergedArea(self._bb, other._bb)

    def segment_query(self, a, b) -> float:
        """Returns the fraction along the segment query the BB is hit.

        Returns infinity if it doesnt hit
        """
        return lib.cpBBSegmentQuery(self._bb, tuple(a), tuple(b))

    def clamp_vect(self, v) -> Vec2d:
        """Returns a copy of the vector v clamped to the bounding box"""
        v2 = lib.cpBBClampVect(self._bb, tuple(v))
        return Vec2d(v2.x, v2.y)

    '''
    def wrap_vect(self, v):
        """Returns a copy of v wrapped to the bounding box.

        That is, BB(0,0,10,10).wrap_vect((5,5)) == Vec2d._fromcffi(10,10)
        """
        return lib._cpBBWrapVect(self._bb[0], v)
    '''

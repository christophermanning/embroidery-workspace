import math


def distance(point1: tuple[int, int], point2: tuple[int, int]) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def bbox_contains(
    bbox1: tuple[int, int, int, int], bbox2: tuple[int, int, int, int]
) -> bool:
    return (
        bbox2[0] >= bbox1[0]
        and bbox2[1] >= bbox1[1]
        and bbox2[2] <= bbox1[2]
        and bbox2[3] <= bbox1[3]
    )

import random
import math
from shapely.geometry import Polygon

def polygon_area(coords):
    """Calculating the area of a polygon using the Gauss method"""
    n = len(coords)
    area = 0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

def generate_polygon(num_points, radius=10):
    """Generate a simple polygon without self-intersections."""
    points = [
        (
            math.cos(2 * math.pi * i / num_points) * random.uniform(0.8, 1) * radius,
            math.sin(2 * math.pi * i / num_points) * random.uniform(0.8, 1) * radius
        )

        for i in range(num_points)
    ]

    # Sort points based on angle from the centroid
    centroid = (
        sum(x for x, y in points) / num_points,
        sum(y for x, y in points) / num_points
    )

    points = sorted(points, key=lambda p: math.atan2(p[1] - centroid[1], p[0] - centroid[0]))

    # Create the polygon
    polygon = Polygon(points)

    if not polygon.is_valid:
        raise ValueError("Generated polygon is invalid")

    return polygon

# Example usage
polygon = generate_polygon(10)
print(f"Generated Polygon: {polygon}")
coords = list(polygon.exterior.coords) 
area = polygon_area(coords)
print(f"The area of polygon: {area:.5f}")

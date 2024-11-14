import random
import math
import time
from shapely.geometry import Polygon, Point


def polygon_area(coords):
    """Calculating the area of a polygon using the Gauss method."""
    n = len(coords)
    area = 0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2


def monte_carlo_area(polygon, num_points):
    """Estimation of the area of a polygon using the Monte Carlo method."""
    min_x, min_y, max_x, max_y = polygon.bounds
    inside_count = 0

    for _ in range(num_points):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        if polygon.contains(Point(x, y)):
            inside_count += 1

    box_area = (max_x - min_x) * (max_y - min_y)
    return box_area * (inside_count / num_points)


def generate_polygon(num_points, radius=10):
    """Generate a simple polygon without self-intersections."""
    points = [
        (
            math.cos(2 * math.pi * i / num_points) * random.uniform(0.8, 1) * radius,
            math.sin(2 * math.pi * i / num_points) * random.uniform(0.8, 1) * radius,
        )
        for i in range(num_points)
    ]

    # Sort points based on angle from the centroid
    centroid = (
        sum(x for x, y in points) / num_points,
        sum(y for x, y in points) / num_points,
    )

    points = sorted(points, key=lambda p: math.atan2(p[1] - centroid[1], p[0] - centroid[0]))
    polygon = Polygon(points)

    if not polygon.is_valid:
        raise ValueError("Generated polygon is invalid")

    return polygon


def find_iterations_for_accuracy(polygon, acceptable_error=0.01, max_iter=1_000_000):
    """Find the minimum number of iterations required to achieve the desired accuracy."""
    true_area = polygon.area
    num_points = 100
    error = float('inf')
    start_time = time.time()

    while error > acceptable_error and num_points <= max_iter:
        estimated_area = monte_carlo_area(polygon, num_points)
        error = abs(estimated_area - true_area) / true_area
        num_points *= 2

    elapsed_time = time.time() - start_time
    return num_points, elapsed_time


if __name__ == "__main__":
    polygon = generate_polygon(100)
    print(f"Generated Polygon: {polygon}")
    
    # Calculate true area using Shapely
    true_area = polygon.area
    print(f"True Area (Shapely): {true_area:.5f}")
    
    # Calculate area using Gauss method
    coords = list(polygon.exterior.coords)
    gauss_area = polygon_area(coords)
    print(f"Area using Gauss method: {gauss_area:.5f}")
    
    # Estimate area using Monte Carlo method
    min_points, execution_time = find_iterations_for_accuracy(polygon, acceptable_error=0.01)
    monte_carlo_estimate = monte_carlo_area(polygon, min_points)
    print(f"\nMonte Carlo Estimate: {monte_carlo_estimate:.5f}")
    print(f"Minimum Points Required: {min_points}")
    print(f"Execution Time: {execution_time:.2f} seconds")

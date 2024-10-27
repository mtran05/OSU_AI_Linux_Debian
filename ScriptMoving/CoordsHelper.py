def interpolate_point(p1, p2, percentage):
    """
    Returns the coordinates of a point that is `percentage`% along the line from p1 to p2.
    
    Parameters:
    - p1: Tuple of (x1, y1) - starting point.
    - p2: Tuple of (x2, y2) - ending point.
    - percentage: Float between 0 and 100 representing the percentage along the path from p1 to p2.

    Returns:
    - (x, y): The interpolated point.
    """
    x1, y1 = p1
    x2, y2 = p2

    # Calculate the interpolated coordinates
    x = x1 + percentage * (x2 - x1)
    y = y1 + percentage * (y2 - y1)

    return x, y
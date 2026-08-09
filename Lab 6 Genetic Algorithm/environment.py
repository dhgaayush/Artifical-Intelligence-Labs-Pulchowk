"""
environment.py

Creates and manages room environments for the
Genetic Algorithm Painter Robot project.
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Room Creation
# ---------------------------------------------------------

def create_empty_room(rows=20, cols=40):
    """
    Create an empty paintable room.

    Parameters
    ----------
    rows : int
        Number of rows.

    cols : int
        Number of columns.

    Returns
    -------
    np.ndarray
        Room filled with zeros.
    """

    return np.zeros((rows, cols), dtype=int)


def create_furnished_room(rows=20, cols=40):
    """
    Create a room containing several rectangular
    furniture obstacles.

    Returns
    -------
    np.ndarray
        Room array.
    """

    room = create_empty_room(rows, cols)

    # Sofa
    room[3:6, 5:10] = 1

    # Table
    room[10:14, 18:24] = 1

    # Cabinet
    room[5:12, 32:35] = 1

    # Chair
    room[15:18, 8:11] = 1

    return room


# ---------------------------------------------------------
# Room Information
# ---------------------------------------------------------

def count_paintable_cells(room):
    """
    Count how many cells can be painted.

    Parameters
    ----------
    room : np.ndarray

    Returns
    -------
    int
    """

    return np.sum(room == 0)


def copy_room(room):
    """
    Return a copy of the room.
    """

    return room.copy()


# ---------------------------------------------------------
# Visualization
# ---------------------------------------------------------

def display_room(room, title="Room"):
    """
    Display the room.

    0 -> White (empty)
    1 -> Black (obstacle)
    2 -> Green (painted)
    """

    plt.figure(figsize=(8, 5))

    plt.imshow(room, cmap="viridis", origin="upper")

    plt.title(title)
    plt.xticks([])
    plt.yticks([])

    plt.show()


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    empty = create_empty_room()

    furnished = create_furnished_room()

    print("Empty room paintable cells:",
          count_paintable_cells(empty))

    print("Furnished room paintable cells:",
          count_paintable_cells(furnished))

    display_room(empty, "Empty Room")

    display_room(furnished, "Furnished Room")
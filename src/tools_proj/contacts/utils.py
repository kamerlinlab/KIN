"""
Useful functions for contact analysis.
"""
import numpy as np

RADIANS_TO_DEGREES = 57.2958


def angle_between_two_vectors(v1, v2):
    """
    Returns the angle in radians between vectors 'v1' and 'v2'.
    """
    v1_u = _unit_vector(v1)
    v2_u = _unit_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return angle * RADIANS_TO_DEGREES


def _unit_vector(vector):
    """
    Returns the unit vector of the vector.
    """
    return vector / np.linalg.norm(vector)


def normal_vector_3_atoms(atom_positions):
    """
    Normal_vector of 3 atoms.
    Can be applied to aromatic rings and guanidinium groups.
    """
    v1 = atom_positions[2] - atom_positions[0]
    v2 = atom_positions[1] - atom_positions[0]
    return np.cross(v1, v2)

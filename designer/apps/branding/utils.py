""" Utility methods """
import re

from django.core.exceptions import ValidationError


def validate_hexadecimal_color(color):
    """
    Returns true if color is a string in the format hexadecimal format
    ex: '#B62168', '#00a2e4'
    Args:
        color: (str) string representing hexadecimal color

    Returns:
        is_valid_hexadecimal_color: (bool) True if `color` is in valid hexadecimal format
    """
    if re.match(r'#[\dA-Fa-f]{6}', color) is None:
        raise ValidationError("Incorrect format. Must follow hexadecimal format (ex. '#B62168' or '#00a2e4')")

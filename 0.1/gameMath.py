

"""
Keeps value inside of specified Boundaries

Parameters:
-----------
value : Any
    The value to be clamped within the range. Must be comparable to `minValue` and `maxValue`.

minValue : Any
    The minimum allowable value. Must be comparable to `value` and `maxValue`.

maxValue : Any
    The maximum allowable value. Must be comparable to `value` and `minValue`.

Returns: Any
    The clamped value, ensuring it is within the range [minValue, maxValue].
"""
def clamp(value, minValue, maxValue):
    return max(minValue, min(value, maxValue))



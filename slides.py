"""Python code specifically for test0.html"""

import re
import cogutil

def tweak_quick_times(line):
    """
    Test times vary: make them more consistent to avoid
    lines changing constantly.
    """
    m = re.search(r"^Ran \d+ tests in 0.00\ds$", line)
    if m:
        line = re.sub(r"in 0.00\ds", "in 0.001s", line)
    m = re.search(r"\d passed in 0.0\ds", line)
    if m:
        line = re.sub(r"in 0.0\ds", "in 0.01s", line)
    return line

def tweak_object_address(line):
    """
    Some lines have object addresses in them, which change
    from run to run.  Make them a constant.
    """
    return re.sub(r"0x1[0-9a-f]{8}\b", "0x1b01dface", line)

cogutil.include_file_default(
    tweaks=[tweak_quick_times, tweak_object_address],
)

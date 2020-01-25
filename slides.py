"""Python code specifically for test0.html"""

import re
import cogutil

def tweak_quick_times(line):
    """
    Test times vary: make them more consistent to avoid
    lines changing constantly.
    """
    m = re.match(r"^Ran \d+ tests in 0.00[01234]s$", line)
    if m:
        line = re.sub(r"in 0.00[01234]s", "in 0.001s", line)
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

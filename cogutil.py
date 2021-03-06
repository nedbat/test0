# Helpers for cogging slides.

import os
import re
import textwrap

import cog
import cagedprompt

def quote_html(s):
    return (s
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\xa0", "&nbsp;")
    )


def clip_long_boring_line(s, l):
    """
    If s is a line with only one character in it, shorten it to length l.
    """
    if len(s) > l and len(set(s)) == 1:
        s = s[:l]
    return s


INCLUDE_FILE_DEFAULTS = dict(
    fname=None,
    show_label=False,
    classes="",
    indir="",
    tweaks=[],
    )

def include_file_default(**kwargs):
    INCLUDE_FILE_DEFAULTS.update(kwargs)

def include_file(
        fname=None,
        start=None, end=None,
        start_has=None, end_has=None,
        start_from=None, end_at=None,
        start_nth=1, end_nth=1,
        line_count=None,
        highlight=None,
        hilite=None,
        section=None,
        show_label=None,
        px=False,
        classes=None,
        number=False,
        incremental=False,
        indent=None,
    ):
    """Include a text file.

    `fname` is read as text, and included in a <pre> tag.

    `highlight` is a list of line numbers to highlight (obsolete).
    `hilite` is a list of substrings of lines to highlight.

    `start` and `end` are the first and last line numbers to show, if provided.
    `start_has` is text that must appear in the start line, to check that the
    file hasn't changed. Similarly for `end_has`.

    `start_from` and `end_at` are substrings of the first and last lines to
    show.  `start_nth` indicates which occurrence of `start_from` to take,
    similarly for `end_nth`.

    `section` is a named section.  If provided, a marked section in the file is extracted
    for display.  Markers for section foobar are "(((foobar))" and "(((end)))".

    If `show_label` is True, add a div with a label, the name of the
    file.  If `show_label` is a string, then show the label if
    `fname` matches the string as a regex.

    If `px` is true, the result is meant for text rather than slides.

    `classes` is a string of extra css classes to add to the <pre> tag.

    If `number` is true, then line numbers will be shown.

    If `incremental` is true, then the "incremental" class should be
    appropriately applied.

    if `indent` is not None, it is the number of spaces to indent the text.

    """
    if fname is None:
        fname = INCLUDE_FILE_DEFAULTS['fname']
    if show_label is None:
        show_label = INCLUDE_FILE_DEFAULTS['show_label']
    if classes is None:
        classes = INCLUDE_FILE_DEFAULTS['classes']
    indir = INCLUDE_FILE_DEFAULTS['indir']

    assert fname is not None, "Need a file name to include!"

    with open(os.path.join(indir, fname)) as f:
        text = f.read()

    lines = text.splitlines()

    tweaks = INCLUDE_FILE_DEFAULTS['tweaks']
    if tweaks:
        tweaked = []
        for line in lines:
            for twfn in tweaks:
                line = twfn(line)
            tweaked.append(line)
        lines = tweaked

    if section:
        assert start_from is None
        assert end_at is None
        assert line_count is None
        start_from = "(((" + section + ")))"
        end_at = "(((end)))"
    if start_from:
        assert start is None
        assert end is None
        start = find_nth(lines, 0, start_from, start_nth)
        if start is None:
            raise Exception("Didn't find {!r} as a start line".format(start_from))
        if end_at:
            end = find_nth(lines, start, end_at, end_nth)
            if end is None:
                raise Exception("Didn't find {!r} as an end line".format(end_at))
        elif line_count is not None:
            end = start + line_count - 1
        if section:
            start += 1
            end -= 1
    else:
        if start is None:
            start = 1
        if end is None:
            end = len(lines)

    if start_has:
        start_line = lines[start-1]
        if start_has not in start_line:
            raise Exception("Didn't find {!r} in the start line: {}:{} {!r}".format(start_has, fname, start, start_line))
    if end_has:
        end_line = lines[end-1]
        if end_has not in end_line:
            raise Exception("Didn't find {!r} in the end line: {}:{} {!r}".format(end_has, fname, end, end_line))

    # Take only the lines we want, and shorten lines that are too long and
    # easily shortened.
    lines = [clip_long_boring_line(l, 60) for l in lines[start-1:end]]

    hilite_nums = []
    if hilite:
        for linenum, line in enumerate(lines):
            if any(h in line for h in hilite):
                hilite_nums.append(linenum)

    text = "\n".join(lines)
    lang = "python" if fname.endswith(".py") else "text"

    if px:
        show_label = False
    elif isinstance(show_label, str):
        show_label = bool(re.search(show_label, fname))
    if show_label:
        if incremental:
            cog.outl("<div class='incremental'>")
            incremental = False
        else:
            cog.outl("<div>")
        cog.outl("<div class='prelabel'>{}</div>".format(fname))
    number_from = start if number else 0
    if incremental:
        classes += " incremental"
    include_code(text, lang=lang, hilite=hilite_nums, px=px, classes=classes, number_from=number_from, indent=indent)
    if show_label:
        cog.outl("</div>")


def find_nth(lines, start, needle, nth):
    indexes = [i for i, l in enumerate(lines[start:], start+1) if needle in l]
    if nth > len(indexes):
        return None
    return indexes[nth-1]


def include_code(text, lang=None, highlight=None, hilite=None, px=False, classes="", number_from=0, indent=None):
    text = textwrap.dedent(text)

    if indent is not None:
        text = textwrap.indent(text, "\xa0" * indent)

    text = "\n".join(l.rstrip() for l in text.splitlines())

    if px:
        cog.outl("<code lang='{}'>".format(lang))
        cog.outl(quote_html(text))
        cog.outl("</code>")
        return

    result = []
    class_attr = lang
    if classes:
        class_attr += " " + classes
    more_attr = ""
    if hilite:
        more_attr += " data-hilite='|{}|'".format("|".join(map(str, hilite)))
    if number_from:
        more_attr += " data-numberfrom='{}'".format(number_from)
    result.append("<pre class='{}'{}>".format(class_attr, more_attr))
    result.append(quote_html(text))
    result.append("</pre>")
    cog.outl("\n".join(result))


def prompt_session(input, command=False, prelude=""):
    output = ""
    if command:
        output += "$ python\n"
    repl_out = cagedprompt.prompt_session(input, banner=command, prelude=prelude)
    # REPL sessions have lone triple-dot lines. Suppress them.
    repl_out = "\n".join('' if l == '... ' else l for l in repl_out.splitlines())
    output += repl_out
    include_code(output, lang="python", classes="console " + INCLUDE_FILE_DEFAULTS['classes'])

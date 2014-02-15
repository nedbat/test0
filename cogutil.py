# Helpers for cogging slides.

import cog
import cagedprompt

def quote_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def include_file(fname, highlight=None, start=None, end=None, section=None, klass=None):
    """Include a text file.

    `fname` is read as text, and included in a <pre> tag.
    
    `highlight` is a list of lines to highlight.
    
    `start` and `end` are the first and last line numbers to show, if provided.

    `section` is a named section.  If provided, a marked section in the file is extracted
    for display.  Markers for section foobar are "(((foobar))" and "(((end)))".

    """
    if fname.endswith(".py"):
        pre_class = "brush: python"
    else:
        pre_class = "brush: plain"
    if highlight:
        pre_class += "; highlight: %r" % (highlight,)
    text = open(fname).read()
    lines = text.split("\n")
    if section:
        assert start is None
        assert end is None
        start_marker = "(((%s)))" % section
        end_marker = "(((end)))"
        start = next(i for i,l in enumerate(lines, 1) if start_marker in l)
        end = next(i for i,l in enumerate(lines[start:], start+1) if end_marker in l)
        start += 1
        end -= 1
    else:
        if start is None:
            start = 1
        if end is None:
            end = len(lines)+1
    lines = lines[start-1:end]

    if start != 1:
        pre_class += "; first-line: %d" % start
    if klass:
        pre_class += "; class-name: %s" % klass

    cog.outl("<pre class='%s'>" % (pre_class,))
    cog.out(quote_html("\n".join(lines)))
    cog.outl("</pre>")

def prompt_session(input):
    output = cagedprompt.prompt_session(input)
    cog.outl("<pre class='brush: python'>")
    cog.outl("$ python")
    cog.out(quote_html(output))
    cog.outl("</pre>")

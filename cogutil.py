# Helpers for cogging slides.

import textwrap

import cog
import cagedprompt

def quote_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def include_file(fname, start=None, end=None, highlight=None, section=None):
    """Include a text file.

    `fname` is read as text, and included in a <pre> tag.

    `highlight` is a list of lines to highlight.

    `start` and `end` are the first and last line numbers to show, if provided.

    `section` is a named section.  If provided, a marked section in the file is extracted
    for display.  Markers for section foobar are "(((foobar))" and "(((end)))".

    """
    with open(fname) as f:
        text = f.read()

    lines = text.splitlines()
    if section:
        assert start is None
        assert end is None
        start_marker = "(((" + section + ")))"
        end_marker = "(((end)))"
        start = next(i for i, l in enumerate(lines, 1) if start_marker in l)
        end = next(i for i, l in enumerate(lines[start:], start+1) if end_marker in l)
        start += 1
        end -= 1
    else:
        if start is None:
            start = 1
        if end is None:
            end = len(lines)

    text = "\n".join(lines[start-1:end])

    lang = "python" if fname.endswith(".py") else "text"
    include_code(text, lang=lang, firstline=start, number=True, show_text=True)

def include_code(text, lang=None, number=False, firstline=1, show_text=False):
    # Put the code in a comment, so we can see it in the HTML while editing.
    if show_text:
        cog.outl("<!--")
        cog.outl(text.replace("-", u"\N{EN DASH}".encode("utf8"))) # Prevent breaking the HTML comment.
        cog.outl("-->")

    text = textwrap.dedent(text)
    import pygments, pygments.lexers, pygments.formatters
    # Because we are omitting the <pre> wrapper, we need spaces to become &nbsp;.
    # This is totally not a public interface...
    import pygments.formatters.html as pfh
    pfh._escape_html_table.update({ord(' '): u'&#xA0;'})

    class CodeHtmlFormatter(pygments.formatters.HtmlFormatter):

        def wrap(self, source, outfile):
            return self._wrap_code(source)

        def _wrap_code(self, source):
            yield 0, '<div class="code {}">'.format(lang)
            for i, t in source:
                if i == 1:
                    # it's a line of formatted code
                    t = '<div class="line">{}&nbsp;</div>\n'.format(t.rstrip())
                yield i, t
            yield 0, '</div>'

    lexer = pygments.lexers.get_lexer_by_name(lang, stripall=True)
    linenos = 'inline' if number else False
    formatter = CodeHtmlFormatter(linenos=linenos, linenostart=firstline, cssclass="source")
    result = pygments.highlight(text, lexer, formatter)
    cog.outl(result)

def prompt_session(input, command=True):
    output = ""
    if command:
        output += "$ python\n"
    output += cagedprompt.prompt_session(input, banner=command)
    include_code(output, lang="pycon", number=False)

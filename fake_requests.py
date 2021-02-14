"""
OK, this is twisty:

This presentation used to use a real stock market API site, but that
site is gone.  It served CSV, which was good for its compactness in
examples.

Rather than look for a new API, I'm faking the API requests.

It's twisty because this fake is used for the "real" code, but then
later we talk about mocking and faking requests for tests.
"""

class FakeResponse:
    def __init__(self, text):
        self.text = text


def get(url):
    return FakeResponse("""\
symbol,something,another,close
HPQ,,,22.09
IBM,,,135.37
""")

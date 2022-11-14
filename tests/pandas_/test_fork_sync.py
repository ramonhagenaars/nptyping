import os
from unittest import TestCase, skipIf
from urllib.request import Request, urlopen


class ForkSyncTest(TestCase):
    @skipIf(os.environ.get("CI"), reason="Only run locally")
    def test_pandas_stubs_fork_is_synchronized(self):
        url = "https://github.com/ramonhagenaars/pandas-stubs/tree/main"
        httprequest = Request(url, headers={"Accept": "text/html"})

        with urlopen(httprequest) as response:
            payload = response.read().decode()
            out_of_sync = "commits behind" in payload

        self.assertFalse(out_of_sync, "The pandas-stubs fork needs to be synchronized")

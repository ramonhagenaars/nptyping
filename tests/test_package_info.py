import os
from unittest import TestCase
from unittest.case import skipIf

import feedparser

from nptyping import __version__


class PackageInfoTest(TestCase):
    @skipIf(os.environ.get("CI"), reason="Only run locally")
    def test_version_bump(self):
        releases = feedparser.parse(
            "https://pypi.org/rss/project/nptyping/releases.xml"
        )
        release_versions = {entry.title for entry in releases.entries}

        self.assertNotIn(__version__, release_versions, "Version bump required")

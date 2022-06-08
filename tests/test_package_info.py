from unittest import TestCase

import feedparser

from nptyping import __version__


class PackageInfoTest(TestCase):
    def test_version_bump(self):
        releases = feedparser.parse(
            "https://pypi.org/rss/project/nptyping/releases.xml"
        )
        release_versions = {entry.title for entry in releases.entries}

        self.assertNotIn(__version__, release_versions, "Version bump required")

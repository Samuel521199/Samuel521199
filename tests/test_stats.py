import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from urllib.error import URLError
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import update_stats as stats


def repo(number, **extra):
    return {"id":number, "name":f"repo-{number}", "owner":{"login":stats.OWNER},
            "private":False, "fork":False, "language":"Python",
            "stargazers_count":0, "forks_count":0, **extra}


class StatisticsTests(unittest.TestCase):
    def test_counts_distinguish_forks_and_unknown_languages(self):
        result = stats.summarize([
            repo(1, stargazers_count=3, forks_count=2),
            repo(2, fork=True, language="Rust", stargazers_count=1),
            repo(3, language=None), repo(4, language="Go")])
        self.assertEqual(result["public_repositories"],4)
        self.assertEqual(result["non_fork_repositories"],3)
        self.assertEqual(result["fork_repositories"],1)
        self.assertEqual(result["primary_languages"],{"Go":1,"Python":1})
        self.assertEqual(result["stars"],4)
        self.assertEqual(result["forks_received"],2)

    def test_pagination_deduplicates_and_excludes_nonpublic_or_other_owner(self):
        page1 = [repo(i) for i in range(100)]
        page2 = [repo(99),repo(100),repo(101,private=True),
                 repo(102,visibility="private"),
                 repo(103,owner={"login":"another-account"})]
        with patch.object(stats,"get_json",side_effect=[page1,page2]) as request:
            result = stats.fetch_repositories()
        self.assertEqual(len(result),101)
        self.assertIn("page=2",request.call_args_list[1].args[0])

    def test_api_failure_keeps_previous_outputs(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root/"data/public-projects.json"
            path.parent.mkdir()
            path.write_text("previous")
            with patch.object(stats,"ROOT",root), patch.object(
                stats,"get_json",side_effect=URLError("unavailable")):
                with self.assertRaises(URLError):
                    stats.main()
            self.assertEqual(path.read_text(),"previous")
            self.assertFalse((root/"assets/stats.svg").exists())

    def test_empty_inventory_is_not_published_as_zero(self):
        with patch.object(stats,"fetch_repositories",return_value=[]):
            with self.assertRaisesRegex(ValueError,"Empty public inventory"):
                stats.main()

    def test_new_languages_expand_layout_and_xml_is_escaped(self):
        repos = [repo(i,language=f"Lang<&{i}") for i in range(14)]
        summary = stats.summarize(repos)
        for compact in (False,True):
            xml = ET.fromstring(stats.dashboard(repos,summary,"2026-10-20 12:00",compact))
            height = int(xml.attrib["height"])
            for item in xml.iter("{http://www.w3.org/2000/svg}text"):
                self.assertLess(float(item.attrib["y"]),height)
            self.assertIn("Lang<&0","".join(xml.itertext()))


if __name__ == "__main__":
    unittest.main()

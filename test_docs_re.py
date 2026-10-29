"""Verify educational RE documentation links and the editable BPMN example."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
ENTRY_POINTS = [
    ROOT / "README.md",
    ROOT / "README.de.md",
    *sorted(DOCS.glob("*.md")),
    DOCS / "archiv" / "README.md",
]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
DI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"


class RequirementsDocumentationTests(unittest.TestCase):
    def test_all_re_reference_links_resolve(self):
        for path in ENTRY_POINTS:
            with self.subTest(source=str(path.relative_to(ROOT))):
                self.assertTrue(path.is_file())
                for target in LINK.findall(path.read_text(encoding="utf-8")):
                    if target.startswith(("http:", "https:", "mailto:", "#")):
                        continue
                    cleaned = target.split("#", 1)[0].split("?", 1)[0]
                    if cleaned:
                        self.assertTrue((path.parent / cleaned).is_file(),
                                        f"Broken link in {path}: {target}")

    def test_bpmn_example_is_valid_xml_with_two_lanes_and_exclusive_gateways(self):
        path = DOCS / "RE-Beispiel-Spiel-abbrechen.bpmn"
        tree = ET.parse(path)
        root = tree.getroot()
        process = root.find(f".//{{{BPMN_NS}}}process")
        self.assertIsNotNone(process)
        self.assertEqual(process.attrib["isExecutable"], "false")
        lanes = root.findall(f".//{{{BPMN_NS}}}lane")
        self.assertEqual({lane.attrib.get("name") for lane in lanes},
                         {"Instructor", "Syzeteo"})
        self.assertGreaterEqual(len(root.findall(
            f".//{{{BPMN_NS}}}exclusiveGateway")), 2)
        nodes = {
            node.attrib["id"] for node in process.iter()
            if node.tag.rsplit("}", 1)[-1] in {
                "startEvent", "endEvent", "task", "userTask",
                "exclusiveGateway"}
        }
        flows = root.findall(f".//{{{BPMN_NS}}}sequenceFlow")
        self.assertGreaterEqual(len(flows), 10)
        for flow in flows:
            self.assertIn(flow.attrib["sourceRef"], nodes)
            self.assertIn(flow.attrib["targetRef"], nodes)
        diagram = root.findall(f".//{{{DI_NS}}}BPMNDiagram")
        self.assertTrue(diagram)

    def test_obsolete_tdd_working_documents_are_not_cited_as_current(self):
        removed_names = (
            "Syzeteo-Akzeptanztests-TDD-DE.md",
            "Syzeteo-TDD-US10-DE.md",
            "Syzeteo-TDD-US21-DE.md",
            "Syzeteo-TDD-Phase2-US24-DE.md",
            "Syzeteo-Testabdeckung-Review-DE.md",
            "Syzeteo-TDD-Kriterien-Governance-DE.md",
            "Syzeteo-TDD-Phase3-Governance-DE.md",
        )
        for path in ENTRY_POINTS:
            content = path.read_text(encoding="utf-8")
            for name in removed_names:
                self.assertNotIn(name, content,
                                 f"Outdated reference in {path}: {name}")


if __name__ == "__main__":
    unittest.main()

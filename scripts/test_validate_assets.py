"""Regression tests for intentional SVG and link defects."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import validate_assets as v

SVG = 'http://www.w3.org/2000/svg'

class SvgTests(unittest.TestCase):
    def check(self, body='', attrs='viewBox="0 0 10 10"'):
        v.errors.clear()
        v.validate_svg(f'<svg xmlns="{SVG}" {attrs}>{body}</svg>'.encode(), 'fixture')
        return '\n'.join(v.errors)

    def test_valid(self):
        self.assertEqual(self.check('<rect width="2" height="2"/>'), '')

    def test_malformed(self):
        self.assertIn('XML parse error', self.check('<rect>'))

    def test_duplicate_id(self):
        self.assertIn('duplicate ID', self.check('<g id="a"/><g id="a"/>'))

    def test_missing_reference(self):
        self.assertIn('unresolved SVG reference', self.check('<rect fill="url(#missing)"/>'))

    def test_invalid_viewbox(self):
        self.assertIn('invalid viewBox', self.check(attrs='viewBox="0 0 NaN 10"'))

    def test_active_element(self):
        self.assertIn('active element', self.check('<script/>'))

    def test_event_attribute(self):
        self.assertIn('event attribute', self.check('<g onclick="x()"/>'))

    def test_external_resource(self):
        self.assertIn('external SVG resource', self.check('<rect fill="url(https://example.com/a.svg)"/>'))

    def test_external_href(self):
        self.assertIn('unexpected external reference', self.check('<image href="https://example.com/a.svg"/>'))

    def test_invalid_embedded_data(self):
        self.assertIn('invalid base64', self.check('<image href="data:image/svg+xml;base64,!!!"/>'))

    def test_dtd(self):
        v.errors.clear()
        v.validate_svg(b'<!DOCTYPE svg><svg/>', 'fixture')
        self.assertIn('DTD or entity declaration', '\n'.join(v.errors))

    def test_local_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'README.md'
            page.write_text('# Example')
            with patch.object(v, 'ROOT', root):
                v.errors.clear()
                v.validate_link(page, 'README.md')
                self.assertEqual(v.errors, [])
                v.validate_link(page, 'missing.svg')
                self.assertIn('broken local link', '\n'.join(v.errors))

if __name__ == '__main__':
    unittest.main()

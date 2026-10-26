import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from sheets_source import sheet_settings

class ConfigTests(unittest.TestCase):
    def test_missing_config_has_actionable_error(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'config.local.json'):
                sheet_settings(Path(d))

    def test_local_config_and_environment_override(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {}, clear=True):
            base = Path(d)
            (base/'config.local.json').write_text(json.dumps({'spreadsheet_id':'demo-id','worksheet':'Tickets'}))
            self.assertEqual(sheet_settings(base), ('demo-id','Tickets'))
            with patch.dict(os.environ, {'GOOGLE_SHEET_ID':'another-id','GOOGLE_SHEET_TAB':'Other'}):
                self.assertEqual(sheet_settings(base), ('another-id','Other'))

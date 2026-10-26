import unittest
from datetime import date
import pandas as pd
from tickets import normalize,date_bounds

class ValidationTests(unittest.TestCase):
    def fixture(self):
        return pd.DataFrame([dict(ticket_id='001',created_at='2026-10-23T17:00:00Z',category='Acceso',priority=' ALTA ',status=' RESUELTO ',first_response_hours='2',resolution_hours='4',channel='Correo')])
    def test_dates_and_normalization(self):
        data,warnings=normalize(self.fixture())
        self.assertEqual(data.iloc[0].created_at.hour,14)
        self.assertEqual(data.iloc[0].status,'Resuelto')
        self.assertEqual(data.iloc[0].ticket_id,'001')
        self.assertFalse(warnings)
    def test_negative_hours(self):
        frame=self.fixture();frame['resolution_hours']=-2
        data,warnings=normalize(frame)
        self.assertTrue(pd.isna(data.iloc[0].resolution_hours));self.assertTrue(warnings)
    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):normalize(pd.concat([self.fixture(),self.fixture()],ignore_index=True))
    def test_invalid_date(self):
        frame=self.fixture();frame['created_at']='invalid'
        data,warnings=normalize(frame)
        self.assertTrue(data.empty);self.assertTrue(warnings)
    def test_partial_range(self):
        day=date(2026,10,23)
        self.assertEqual(date_bounds((day,)),(day,day))
        self.assertEqual(date_bounds(()),(None,None))

if __name__=='__main__':unittest.main()

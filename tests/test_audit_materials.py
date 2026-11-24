import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit_materials',ROOT/'scripts/audit_materials.py')
data=importlib.util.module_from_spec(spec)
spec.loader.exec_module(data)

class VisibleEvidenceTests(unittest.TestCase):
    def test_low_group_orange_count_matches_visible_rows(self):
        self.assertEqual(sum(60<=r[2]<80 for r in data.LOW),7)
        self.assertEqual(len(data.HIGH),14)
        self.assertEqual(len(data.LOW),14)

    def test_group_gap_must_use_visible_table_means(self):
        high=sum(r[2] for r in data.HIGH)/14
        low=sum(r[2] for r in data.LOW)/14
        self.assertAlmostEqual(high,54.0428571429)
        self.assertAlmostEqual(low,62.0571428571)
        self.assertEqual(round(low-high,2),8.01)

    def test_headroom_rounding_is_not_a_false_positive(self):
        self.assertEqual(round((57.10-53.99)/57.10*100,1),5.4)
        self.assertEqual(sum(v<5 for name,v in data.HEADROOM),9)

    def test_missing_sample_explanations_remain_conditional(self):
        findings={r['id']:r for r in data.LFCRI_CHECKS}
        self.assertEqual(findings['L06']['status'],'limited')
        self.assertEqual(findings['L07']['status'],'limited')
        self.assertEqual(findings['L14']['status'],'limited')
        self.assertAlmostEqual((61.2*5+56.1*10)/15,57.8)

    def test_difference_order_identifies_b_not_a(self):
        diffs=[abs(a-b) for a,b in zip(data.BLOCKS['high'],data.BLOCKS['low'])]
        self.assertEqual(diffs.index(max(diffs)),1)
        self.assertAlmostEqual(diffs[3],5.1)

if __name__=='__main__':unittest.main()

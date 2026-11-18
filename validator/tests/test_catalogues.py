"""Shared draft catalogue integrity and key identifier regressions."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def read(name):
            return json.loads((ROOT / 'catalogues' / name).read_text(encoding='utf-8'))
        cls.units = read('qudt-units-3.5.2.json')
        cls.quantities = read('qudt-quantities-3.5.2.json')
        cls.local_quantities = read('isa-phm-quantities.json')

    def test_identifiers_are_unique_and_sources_distinct(self):
        for collection in (self.units, self.quantities, self.local_quantities):
            ids = [item['identifier'] for item in collection]
            self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(item['identifier'].startswith('http://qudt.org/vocab/unit/') for item in self.units))
        self.assertTrue(all(item['identifier'].startswith('http://qudt.org/vocab/quantitykind/') for item in self.quantities))
        self.assertTrue(all(item['identifier'].startswith('urn:isa-phm:') for item in self.local_quantities))

    def test_important_units_and_quantities(self):
        units = {item['identifier']: item for item in self.units}
        self.assertEqual(units['http://qudt.org/vocab/unit/GM']['symbol'], 'g')
        self.assertEqual(units['http://qudt.org/vocab/unit/G']['symbol'], 'G')
        for suffix in ('HZ', 'KiloHZ', 'REV-PER-MIN', 'UNITLESS'):
            self.assertIn('http://qudt.org/vocab/unit/' + suffix, units)
        self.assertIn('http://qudt.org/vocab/quantitykind/Acceleration', {item['identifier'] for item in self.quantities})
        self.assertIn('urn:isa-phm:quantity:quaternion-component', {item['identifier'] for item in self.local_quantities})

    def test_existing_warning_rule_identifiers_exist(self):
        rules = json.loads((ROOT / 'specification' / 'quantity-unit-warning-rules.json').read_text(encoding='utf-8'))['rules']
        units = {item['identifier'] for item in self.units}
        quantities = {item['identifier'] for item in self.quantities} | {item['identifier'] for item in self.local_quantities}
        for rule in rules:
            self.assertTrue(set(rule['unitIdentifiers']) <= units)
            self.assertTrue(set(rule['quantityIdentifiers']) <= quantities)

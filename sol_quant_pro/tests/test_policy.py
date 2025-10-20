import unittest
from policy.bias_gate import BiasInputs, bias_gate
from policy.derivs_filter import DerivsInputs, derivatives_confirmation
from policy.acceptance import AcceptanceInputs, accepted

class TestPolicy(unittest.TestCase):
    def test_bias_gate(self):
        self.assertEqual(bias_gate(BiasInputs(201, 200, 199)), 'Bullish')
        self.assertEqual(bias_gate(BiasInputs(199, 200, 201)), 'Bearish')
        self.assertEqual(bias_gate(BiasInputs(200, 200, 200)), 'Neutral')

    def test_derivs(self):
        self.assertEqual(derivatives_confirmation(DerivsInputs(190, 200, -0.01, 0.001)), 'Neutral_TacticalBearish')
        self.assertEqual(derivatives_confirmation(DerivsInputs(210, 200, 0.02, -0.001)), 'Neutral_TacticalBullish')
        self.assertEqual(derivatives_confirmation(DerivsInputs(210, 200, 0.0, 0.0)), 'None')

    def test_acceptance(self):
        self.assertTrue(accepted(AcceptanceInputs(2, False, True)))
        self.assertTrue(accepted(AcceptanceInputs(0, True, True)))
        self.assertFalse(accepted(AcceptanceInputs(2, False, False)))

if __name__ == '__main__':
    unittest.main()

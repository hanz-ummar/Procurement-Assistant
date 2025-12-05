# Test Fixtures

This directory contains test data files used by the test suite.

## Files

- `golden_procurement.csv`: Reference dataset with known patterns for AI quality testing

## Golden Dataset Characteristics

The golden dataset (`golden_procurement.csv`) is designed to test agent accuracy:

### Spend Patterns
- **Total Spend**: ~$205,200
- **IT Spending**: ~$134,000 (65%)
- **HR Spending**: ~$25,000 (12%)
- **Facilities**: ~$9,500 (5%)
- **Office**: ~$6,700 (3%)

### Supplier Performance
- **Acme Corporation**: Most reliable (3 POs, all completed, avg quality: 9.37)
- **Beta Industries**: Good (3 POs, 2 completed, avg quality: 8.47)
- **Gamma Solutions**: High risk (3 POs, all delayed, avg quality: 7.27)
- **Delta Services**: Excellent small supplier (2 POs, all completed, avg quality: 9.05)
- **Epsilon Tech**: Mixed (2 POs, 1 delayed, avg quality: 7.70)
- **Zeta Supplies**: Reliable small supplier (2 POs, all completed, avg quality: 8.90)

### Risk Indicators
- **High Risk**: Gamma Solutions (all orders delayed)
- **Medium Risk**: Epsilon Tech (50% delay rate)
- **Low Risk**: Acme, Delta, Zeta (100% completion)

### Expected Agent Insights

When tested with this dataset, agents should identify:

1. **Spend Analysis Agent**:
   - IT category dominates spending
   - Acme Corporation is top supplier by volume
   - Average PO value: ~$13,680

2. **Risk Monitoring Agent**:
   - Gamma Solutions has 100% delay rate (HIGH RISK)
   - Epsilon Tech has delivery issues
   - 33% of IT purchases are delayed

3. **Supplier Intelligence Agent**:
   - Top performer: Acme Corporation (quality: 9.37, 100% on-time)
   - Worst performer: Gamma Solutions (quality: 7.27, 0% on-time)
   - Recommended suppliers: Acme, Delta, Zeta

4. **Contract Intelligence Agent**:
   - Net30 is most common payment term (73%)
   - Beta Industries has longest payment terms (Net45)

5. **Compliance Agent**:
   - All POs within expected ranges
   - No outlier payments detected

## Usage in Tests

```python
@pytest.fixture
def golden_dataset():
    return pd.read_csv("tests/fixtures/golden_procurement.csv")

def test_spend_agent_accuracy(golden_dataset):
    agent = SpendAnalysisAgent()
    # Process golden dataset
    # Compare agent output to expected insights
```

## Maintenance

When updating golden dataset:
1. Update expected values in this README
2. Update affected AI quality tests
3. Document any new patterns added

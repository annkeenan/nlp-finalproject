# NLP Final Project

Ann Keenan

## Summary

Final project for CSE 40657 Natural Language Processing

## Usage

### Baseline

Calculate the baseline standard deviation and correctness
* `python3 bin/run_baseline.py`

```
Baseline:
stddev		1.43190
correctness	19.492
```

### Data

Testing on reviews from the following restaurants

name | city | stars | review_count
--- | --- | --- | ---
Bouchon at the Venezia Tower | Las Vegas | 4 | 3439
Luxor Hotel and Casino Las Vegas | Las Vegas | 2.5 | 3429
MGM Grand Hotel | Las Vegas | 3 | 3285
Gangnam Asian BBQ Dining | Las Vegas | 4.5 | 3180
McCarran International Airport | Las Vegas | 3.5 | 3090

Process data for use
* `python3 run_process_db.py --min 3000 --max 3500 data/data.test`
* `python3 run_process_db.py --max 50 data/data.train`

## Results

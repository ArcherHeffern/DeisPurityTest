# About
Brandeis Purity Test. Deployed + Advertised to Brandeis Campus for 1 month.   

Got 1040 Responses - Mean score was 72.448, standard deviation was 15.19 

# Usage
1. Create questions.txt file
2. Put one question per line 
3. Postfix a line to make it a section header
4. You Must have 100 questions

## Example
```
Brandeis:                       <- This begins a section
Seen Ron Liebowitz              <- These are questions
Gone in the Massel pond
Swam in the reservoir
Successfully contacted the BCC
Academics:                      <- This is a new section
Been told to drop a class
Failed a class
Dropped a class to avoid a project/exam
```

## Run
1. (Optional) Create a virtual environment
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Run
```bash
./scripts/run.sh
```

## Analyze Metrics
### Count responses
`./scripts/count.sh`

### Create Histogram of Question Response Frequencies and View Standard Deviation, Range, and Mean
`./scripts/score.py`
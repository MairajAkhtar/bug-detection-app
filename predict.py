# Inside predict.py
import pandas as pd

# Simulated prediction results
results = pd.DataFrame({
    'File': ['file1.py', 'file2.py'],
    'BugPrediction': ['Yes', 'No'],
    'BugSeverity': ['High', 'Low']
})

results.to_csv('predictions.csv', index=False)

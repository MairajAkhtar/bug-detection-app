import pandas as pd

# Simulated static code metrics (replace this with real SonarQube parsing later)
data = {
    'TLOC': [150],
    'LLOC': [130],
    'NBD': [3],
    'VG': [4],
    'CLOC': [50],
    'LOC_method_avg': [20],
    'CYCLO_method_avg': [2],
    'NOSI': [5],
    'PAR': [4],
    'NOSD': [3],
    'NOI': [1],
    'NOF': [6],
    'NOM': [8],
    'RFC': [12],
    'DIT': [2],
    'LCOM': [3]
}

df = pd.DataFrame(data)
df.to_csv("output_metrics.csv", index=False)
print("✅ Exported static metrics to output_metrics.csv")

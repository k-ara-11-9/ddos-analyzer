import pandas as pd

df = pd.read_csv("data/raw/cic-ddos2019/cic-ddos2019.csv")
df.columns = df.columns.str.strip()

df_benign = df[df["Label"] == "BENIGN"].sample(n=2500, random_state=42)
df_attack = df[df["Label"] != "BENIGN"].sample(n=2500, random_state=42)

df_sample = pd.concat([df_benign, df_attack]).sample(frac=1, random_state=42)

df_sample.to_csv("data/processed/ddos_balanced_sample.csv", index=False)
print("Processed dataset saved to data/processed/ddos_balanced_sample.csv")

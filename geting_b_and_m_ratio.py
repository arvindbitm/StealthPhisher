from string import ascii_lowercase, digits
import pandas as pd

# Read the dataset (replace 'spcd.csv' with your actual dataset file)
df = pd.read_csv("spcd.csv")

# Define valid characters
valid_characters = ascii_lowercase + digits + "_-"

# Separate benign and phishing URLs
LABEL = df.iloc[:, -1].name  # Assumes last column is the label column
bDF = df[df[LABEL] == 1]  # Benign URLs
mDF = df[df[LABEL] == 0]  # Phishing URLs

# Compute character frequencies for benign URLs
bCharCounts = bDF['url'].apply(lambda x: pd.Series({char: x.count(char) for char in valid_characters})).sum()
total_bChars = bCharCounts.sum()
bRatio = bCharCounts / total_bChars if total_bChars > 0 else bCharCounts

# Compute character frequencies for phishing URLs
mCharCounts = mDF['url'].apply(lambda x: pd.Series({char: x.count(char) for char in valid_characters})).sum()
total_mChars = mCharCounts.sum()
mRatio = mCharCounts / total_mChars if total_mChars > 0 else mCharCounts

# Save the bRatio and mRatio dictionaries to CSV or JSON for future use
bRatio.to_csv('bRatio.csv', header=True)
mRatio.to_csv('mRatio.csv', header=True)



# Display first few ratios as an example
print("Benign Ratios (bRatio):")
print(bRatio.head())

print("Phishing Ratios (mRatio):")
print(mRatio.head())

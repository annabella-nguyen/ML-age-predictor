import pandas as pd

df = pd.read_csv('organized_utkface/utkface_organized.csv')

print(f"Total Images: {len(df)}")

print("\nSplitting data..")
train_df = df[df['set'] == 'Train']
val_df = df[df['set'] == 'Val']
test_df = df[df['set'] == 'Test']

print(f"  Train: {len(train_df)} images")
print(f"  Val: {len(val_df)} images")
print(f"  Test: {len(test_df)} images")

print("\nSaving CSV files...")
train_df.to_csv('organized_utkface/train.csv', index=False)
print("train.csv saved!")

val_df.to_csv('organized_utkface/val.csv', index=False)
print("val.csv saved!")

test_df.to_csv('organized_utkface/test.csv', index=False)
print("est.csv saved!")

print("csv files created :)")
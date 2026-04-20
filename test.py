from nationalparksdata import refresh_dataset

print("Running test..")
df = refresh_dataset()
print(df.head())
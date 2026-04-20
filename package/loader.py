#Loads in the files back to a dictionary and dataframe for analysis

def build_dataset(save=True):
    from pathlib import Path
    import pandas as pd
    import json

    #data_path = Path("data")

    BASE_DIR = Path(__file__).resolve().parent.parent
    data_path = BASE_DIR / "data"

    base_df = pd.read_csv(data_path / "base_data.csv")

    with open(data_path / "csv_dictionary.json") as f:
        raw = json.load(f)

    csv_dict = {
        k: pd.DataFrame(v)
        for k, v in raw.items()
    }

    rows = []

    # For each park in the dictionary
    for park_code, records in csv_dict.items():
        for _, record in records.iterrows():

            row = base_df[
                base_df['parkCode'].str.lower() == park_code.lower()
            ].copy()

            if not row.empty:
                row = row.iloc[0].to_dict()

                row['year'] = record['Year']
                row['annual visits'] = record['RecreationVisitors']
                row['total visits'] = record.get('TotalRecreationVisitors', None)

                rows.append(row)

    # Create the new DataFrame
    combined_df = pd.DataFrame(rows)

    activities = set()
    import re

    for code in combined_df['parkCode'].unique():
        park_rows = combined_df[combined_df['parkCode'] == code]
        for row_activities in park_rows['activities']:
            if isinstance(row_activities, str):
                matches = re.findall(r':\s*([^,;]+)', row_activities)
                for activity in matches:
                    cleaned = re.sub(r'[^A-Za-z\s]', '', activity)
                    cleaned = cleaned.strip()
                    if cleaned and cleaned[0].isupper() and not cleaned.isupper():
                        activities.add(cleaned.lower())

    # Create dummy variables for each activity in the set
    for activity in activities:
        col_name = f'activity_{activity.replace(" ", "_")}'
        combined_df[col_name] = combined_df['activities'].apply(lambda x: 1 if isinstance(x, str) and activity in x.lower() else 0)

    if save:
        combined_df.to_csv(data_path / "final.csv", index=False)

    return combined_df


#build_dataset()
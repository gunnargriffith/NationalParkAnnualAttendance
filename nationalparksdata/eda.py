def parks_with_activity(*activities):
    import pandas as pd
    df = pd.read_csv('data/final.csv')
    """
    Display parks that have ALL of the specified activities.
    Accepts multiple activities as separate arguments or as a list.
    Example: parks_with_activity('horseback riding', 'hiking')
    """
    # Allow passing a single list as the argument
    if len(activities) == 1 and isinstance(activities[0], (list, tuple)):
        activities = activities[0]
    col_names = [f"activity_{'_'.join(a.lower().split())}" for a in activities]
    missing = [col for col in col_names if col not in df.columns]
    if missing:
        print(f"Missing activity columns: {', '.join(missing)}")
        return
    # Filter parks that have all activities
    mask = df[col_names].eq(1).all(axis=1)
    parks_with_all = df[mask]
    unique_park_names = parks_with_all['fullName'].drop_duplicates()
    print(f"Parks with all activities: {', '.join(activities)}")
    for name in unique_park_names:
        print(name)
    if unique_park_names.empty:
        print("No parks found with all specified activities.")




import pandas as pd

WEEKDAYS = {0: 'Mon',
            1: 'Tue',
            2: 'Wed',
            3: 'Thu',
            4: 'Fri',
            5: 'Sat',
            6: 'Sun'}

METERS_TO_MILES = 1.60934 * 1000


def activities_to_df(detailed_activities):
    keys_to_keep = ['id', 'name', 'start_date_local', 'distance', 'description']
    filtered_activities = [{k: v for k, v in a.items() if k in keys_to_keep} for a in detailed_activities]
    activities_df = pd.DataFrame(filtered_activities)
    activities_df['start_datetime'] = pd.to_datetime(activities_df['start_date_local'])
    activities_df['week_start_date'] = (activities_df['start_datetime'] - activities_df['start_datetime'].dt.weekday.astype('timedelta64[D]')).dt.date
    activities_df['start_date'] = activities_df['start_datetime'].dt.date
    activities_df['distance'] = activities_df['distance'] / METERS_TO_MILES
    return activities_df.sort_values('start_date')


def _print_training_summary(activities_df):
    for i, (week, week_group) in enumerate(activities_df.sort_values('start_date').groupby('week_start_date')):
        print(f"Week of {week.day:02d}/{week.month:02d}")
        for date, activity_group in week_group.groupby('start_date'):
            activity_group.sort_values('start_datetime', inplace=True)
            if len(activity_group) == 1:
                if activity_group.iloc[0]['description']:
                    print(
                        f"{WEEKDAYS[date.weekday()]}: {activity_group.iloc[0]['name']}, {round(activity_group.iloc[0]['distance'], 1)}m, {activity_group.iloc[0]['description']}")
                else:
                    print(
                        f"{WEEKDAYS[date.weekday()]}: {activity_group.iloc[0]['name']}, {round(activity_group.iloc[0]['distance'], 1)}m")
            else:
                if activity_group.iloc[0]['description']:
                    print(
                        f"{WEEKDAYS[date.weekday()]}: AM - {activity_group.iloc[0]['name']}, {round(activity_group.iloc[0]['distance'], 1)}m, {activity_group.iloc[0]['description']}, ",
                        end='')
                else:
                    print(
                        f"{WEEKDAYS[date.weekday()]}: AM - {activity_group.iloc[0]['name']}, {round(activity_group.iloc[0]['distance'], 1)}m, ",
                        end='')
                for i in range(1, len(activity_group)):
                    if activity_group.iloc[i]['description']:
                        print(
                            f"PM - {activity_group.iloc[i]['name']}, {round(activity_group.iloc[i]['distance'], 1)}m, {activity_group.iloc[i]['description']}")
                    else:
                        print(f"PM - {activity_group.iloc[i]['name']}, {round(activity_group.iloc[i]['distance'], 1)}m")
        print(f"Total: {round(week_group.distance.sum(), 1)} miles.\n")


def print_training_summary(detailed_activities):
    activities_df = activities_to_df(detailed_activities)
    _print_training_summary(activities_df)


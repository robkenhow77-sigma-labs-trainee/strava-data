from datetime import datetime, timedelta
import json

import pandas as pd
import altair as alt


def make_pace_df(data: list[dict]):
    """Creates a pace df"""
    df = pd.DataFrame(data["splits_metric"])
    df = df[["average_speed", "elapsed_time"]]
    df["time"] = df["elapsed_time"].cumsum()
    # df["time"] = df["time"].apply(lambda x: timedelta(seconds=x))
    df["time"] = df["time"].apply(lambda x: round(x/60, 2))
    df["average_speed"] = df["average_speed"].apply(lambda x: x * 3.6)
    total_time = df["time"].max()
    if total_time > 30:
        tick_count = 10
    else:
        tick_count = 5
    return (df[["average_speed", "time"]], tick_count)


def make_pace_graph(data: list[dict]):
    """Creates a pace graph"""
    df, tick_count = make_pace_df(data)
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X("time", axis=alt.Axis(tickCount=tick_count)),
        y="average_speed"
    ).properties(
        width='container',
        height='container'
    )
    return chart.to_json()


def make_elevation_df(data: list[dict]):
    """Creates an elevation df"""
    df = pd.DataFrame(data["splits_metric"])
    df = df[["elevation_difference", "elapsed_time"]]
    df["time"] = df["elapsed_time"].cumsum()
    df["elevation"] = df["elevation_difference"].cumsum()
    # df["time"] = df["time"].apply(lambda x: timedelta(seconds=x))
    df["time"] = df["time"].apply(lambda x: round(x/60, 2))
    total_time = df["time"].max()
    if total_time > 30:
        tick_count = 10
    else:
        tick_count = 5
    return (df[["elevation", "time"]], tick_count)


def make_elevation_graph(data: list[dict]):
    """Creates an elevation graph"""
    df, tick_count = make_elevation_df(data)
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X("time", axis=alt.Axis(tickCount=tick_count)),
        y="elevation"
    ).properties(
        width='container',
        height='container'
    )
    return chart.to_json()


if __name__ == "__main__":
    with open("example_activity.json", 'r', encoding="UTF-8") as file:
        data = json.load(file)
    df, tick_count = make_elevation_df(data)

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X("time", axis=alt.Axis(tickCount=tick_count)),
        y="elevation"
    ).properties(
        height=500,
        width=700
    )
    chart.save('chart.html')
   
def basic_cleaning(df):

    """docstring

    """

    ## imports
    import pandas as pd
    import numpy as np

    # first, remove LOCATION.  it is redundant with LATITUDE and LONGITUDE
    df.drop(columns = "LOCATION", inplace = True)

    ## there are some zeros in the positions
    mask = (df["LATITUDE"] < 35) | (df["LONGITUDE"]>-65)

    df.loc[mask,"LATITUDE"] = np.nan
    df.loc[mask,"LONGITUDE"] = np.nan


    # change date and time to datetime64

    crash_dt = df["CRASH DATE"] + " " + df["CRASH TIME"]
    crash_dt = pd.to_datetime(crash_dt)

    df.insert(0, "DATETIME", crash_dt)

    df.drop(columns = ["CRASH DATE", "CRASH TIME"], inplace = True)

    ## some of the records have non-zero NUMBER OF MOTORIST KILLED.
    # some of these involved motorbikes

    ## OFF-STREET NAME
    #list( df["OFF STREET NAME"][~df["OFF STREET NAME"].isna()] )
    # basically a street address if there is one.  missing 90% of the values

    df.drop(columns="OFF STREET NAME", inplace = True)


    # NUMBER OF PERSONS INJURED   and    NUMBER OF PERSONS KILLED
    # almost everything is there.  convert to integer

    na_rows = df["NUMBER OF PERSONS INJURED"].isna()
    na_rows = df.loc[na_rows,:].index

    # the first one, 21634, has no injuries or deaths.  drop!
    df.drop(index=na_rows[0], inplace = True)

    # the second one, 26814, has a NUMER OF CYCLIST INJURED = 1, but nothing in the 
    df.loc[na_rows[1],"NUMBER OF PERSONS INJURED"] = 1
    df.loc[na_rows[1],"NUMBER OF PERSONS KILLED"] = 0

    df["NUMBER OF PERSONS INJURED"] = df["NUMBER OF PERSONS INJURED"].astype("int")
    df["NUMBER OF PERSONS KILLED"] = df["NUMBER OF PERSONS KILLED"].astype("int")


    ## sort the collisions by timestamp
    df.sort_values(by = "DATETIME", inplace = True, ignore_index = True)


    # any duplicate rows?
    #df[df.duplicated(keep = False)]
    df.drop_duplicates(inplace = True, ignore_index = True)

    ## let's trim down the data to cases when a cyclist was injured or killed
    drop_cols = ["NUMBER OF PERSONS INJURED", "NUMBER OF PERSONS KILLED",
                 "NUMBER OF PEDESTRIANS INJURED", "NUMBER OF PEDESTRIANS KILLED",
                 "NUMBER OF MOTORIST INJURED", "NUMBER OF MOTORIST KILLED"]

    df.drop(columns=drop_cols, inplace=True)

    return df

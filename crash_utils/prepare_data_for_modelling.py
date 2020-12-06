def prepare_data_for_modelling(df):

    '''Note that this function also uses "make_crash_features.py" to create some
    features for the fitting

    '''

    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.feature_extraction.text import CountVectorizer
    from crash_utils.make_crash_features import make_crash_features


    # trim more columns that aren't useful for modelling
    df.drop(columns=["LATITUDE","LONGITUDE","COLLISION_ID"],inplace = True)

    # now encode the outcome:  0 = no injury, 1 = injury, 2 = fatality

    # initiate column
    df["outcome"] = np.nan

    # no injuries
    mask = df["NUMBER OF CYCLIST INJURED"] == 0
    df.loc[mask,"outcome"] = 0

    # injuries only
    mask = df["NUMBER OF CYCLIST INJURED"] > 0
    df.loc[mask,"outcome"] = 1

    mask = df["NUMBER OF CYCLIST KILLED"] > 0
    df.loc[mask,"outcome"] = 2

    df.drop(columns = ["NUMBER OF CYCLIST INJURED","NUMBER OF CYCLIST KILLED"],
            inplace = True)


    # make another data frame, but now with features (can be easier for some analyses)
    df = make_crash_features(df)

    # lowercase the column names
    df.columns= df.columns.str.lower()


    # now one-hot encode some data
    ohe = OneHotEncoder(drop = "first")
    ohe.fit(df[["borough","zip code","on street name"]])
    ohe_matrix = ohe.transform(df[["borough","zip code","on street name"]])
    ohe_df = pd.DataFrame.sparse.from_spmatrix(data = ohe_matrix,
                                               columns = ohe.get_feature_names())


    # generate a document-term matrix for the vehicles and contributing factors

    # vehicles
    # 1. Instantiate
    bagofwords = CountVectorizer(token_pattern=r"(?u)\S\S+")

    # 2. Fit
    bagofwords.fit(df["vehicles"])

    # 3. Transform
    veh_transformed = bagofwords.transform(df["vehicles"])

    veh_df = pd.DataFrame.sparse.from_spmatrix(data = veh_transformed,
                                               columns = bagofwords.get_feature_names())


    # crash factors

    # 1. Instantiate
    bagofwords = CountVectorizer(token_pattern=r"(?u)\S\S+")

    # 2. Fit
    bagofwords.fit(df["factors"])

    # 3. Transform
    factors_transformed = bagofwords.transform(df["factors"])


    factors_df = pd.DataFrame.sparse.from_spmatrix(data = factors_transformed,
                                                   columns = bagofwords.get_feature_names())



    # concatenate the original df, the ohe df, and the two document term dfs

    # reset indices to ensure smooth concatenation
    df.reset_index(drop = True, inplace = True)
    ohe_df.reset_index(drop=True, inplace=True)
    veh_df.reset_index(drop = True, inplace=True)
    factors_df.reset_index(drop = True, inplace=True)


    df = pd.concat((df,ohe_df,veh_df, factors_df),axis=1)
    del ohe_df, veh_df, factors_df

    # drop all columns that we encoded or count-vectorized
    df.drop(columns = ["vehicles","factors","borough","zip code","on street name"],
            inplace = True)


    # move outcome to be the 1st column
    outcome = df["outcome"]
    df.drop(columns="outcome",inplace=True)
    df.insert(0,"outcome",outcome)


    return df

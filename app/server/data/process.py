import pandas as pd
import os
import glob

csv_files = glob.glob("./tech_raw/*.csv")

for file in csv_files:
    df = pd.read_csv(file)

    selected_df = df[["Date", "Adj Close"]].rename(
        columns={"Date": "date", "Adj Close": "price"}
    )

    new_file_name = "./tech/" + os.path.splitext(os.path.basename(file))[0] + ".csv"
    selected_df.to_csv(new_file_name, index=False)


# $GOOG Alphabet Inc.
# $MSFT Microsoft Corporation
# $FB Facebook, Inc.
# $T AT&T Inc.
# $CHL China Mobile Limited
# $ORCL Oracle Corporation
# $TSM Taiwan Semiconductor Manufacturing Company Limited
# $VZ Verizon Communications Inc.
# $INTC Intel Corporation
# $CSCO Cisco Systems, Inc.

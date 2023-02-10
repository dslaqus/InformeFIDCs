import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from urllib.error import URLError
import os
import sys
from s3fs.core import S3FileSystem
import warnings
import re



# aws keys stored in ini file in same path
# refer to boto3 docs for config settings
os.environ['AWS_CONFIG_FILE'] = 'aws_config.ini'

s3 = S3FileSystem(anon=False)
key = 'streamlit/informes_fidcs_2023-02-09.csv'
bucket = 'data-science-laqus'

df = pd.read_csv(s3.open(f'{bucket}/{key}', mode='rb')).drop(columns='Unnamed: 0')



try:
    fidcs = st.multiselect(
        "Choose FIDCs", list(df.NomeFIDC), ["China", "United States of America"]
    )
    if not fidcs:
        fidcs = list(df.NomeFIDC.drop_duplicates().values)
    else:
        data = df.loc[fidcs]
        st.write("### FIDCs Teste", data.sort_index())

        data = df.copy()
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="NomeFIDC",
                y="Carteira",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
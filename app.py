import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import streamlit as st
from urllib.error import URLError
import os
import sys
from s3fs.core import S3FileSystem
import warnings
import re
import plotly.graph_objects as go


# aws keys stored in ini file in same path
# refer to boto3 docs for config settings
os.environ['AWS_CONFIG_FILE'] = 'aws_config.ini'

s3 = S3FileSystem(anon=False)
key = 'streamlit/informes_fidcs_2023-02-09.csv'
bucket = 'data-science-laqus'

df = pd.read_csv(s3.open(f'{bucket}/{key}', mode='rb')).drop(columns='Unnamed: 0')
df_plot = df.copy()
df_plot = df_plot.sort_values(by='Carteira',ascending=False).iloc[:50,:].drop_duplicates()
df_plot = df_plot.sort_values(by='Carteira',ascending=True)
carteira_ = df_plot.Carteira
carteira_ate_360_ = df_plot['Carteira por prazo de vencimento até 30 dias'] + df_plot['Carteira por prazo de vencimento de 31 a 60 dias'] + df_plot['Carteira por prazo de vencimento de 61 a 90 dias'] + df_plot['Carteira por prazo de vencimento de 91 a 120 dias'] + df_plot['Carteira por prazo de vencimento de 121 a 150 dias'] + df_plot['Carteira por prazo de vencimento de 151 a 180 dias'] + df_plot['Carteira por prazo de vencimento de 181 a 360 dias']
NomeFIDC_ = df_plot.NomeFIDC

fig = go.Figure()
fig.add_trace(go.Bar(
    y=NomeFIDC_,
    x=carteira_,
    name='Carteira',
    orientation='h',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
))
fig.add_trace(go.Bar(
    y=NomeFIDC_,
    x=carteira_ate_360_,
    name='Carteira com operações de até 360 dias',
    orientation='h',
    marker=dict(
        color='rgba(58, 71, 80, 1.0)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
    )
))

fig.update_layout()



tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)
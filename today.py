from logging import debug
import pandas as pd
from pandas.core.frame import DataFrame
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import openpyxl
import math
import datetime

import os


from func_collection import get_file_from_gdrive

st.set_page_config(page_title='受注内容/日')
st.markdown('#### 受注内容/日')

#小数点以下１ケタ
pd.options.display.float_format = '{:.2f}'.format

#current working dir
cwd = os.path.dirname(__file__)

#**********************gdriveからエクセルファイルのダウンロード・df化
data_list = ['--データを選択--', '北日本', '東日本', '中部', '関西', '中四国九州']

selected_data = st.selectbox(
    'データの選択',
    data_list
)

if selected_data == '--データを選択--':
    st.stop()
data_dict = {
    '北日本': 'kita79j',
    '東日本': 'higashi79j',
    '中部': 'chuubu79j',
    '関西': 'kansai79j',
    '中四国九州': 'chuushikoku79j'
}

#driveからファイル取得dataに保存
fname = data_dict[selected_data]
file_name = f"{fname}.xlsx"
get_file_from_gdrive(cwd, file_name)

#****************************************************************ファイルの加工

@st.cache_data(ttl=datetime.timedelta(hours=1))
def make_data_now(file_path):
    
    df_now = pd.read_excel(
    file_path, sheet_name='受注委託移動在庫生産照会', \
        usecols=[3, 6, 8, 10, 14, 15, 16, 46]) #index　ナンバー不要　index_col=0

    # ***INT型への変更***
    df_now[['数量', '単価', '金額']] = df_now[['数量', '単価', '金額']].fillna(0).astype('int64')
    #fillna　０で空欄を埋める

    return df_now

# ***今期受注***
#受注データのpath取得
fname_jnow = f'{fname}.xlsx'
path_jnow = os.path.join(cwd, 'data', fname_jnow)

df_now = make_data_now(path_jnow)

#************************ファイルのdf化・加工

df_now.sort_values('受注日', ascending=False, inplace=True)

#受注日の選択
#時刻の消去
df_now['受注日'] = df_now['受注日'].apply(lambda x: str(x).split('T')[0])
df_now['受注日'] = df_now['受注日'].apply(lambda x: str(x).split(' ')[0])

selected_day =st.selectbox(
    '受注日を選択',
    df_now['受注日'].unique()
)
df_selected_now = df_now[df_now['受注日'] == selected_day]

#担当者の選択
person_list = list(df_selected_now['営業担当者名'].unique())
person_list.insert(0, '全員')

selected_person = st.selectbox(
    '担当者を選択',
    person_list
)

if selected_person == '全員':
    day_sum = df_selected_now['金額'].sum()
    st.write('合計金額:')
    day_sum = '{:,}'.format(day_sum)
    st.markdown(f'##### {day_sum}')

    st.table(df_selected_now.iloc[:, 0:6])

else:
    df_selected_now2 = df_selected_now[df_selected_now['営業担当者名']==selected_person]

    day_sum = df_selected_now2['金額'].sum()
    st.write('合計金額:')
    day_sum = '{:,}'.format(day_sum)
    st.markdown(f'##### {day_sum}')

    st.table(df_selected_now2.iloc[:, 0:6])






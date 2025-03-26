import streamlit as st
import pandas as pd
from io import StringIO
import openpyxl

# Excel'den veriyi oku
df = pd.read_excel("Faaliyet_Matrisi.xlsx")

# Politikaların stratejiyle tekrarlandığı haliyle eşleştirildiği satırları belirle
policy_strat_pairs = []
current_policy = None
current_policy_full = None

for _, row in df.iterrows():
    policy = row['POLİTİKA']
    strat = row['STRATEJİ']

    if pd.notna(policy):
        current_policy = policy.split()[0]  # P.1
        current_policy_full = policy        # P.1. Açıklama

    if pd.notna(strat):
        strat_code = strat.split()[0]       # S.1.1
        strat_full = strat                  # S.1.1. Açıklama
        policy_strat_pairs.append({
            "policy_code": current_policy,
            "policy_full": current_policy_full,
            "strategy_code": strat_code,
            "strategy_full": strat_full
        })

# VeriFrame'e dönüştür
pairs_df = pd.DataFrame(policy_strat_pairs)

# Pivot tablo oluştur (kodlar bazında)
pivot_df = pd.DataFrame(index=pairs_df['strategy_code'].unique(),
                        columns=pairs_df['policy_code'].unique()).fillna("")

# Eşleşenlere çarpı koy
for _, row in pairs_df.iterrows():
    pivot_df.loc[row['strategy_code'], row['policy_code']] = '❌'

# Tooltip bilgileri için sözlükler
policy_tooltips = pairs_df.drop_duplicates('policy_code').set_index('policy_code')['policy_full'].to_dict()
strategy_tooltips = pairs_df.drop_duplicates('strategy_code').set_index('strategy_code')['strategy_full'].to_dict()

st.set_page_config(layout="wide")  # Geniş ekran
st.title("ARDEK Politika-Strateji Matrisi")

# HTML tablosu oluştur
html = "<div style='overflow-x:auto'><table border='1' style='border-collapse: collapse; min-width: 100%;'>"

# Header
html += "<tr><th style='position:sticky; left:0; background-color:#f0f0f0;'></th>"
for col in pivot_df.columns:
    full = policy_tooltips.get(col, col)
    html += f"<th title='{full}' style='padding:8px; text-align:center; background-color:#e0f0ff'>{col}</th>"
html += "</tr>"

# Satırlar
for idx in pivot_df.index:
    full = strategy_tooltips.get(idx, idx)
    html += f"<tr><td title='{full}' style='padding:8px; position:sticky; left:0; background-color:#f9f9f9'>{idx}</td>"
    for col in pivot_df.columns:
        val = pivot_df.loc[idx, col]
        html += f"<td style='text-align:center; padding:8px'>{val}</td>"
    html += "</tr>"

html += "</table></div>"

# Göster
st.markdown(html, unsafe_allow_html=True)

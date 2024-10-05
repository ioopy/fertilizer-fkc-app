import streamlit as st
from utils.func import break_page, get_color_map, get_head_title, section_title
from utils.load_data import get_data
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Default page header.
get_head_title(1, "เพื่อศึกษาแบรนด์ที่ยอดขายสูง")
# Get data & Filter data
data_all = get_data()
data_all = data_all[['marketplace', 'product_name', 'amount_sold_format', 'discount_price_format', 'total_value', 'per_discount_format', 'itemId', 'shopId', 'star_review']]
data_all = data_all[data_all['amount_sold_format'] > 0]

def get_bar_plot(data, title):
    data = data.sort_values('total_value', ascending=False)
    data.rename(columns={'total_value': 'ยอดขาย'}, inplace=True)
    fig = px.bar(
        data,
        x='ยอดขาย', 
        y='marketplace',
        color=data["marketplace"],
        orientation='h',
        text='ยอดขาย',
        color_discrete_map=get_color_map(),
    ) 
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="ยอดขาย",
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")

def get_bar_plot_group(data, title):

    sorted_df_final = data.sort_values(by=['marketplace', 'amount_sold_format'], ascending=[False, True])
    sorted_df_final.rename(columns={'amount_sold_format': 'ยอดขาย'}, inplace=True)
    fig = px.bar(
        sorted_df_final,
        x='ยอดขาย', 
        y='product_nm',
        color=sorted_df_final["marketplace"],
        orientation='h',
        barmode='group',
        height=700,
        color_discrete_map=get_color_map(),
        text='ยอดขาย')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="ยอดขาย (ชิ้น)",
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")

def get_line_comparision(data, title):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['amount_sold_format'],
        name="ยอดขาย ชิ้น",
        line=dict(color='#1f77b4',width=2),
        line_shape='linear'
    ))


    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['discount_price_format'],
        name="ราคาขาย",
        yaxis="y2",
        line=dict(color='#ff7f0e',width=2),
        line_shape='linear'
    ))

    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['per_discount_format'],
        name="% ส่วนลด",
        yaxis="y3",
        line=dict(color='#d62728',width=2, dash='dot'),
        line_shape='linear'
    ))

    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['star_review'],
        name="คะแนน",
        yaxis="y4",
        line=dict(color='#9467bd',width=2, dash='dot'),
        line_shape='linear'
    ))


    # Create axis objects
    fig.update_layout(
        xaxis=dict(
            domain=[0.13, 0.9]
        ),
        yaxis=dict(
            title="ราคาขาย",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="ราคาขาย",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position=0.01
        ),
        yaxis3=dict(
            title="% ส่วนลด",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        yaxis4=dict(
            title="คะแนน",
            titlefont=dict(
                color="#9467bd"
            ),
            tickfont=dict(
                color="#9467bd"
            ),
            anchor="free",
            overlaying="y",
            side="right",
            position=1
        )
    )

    # Update layout properties
    fig.update_layout(
        title_text=title,
        width=800,
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        legend_title_text=''
    )

    st.plotly_chart(fig, theme="streamlit")
# Section 1
section_title("ระหว่าง Shopee และ Lazada แพลตฟอร์มใดที่มียอดขายเฉลี่ยของสินค้าสูงกว่ากัน")
grouped_df = data_all.groupby('marketplace')['total_value'].sum().reset_index()

display = data_all.groupby('marketplace').agg(
    total_value_sum=('total_value', 'sum'),
    total_value_mean=('total_value', 'mean')
).reset_index()

display['total_value_mean'] = display['total_value_mean'].apply(lambda x: f"{x:,.2f}")
display.rename(columns={'total_value_sum': 'ยอดขายรวม', 'total_value_mean': 'ยอดขายเฉลี่ย'}, inplace=True)
st.dataframe(display, hide_index=True)
get_bar_plot(grouped_df, "")

st.divider()
break_page()

# Section 2
section_title("สินค้าที่ขายดีที่สุดใน Shopee และ Lazada แตกต่างกันมากน้อยเพียงใด")

display = data_all[['marketplace','product_name', 'discount_price_format', 'per_discount_format', 'amount_sold_format', 'total_value', 'itemId', 'shopId']]
display = display.sort_values('total_value', ascending=False)
display = display.drop_duplicates()
st.dataframe(display, hide_index=True)

shopee = data_all[data_all['marketplace'] == 'shopee']
shopee = shopee.sort_values('total_value', ascending=False)
shopee = shopee.drop_duplicates()
shopee = shopee.head(10)
get_line_comparision(shopee, "Shopee 10 อันดับสินค้าที่ขายดี")

lazada = data_all[data_all['marketplace'] == 'lazada']
lazada = lazada.sort_values('total_value', ascending=False)
lazada = lazada.drop_duplicates()
lazada = lazada.head(10)
get_line_comparision(lazada, "Lazada 10 อันดับสินค้าที่ขายดี")




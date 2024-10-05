import streamlit as st
import pandas as pd
import plotly.express as px
from utils.func import break_page, get_color_map, get_head_title, get_lat_lon, section_title
from utils.load_data import get_data
import plotly.graph_objects as go

from plotly.subplots import make_subplots

# Default page header.
get_head_title(4, "เพื่อดึงดูดลูกค้า")
# Get data & Filter data
data_all = get_data()
data_all = data_all[['marketplace', 'star_review', 'original_price', 'discount_price_format', 'per_discount_format', 'amount_sold_format', 'province', 'total_value', 'latitude', 'longitude']]
data_all = data_all[data_all['amount_sold_format'] > 0]

def get_scatter_plot(data):
    mean_discount_price = data['discount_price_format'].mean()
    fig = px.scatter(data, x='star_review', y='discount_price_format',
                # color='product_nm',
                # symbol='product_nm',
                # trendline='ols'
                # hover_name="product_nm",
                # labels={'product_nm': 'สินค้า', 'original_price': 'ราคา', 'star_review': 'คะแนน', 'total_sale': 'sale value', 'province': 'จังหวัด', 'amount_sold_format': 'ยอดขาย'},
            )
    fig.add_shape(type="line",
                x0=0, x1=5,
                y0=mean_discount_price, y1=mean_discount_price,
                line=dict(color="Red", width=2, dash="dash"),
                name="Mean Price")
    fig.add_annotation(x=data_sorted['star_review'].min(), y=mean_discount_price,
                    text=f"ราคาเฉลี่ย: {mean_discount_price:.2f}",
                    showarrow=False, 
                    yshift=10,  # Shift the annotation up slightly
                    font=dict(color="Red", size=12))
    fig.update_layout(
        # shapes=[dict(
        #     type="line",
        #     xref="x", yref="y",
        #     x0=mean_discount_price, y0=data_sorted['star_review'].maxmin(),
        #     x1=mean_discount_price, y1=data_sorted['star_review'].min(),
        #     line=dict(color="Red", width=2, dash="dash"),
        #     name="ราคาเฉลี่ย"
        # )],
        title={
            'text': '',
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="ราคาสินค้า",
        xaxis_title="คะแนนรีวิว",
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
        margin=dict(
            t=100  # Add space at the top (increase this value as needed)
        ),
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")
    return None

def plot_scatter_map(data, size_col, title=""):
    fig = px.scatter_mapbox(data,
                            lat="latitude",
                            lon="longitude",
                            size=size_col,   # Column to determine the bubble size
                            color="marketplace", 
                            color_discrete_map=get_color_map(), # Color bubbles by marketplace
                            hover_name="province",  # Column that will appear on hover
                            hover_data={"latitude": False, "longitude": False, "marketplace": True},
                            zoom=4.2,  # Adjust zoom level
                            size_max=50)

    # Customize the map appearance
    fig.update_layout(mapbox_style="open-street-map",
                    mapbox_center={"lat": 13.5, "lon": 100.5},  # Center of Thailand
                    margin={"r": 0, "t": 100, "l": 0, "b": 0},
                    width=300,
                    height=500,
                    legend=dict(
                        orientation="h",        # Set the legend orientation to horizontal
                        yanchor="bottom",       # Anchor the legend at the bottom
                        y=1,                    # Position the legend above the graph
                        xanchor="center",       # Center the legend horizontally
                        x=0.5                   # Set the legend to the center of the x-axis
                    ),
                    legend_title_text='',
                    title={
                        'text': title,
                        'x': 0.5,  # Center the title
                        'xanchor': 'center',  # Ensure it's anchored in the center
                        'yanchor': 'top'  # Keep it at the top
                    },
                )

    st.plotly_chart(fig, theme="streamlit")

# Section 1
section_title("สินค้าที่มีราคาหลังหักส่วนลดต่ำกว่าค่าเฉลี่ยได้รับรีวิวดีขึ้นหรือไม่") #discount_price, star_review
data_sorted = data_all.sort_values(by='discount_price_format', ascending=False)

get_scatter_plot(data_sorted)

st.divider()
break_page()
# Section 2
section_title("ร้านในพื้นที่ใดมีแนวโน้มที่จะมีลูกค้าใช้จ่ายมากที่สุดในสินค้าที่มีราคาสูงหลังหักส่วนลด") #province, original_price, amount_sold
mean_total_value = data_all['total_value'].mean()
mean_amount_sold = data_all['amount_sold_format'].mean()
discount_stats = data_all.groupby(['marketplace', 'province', 'latitude', 'longitude']).agg({
    'amount_sold_format': 'sum',
    'total_value': 'sum'
}).reset_index()


col1, col2 = st.columns([1,1])
with col1:
    plot_scatter_map(discount_stats, 'amount_sold_format', "ยอดขายจำนวนชิ้น")
with col2:
    plot_scatter_map(discount_stats, 'total_value', "ยอดขาย")

break_page()

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="SuperstoreOrders Sales Analysis!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: SuperStore Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df = pd.read_csv("SuperStoreOrders.csv", encoding= "ISO-8859-1")

col1, col2, col3, col4 = st.columns((4))
df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True, errors='coerce')

# Getting the min and max date

startDate = startDate = pd.to_datetime(df["order_date"]).min()
endDate = pd.to_datetime(df["order_date"]).max()

with col1: 
     date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["order_date"] >= date1) & (df["order_date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")
# Create for Region
Region = st.sidebar.multiselect("Pick your Region", df["region"].unique())
if not Region:
    df2 = df.copy()
else:
    df2 = df[df["region"].isin(Region)]
    
    # Create Country
    # Create for State
Country = st.sidebar.multiselect("Pick the country", df2["country"].unique())
if not Country:
    df3 = df2.copy()
else:
    df3 = df2[df2["country"].isin(Country)]
# Create for State
State = st.sidebar.multiselect("Pick the State",df3["state"].unique())

# filter the data based on Region, State and City


if not Region and not Country and not State:
    filtered_df = df
elif not Country and not State:
    filtered_df = df[df["region"].isin(Region)]
elif not Region and not State:
    filtered_df = df[df["country"].isin(Country)]
elif Country and State:
    filtered_df = df3[df["country"].isin(Country) & df3["state"].isin(State)]
elif Region and State:
    filtered_df = df3[df["region"].isin(Region) & df3["state"].isin(State)]
elif Region and Country:
    filtered_df = df3[df["region"].isin(Region) & df3["state"].isin(Country)]
elif State:
    filtered_df = df3[df3["state"].isin(State)]
else:
#     filtered_df = df3[df3["region"].isin(Region) & df3["state"].isin(Country) & df3["state"].isin(State)]
#    # category_df = df[["category","sales"]].groupby(by="category")["sales"].sum()
#     category_df = filtered_df.groupby(by = ["category"], as_index = False)["sales"].sum()
  filtered_df = df3[ (df3["region"].isin(Region)) &  (df3["state"].isin(Country)) &  (df3["state"].isin(State))]
  category_df = filtered_df.groupby(by=["category"], as_index=False)["sales"].sum()
st.subheader("Sales by Category ")
# fig = px.bar(filtered_df, x = "Category", y = "sales", text = ['${:,.2f}'.format(x) for x in filtered_df["sales"]],
                #  template = "seaborn")
    # fig = px.bar(filtered_df, x="category", y="sales", labels={"category": "Category", "sales": "Sales {$}"},
    #          title="Sales by Category", text="sales",
    #          template="gridon", height=500)
    #
fig = px.bar(df, x="category", y="sales", labels={"category": "Category", "sales": "Sales {$}"},
             title="Sales by Category", text="sales",
             template="gridon", height=500)

st.plotly_chart(fig,use_container_width=True, height = 200)
        
with col2:
    st.subheader("Product Sales by Region")
    fig = px.pie(filtered_df, values = "sales", names = "region", hole = 0.5)
    fig.update_traces(text = filtered_df["region"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

#     #col3, col4, col5: st.columns(3) # type: ignore
    
# with col3:
#     st.subheader(" Sales by Product")
#     # fig = px.bar(filtered_df, values = "sales", names = "category", hole = 0.5)
#     # fig.update_traces(text = filtered_df["region"], textposition = "outside")
#     # st.plotly_chart(fig,use_container_width=True)
        

# fig = px.bar(filtered_df, x="sub_category", y="sales", labels={"sub_category": "Sub_category", "sales": "Sales {$}"},
#              title="Sales by Product", text="sales",
#              template="gridon", height=500)


    
# st.subheader("Product Sales by Region")
# # Create a treemap visualization
# fig = px.treemap(filtered_df, path=["Region"],  # Hierarchical levels for treemap
#     values="Sales",  # Box size
#     color="Sales",  # Box color intensity
#     color_continuous_scale="Blues",  # Color palette
#     title="Product Sales by Region",
# )

# # Add labels
# fig.update_traces(textinfo="label+value", textposition="middle center")

# # Display the treemap
# st.plotly_chart(fig, use_container_width=True)
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by = "region", as_index = False)["sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')
        
        filtered_df["month_year"] = filtered_df["drder_date"].dt.to_period("M")
st.subheader('Category Sales by Month')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="sales", labels = {"sales": "Amount"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of SalesByMonth:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "SalesByMonth.csv", mime ='text/csv')
    
    # Create a treem based on Region, category, sub-Category
st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path = ["region","category","sub_category"], values = "sales",hover_data = ["sales"],
                  color = "sub_category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values = "sales", names = "segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader(' Sales  by Category')
    fig = px.pie(filtered_df, values = "sales", names = "category", template = "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["region","country","state","category","sales","profit","quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    
    sub_category_Year = pd.pivot_table(data = filtered_df, values = "sales", index = ["sub_category"],columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Create a scatter plot
data1 = px.scatter(filtered_df, x = "sales", y = "profit", size = "quantity")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")

import streamlit as st
import yfinance as yf
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key="Your api key")
def get_stock_data(ticket_stock,start_date,end_date):
    data = yf.download(ticket_stock,start=start_date,end=end_date)
    return data

st.title("interactive financial market data  and comperative analysis".title())

st.sidebar.header("users inputs".title())
selected_stock=st.sidebar.text_input("Enter your stock ticket","AAPL").upper()
selected_stock2=st.sidebar.text_input("Enter your stock ticket","TSLA").upper()
start_date=st.sidebar.date_input("Enter the start date",datetime(2025,1,1))
end_date = st.sidebar.date_input("Enter the end date", datetime(2025,2,1))

stock_data1 = get_stock_data(selected_stock,start_date,end_date)
stock_data2=get_stock_data(selected_stock2,start_date,end_date)

col1,col2=st.columns(2)

with col1:
    st.subheader(f"Displaying the data for:{selected_stock}")
    st.write(stock_data1)
    char_type=st.sidebar.selectbox(f"Select chart for your {selected_stock}",["Bar","line"])
    if char_type=="Bar":
        st.bar_chart(stock_data1["Close"])
    else:
        st.line_chart(stock_data1["Close"])

with col2:
    st.subheader(f"Displaying the data for:{selected_stock2}")
    st.write(stock_data2)
    char_type1 = st.sidebar.selectbox(f"Select chart for your {selected_stock}",["Bar","Line"])
    if char_type1 == "Bar":
        st.bar_chart(stock_data2["Close"])
    else:
        st.line_chart(stock_data2["Close"])

if st.button("comparative perfomance".upper()):
    response= client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"You are a financial assistant that will retrieve two tables of financial market data and will summarize the comparative performance in text, in full detail with highlights for each stock and also a conclusion with a markdown output. BE VERY STRICT ON YOUR OUTPUT"},
            {"role":"user","content":f"This is the {selected_stock} stock data : {stock_data1}, this is {selected_stock2} stock data: {stock_data2}" }
        ]
    )
    st.write(response.choices[0].message.content)
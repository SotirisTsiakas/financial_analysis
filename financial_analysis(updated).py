import streamlit as st
import yfinance as yf
from datetime import datetime
from openai import OpenAI


client = OpenAI(api_key=st.secrets["OPEN_API_KEY"])
def get_stock_data(ticket_stock,start_date,end_date):
    data = yf.download(ticket_stock,start=start_date,end=end_date)
    return data

def get_metrics(ticket_stock):
    metrics = dict()
    metrics["market_cap"] = yf.Ticker(ticket_stock).info["marketCap"]
    metrics["EPS_Ratio"] = yf.Ticker(ticket_stock).info['trailingEps']
    metrics["PE_Ratio"] = yf.Ticker(ticket_stock).info['trailingPE']
    metrics["PBV_Ratio"] = yf.Ticker(ticket_stock).info["bookValue"]
    return metrics



# Title
st.title("interactive financial market data  and comperative analysis".title())
# sidebar creation
st.sidebar.header("users inputs".title())
selected_stock=st.sidebar.text_input("Enter your stock ticket","AAPL").upper()
selected_stock2=st.sidebar.text_input("Enter your stock ticket","TSLA").upper()
start_date=st.sidebar.date_input("Enter the start date",datetime(2025,1,1))
end_date = st.sidebar.date_input("Enter the end date", datetime(2025,2,1))

stock_data1 = get_stock_data(selected_stock,start_date,end_date)
stock_data2=get_stock_data(selected_stock2,start_date,end_date)
sp500 = get_stock_data("^GSPC",start_date,end_date)
BTC = get_stock_data("BTC-USD",start_date,end_date)
# normalizations of stocks and S&P500 closing prices
normalized_stock1= stock_data1['Close']/stock_data1['Close'].iloc[0]*10
normalized_stock2= stock_data2['Close']/stock_data2['Close'].iloc[0]*10
normalized_sp500 = sp500['Close']/sp500['Close'].iloc[0]*10
normalized_BTC = BTC['Close']/BTC['Close'].iloc[0]*10
col1 ,col2 = st.columns(2)


with col1:
    st.subheader(f"Displaying the data for:{selected_stock}")
    st.write(stock_data1)
    st.subheader(f"Graphical representation of {selected_stock} closing prices and financial metrics")
    char_type=st.sidebar.selectbox(f"Select chart for your {selected_stock}",["Bar","line"])
    if char_type=="Bar":
        st.bar_chart(stock_data1["Close"])
    else:
        st.line_chart(stock_data1["Close"])
    if st.button(f"Displaying  metrics of {selected_stock}"):
        st.write(f" Market_cap  of {selected_stock}:{get_metrics(selected_stock)['market_cap']}")
        st.write(f" EPS_Ratio of {selected_stock}:{get_metrics(selected_stock)['EPS_Ratio']}")
        st.write(f" PE_Ratio of {selected_stock}:{get_metrics(selected_stock)['PE_Ratio']}")
        st.write(f" PBV_Ratio of {selected_stock}:{get_metrics(selected_stock)['PBV_Ratio']}")




with col2:
    st.subheader(f"Displaying the data for:{selected_stock2}")
    st.write(stock_data2)
    st.subheader(f"Graphical representation of {selected_stock2} closing prices and financial metrics")
    char_type1 = st.sidebar.selectbox(f"Select chart for your {selected_stock2}",["Bar","Line"])
    if char_type1 == "Bar":
        st.bar_chart(stock_data2["Close"])
    else:
        st.line_chart(stock_data2["Close"])
    if st.button(f"Displaying metrics of {selected_stock2}"):
        st.write(f" Market_cap  of {selected_stock2}:{get_metrics(selected_stock2)['market_cap']}")
        st.write(f" EPS_Ratio of {selected_stock2}:{get_metrics(selected_stock2)['EPS_Ratio']}")
        st.write(f" PE_Ratio of {selected_stock2}:{get_metrics(selected_stock2)['PE_Ratio']}")
        st.write(f" PBV_Ratio of {selected_stock2}:{get_metrics(selected_stock2)['PBV_Ratio']}")


st.subheader(f"Visualization of  {selected_stock}, {selected_stock2} ,  S&P500  and Bitcoin performance efficiency")

data =normalized_stock1.merge(normalized_stock2,on='Date').merge(normalized_sp500,on='Date').merge(normalized_BTC,on='Date')

if st.button('Chart'):
    st.line_chart(data)




st.subheader(f"Financial Analysis")
if st.button("comparative performance".upper()):
    response= client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"""You are a financial assistant that will retrieve four tables of financial market data: two related to stocks and two for the S&P 500 index and BTC respectively. 
                                        Additionally, you will gather some current financial metrics about the stocks and summarize a comparative performance analysis in three parts.
                                        In the first part, you will provide a detailed analysis of the two stocks, highlighting key points and insights.
                                        In the second part, you will analyze the financial metrics and their potential implications for the stocks.
                                        In the third part, you will compare the given stocks with the S&P 500 index and BTC in terms of efficiency and performance and 
                                        finally, Finally, you will conclude with a summary presented in markdown format.BE VERY STRICT ON YOUR OUTPUT. """},
            {"role":"user","content":f"This is the {selected_stock} stock data : {stock_data1} and this is the current metrics {get_metrics(selected_stock)}, this is {selected_stock2} stock data: {stock_data2} , and the {get_metrics(selected_stock2)} , this is the data of {sp500},this is the data of {BTC}"}
        ]
    )
    st.write(response.choices[0].message.content)
import streamlit as st
import yfinance as yf
import requests

# ✅ API 키 설정
FINNHUB_API_KEY = "YOUR_FINNHUB_API_KEY"

# 🎯 페이지 기본 설정
st.set_page_config(
    page_title="미국 주식 분석 요약",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🧭 타이틀 및 설명
st.markdown("<h1 style='text-align: center;'>📊 미국 주식 종합 분석기</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>티커만 입력하면 실적, 목표가, 추천 의견, 리스크 요약까지 한 눈에!</p>", unsafe_allow_html=True)
st.markdown("---")

# 📌 사용자 입력
ticker = st.text_input("🎯 조회할 미국 주식 티커를 입력하세요 (예: AAPL, TSLA)", value="AAPL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        st.markdown("### 💰 기본 정보")
        col1, col2, col3 = st.columns(3)
        col1.metric("현재 주가", f"${info.get('currentPrice')}")
        col2.metric("EPS", info.get('trailingEps'))
        col3.metric("총 매출", f"${info.get('totalRevenue'):,}" if info.get('totalRevenue') else "N/A")

    except Exception as e:
        st.error(f"yFinance 데이터 오류 발생: {e}")

    # 🔍 Finnhub A
import matplotlib.pyplot as plt

# 📈 실적 추이 (EPS 및 수익)
try:
    earnings = stock.earnings  # 연도별 데이터 (DataFrame)
    if not earnings.empty:
        st.markdown("### 🧾 최근 5년간 실적 추이 (Revenue & EPS)")

        # 표로 수치 표시
        st.dataframe(earnings.tail(5).sort_index(ascending=False))

        # 그래프 표시
        fig, ax = plt.subplots()
        ax.bar(earnings.index, earnings['Revenue'] / 1e9, label='Revenue (Billion $)', color='skyblue')
        ax.plot(earnings.index, earnings['Earnings'] / 1e9, label='Earnings (Billion $)', color='orange', marker='o')

        ax.set_xlabel("연도")
        ax.set_ylabel("금액 (단위: 억 달러)")
        ax.set_title("📊 연도별_

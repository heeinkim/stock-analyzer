import streamlit as st
import yfinance as yf
import requests

# ✅ Finnhub API 키 입력
FINNHUB_API_KEY = "YOUR_FINNHUB_API_KEY"

# 🎯 페이지 설정
st.set_page_config(page_title="미국 주식 요약 분석기", layout="centered")

st.title("📊 미국 주식 요약 분석기")
st.markdown("미국 주식의 실적, 목표 주가, 추천 의견, 리스크 요약을 한 눈에 확인하세요.")

# 📌 사용자 입력
ticker = st.text_input("종목 티커를 입력하세요 (예: AAPL, TSLA)", value="AAPL")

if ticker:
    # 🧾 yFinance 데이터
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        st.subheader("💰 기본 정보")
        st.write(f"**현재 주가**: ${info.get('currentPrice')}")
        st.write(f"**EPS (주당순이익)**: {info.get('trailingEps')}")
        st.write(f"**총 매출**: {info.get('totalRevenue')}")

    except Exception as e:
        st.error(f"yFinance 데이터 오류: {e}")

    # 🔍 Finnhub 데이터
    try:
        target_url = f"https://finnhub.io/api/v1/stock/price-target?symbol={ticker}&token={FINNHUB_API_KEY}"
        reco_url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={ticker}&token={FINNHUB_API_KEY}"
        news_url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-01-01&to=2024-12-31&token={FINNHUB_API_KEY}"

        target_data = requests.get(target_url).json()
        reco_data = requests.get(reco_url).json()
        news_data = requests.get(news_url).json()

        st.subheader("🎯 애널리스트 목표가")
        st.write(f"**목표 평균가**: ${target_data.get('targetMean')}")
        st.write(f"상위: ${target_data.get('targetHigh')} / 하위: ${target_data.get('targetLow')}")

        if reco_data:
            rec = reco_data[0]
            st.subheader("✅ 추천 의견")
            st.write(f"Buy: {rec.get('buy')}, Hold: {rec.get('hold')}, Sell: {rec.get('sell')}")

        st.subheader("⚠️ 리스크 요약 (최근 뉴스)")
        for news in news_data[:3]:
            st.write(f"- {news['headline']}")

    except Exception as e:
        st.error(f"Finnhub API 오류: {e}")

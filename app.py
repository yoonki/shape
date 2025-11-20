import streamlit as st
import quantstats as qs
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(page_title="주식 성과 분석 보고서", layout="wide", page_icon="📈")

# 스타일 설정
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 주식 성과 분석 보고서 (QuantStats)")

# 탭 생성
tab1, tab2 = st.tabs(["📊 분석 대시보드", "📚 지표 용어 가이드"])

# --- 탭 1: 분석 대시보드 ---
with tab1:
    # 사이드바 설정 (탭 1에서만 유효한 것처럼 보이지만 실제로는 전역)
    with st.sidebar:
        st.header("⚙️ 분석 설정")
        
        ticker = st.text_input(
            "분석할 주식 티커",
            value="005930.KS",
            help="예: AAPL, MSFT, 005930.KS (삼성전자)"
        ).upper()
        
        benchmark = st.text_input(
            "벤치마크 티커",
            value="SPY",
            help="비교할 지수 또는 주식 (기본값: SPY - S&P 500 ETF)"
        ).upper()
        
        years = st.slider("분석 기간 (년)", 1, 10, 3)
        
        st.markdown("---")
        st.markdown("### ℹ️ 사용법")
        st.markdown("""
        1. **주식 티커** 입력 (한국주식은 .KS/.KQ)
        2. **벤치마크** 입력
        3. **기간** 설정
        4. 결과 확인
        """)

    if ticker:
        try:
            with st.spinner('데이터를 불러오고 분석 중입니다...'):
                # 날짜 계산
                end_date = datetime.now()
                start_date = end_date - timedelta(days=years*365)
                
                # 데이터 다운로드
                # 캐싱을 사용하여 성능 향상 및 반복 호출 방지
                @st.cache_data(ttl=3600)
                def get_data(ticker, period):
                    return qs.utils.download_returns(ticker, period=period)

                stock_data = get_data(ticker, period=f"{years}y")
                
                if benchmark:
                    bench_data = get_data(benchmark, period=f"{years}y")
                else:
                    bench_data = None

                if stock_data is None or len(stock_data) == 0:
                    st.error(f"❌ '{ticker}' 데이터를 찾을 수 없습니다. 티커를 확인해주세요.")
                else:
                    # 1. 주요 지표 카드 표시
                    st.subheader("📊 핵심 성과 지표")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    try:
                        cagr = qs.stats.cagr(stock_data)
                        sharpe = qs.stats.sharpe(stock_data)
                        mdd = qs.stats.max_drawdown(stock_data)
                        volatility = qs.stats.volatility(stock_data)
                        
                        with col1:
                            st.metric("연평균 수익률 (CAGR)", f"{cagr*100:.2f}%", help="매년 평균적으로 성장한 비율")
                        with col2:
                            st.metric("샤프 지수 (Sharpe)", f"{sharpe:.2f}", help="위험 대비 수익률 (높을수록 좋음)")
                        with col3:
                            st.metric("최대 낙폭 (MDD)", f"{mdd*100:.2f}%", help="고점 대비 최대 하락률 (0에 가까울수록 좋음)")
                        with col4:
                            st.metric("연간 변동성", f"{volatility*100:.2f}%", help="주가의 출렁임 정도")
                    except Exception as e:
                        st.warning(f"지표 계산 중 일부 오류가 발생했습니다: {e}")
                    
                    st.markdown("---")
                    
                    # 2. QuantStats 전체 리포트
                    st.subheader("📑 상세 분석 보고서")
                    st.info("아래 보고서는 QuantStats 라이브러리를 통해 생성된 상세 분석 결과입니다. 용어가 어렵다면 '지표 용어 가이드' 탭을 참고하세요.")
                    
                    report_path = "report.html"
                    
                    # 리포트 생성 시 오류 처리
                    try:
                        qs.reports.html(stock_data, benchmark=bench_data, output=report_path, title=f"{ticker} vs {benchmark}" if benchmark else f"{ticker} Analysis", download_filename=report_path)
                        
                        with open(report_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        components.html(html_content, height=1000, scrolling=True)
                        
                        with open(report_path, 'rb') as f:
                            st.download_button(
                                label="📥 보고서 다운로드 (HTML)",
                                data=f,
                                file_name=f"{ticker}_quantstats_report.html",
                                mime="text/html"
                            )
                    except Exception as e:
                        st.error(f"리포트 생성 중 오류가 발생했습니다: {e}")
                        st.warning("데이터가 부족하거나 형식이 맞지 않을 수 있습니다.")

        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
            st.warning("티커가 올바른지, 데이터가 존재하는지 확인해주세요. (예: 삼성전자 -> 005930.KS)")
    else:
        st.info("👈 왼쪽 사이드바에서 분석할 주식 티커를 입력해주세요.")

# --- 탭 2: 지표 용어 가이드 ---
with tab2:
    st.header("📚 QuantStats 리포트 용어 대백과")
    st.markdown("리포트에 등장하는 영어 용어들의 의미를 한국어로 상세히 설명합니다.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 수익률 관련 지표 (Returns)")
        st.markdown("""
        - **Cumulative Return (누적 수익률)**: 투자 시작부터 현재까지의 총 수익률입니다.
        - **CAGR (Compound Annual Growth Rate)**: 연평균 복리 성장률입니다. 매년 평균적으로 자산이 얼마나 불어났는지를 보여줍니다.
        - **Expected Daily/Monthly/Yearly %**: 예상되는 일간/월간/연간 수익률 평균입니다.
        - **Best Day/Month/Year**: 가장 수익률이 좋았던 날/달/해의 수익률입니다.
        - **Worst Day/Month/Year**: 가장 수익률이 나빴던 날/달/해의 수익률입니다.
        - **Win Days/Month/Year %**: 수익을 낸 날/달/해의 비율입니다. (승률)
        """)
        
        st.subheader("🛡️ 위험 관련 지표 (Risk)")
        st.markdown("""
        - **Max Drawdown (MDD)**: 전고점 대비 최대 하락폭입니다. "최악의 경우 이만큼 깨질 수 있다"는 것을 의미합니다.
        - **Volatility (ann.)**: 연간 변동성입니다. 주가가 얼마나 심하게 출렁이는지를 나타냅니다.
        - **Longest DD Days**: 전고점을 회복하기까지 걸린 최장 기간(일)입니다. 원금 회복의 고통스러운 시간을 의미합니다.
        - **Avg. Drawdown**: 평균적인 하락폭입니다.
        - **Avg. Drawdown Days**: 하락 후 회복까지 걸리는 평균 기간입니다.
        - **Value-at-Risk (VaR)**: 특정 확률(보통 95%) 내에서 발생할 수 있는 최대 손실액입니다.
        """)

    with col2:
        st.subheader("⚖️ 위험 조정 수익률 (Risk-Adjusted)")
        st.markdown("""
        - **Sharpe Ratio (샤프 지수)**: (수익률 - 무위험이자율) / 변동성. 위험 1단위당 얻는 초과 수익입니다. **가장 중요한 지표** 중 하나입니다.
            - 1.0 이상: 양호
            - 2.0 이상: 우수
            - 3.0 이상: 탁월
        - **Sortino Ratio (소르티노 지수)**: 샤프 지수와 비슷하지만, 주가 상승 시의 변동성은 무시하고 **하락 위험**만 고려합니다. 투자자 입장에서 더 실질적인 지표일 수 있습니다.
        - **Calmar Ratio**: 연평균 수익률을 MDD로 나눈 값입니다. 큰 하락을 견디면서 얼마나 수익을 냈는지 보여줍니다.
        - **Information Ratio**: 벤치마크 대비 초과 수익을 추적 오차(Tracking Error)로 나눈 값입니다. 벤치마크를 얼마나 안정적으로 이겼는지 보여줍니다.
        """)
        
        st.subheader("📊 기타 통계 지표")
        st.markdown("""
        - **Beta (베타)**: 시장(벤치마크) 민감도입니다.
            - 1.0: 시장과 동일하게 움직임
            - > 1.0: 시장보다 민감하게 움직임 (공격적)
            - < 1.0: 시장보다 둔감하게 움직임 (방어적)
        - **Alpha (알파)**: 시장 수익률로 설명되지 않는 초과 수익입니다. 매니저의 능력을 나타냅니다.
        - **R^2 (결정계수)**: 포트폴리오의 움직임이 벤치마크로 얼마나 설명되는지 나타냅니다. (1에 가까울수록 벤치마크와 비슷하게 움직임)
        - **Kurtosis (첨도)**: 수익률 분포의 뾰족한 정도입니다. 높을수록 극단적인 수익/손실(Fat tail)이 발생할 확률이 높습니다.
        - **Skew (왜도)**: 수익률 분포의 치우침 정도입니다. 양수면 큰 수익의 빈도가, 음수면 큰 손실의 빈도가 높을 수 있습니다.
        - **Kelly Criterion**: 파산을 피하면서 자산을 최대화하기 위한 최적의 투자 비중 공식입니다.
        """)
    
    st.markdown("---")
    st.info("💡 **팁**: 이 가이드를 띄워놓고 '분석 대시보드'의 리포트를 비교해서 보시면 이해하기 쉽습니다.")

# 📈 주식 백테스팅 분석기 (Sharpe Ratio)

샤프 지수(Sharpe Ratio)를 기반으로 주식 거래 전략을 백테스팅하는 Streamlit 애플리케이션입니다.

## 🎯 기능

- **실시간 주식 데이터**: yfinance를 이용한 최신 주식 데이터 자동 수집
- **SMA 크로스오버 전략**: 단순 이동평균 기반 거래 신호 생성
- **Buy & Hold 전략**: 비교를 위한 기본 전략
- **상세 분석 지표**:
  - 샤프 지수 (Sharpe Ratio)
  - 수익률 (Annual Return)
  - 변동성 (Volatility)
  - 최대 낙폭 (Maximum Drawdown)
- **인터랙티브 차트**: Plotly를 이용한 실시간 데이터 시각화
- **거래 신호**: SMA 크로스오버 포인트 표시

## 🚀 빠른 시작

### 방법 1: start.sh 사용 (권장)

```bash
cd "/Users/yoonkilee/Documents/코딩/이윤기/샤프지수"
./start.sh
```

첫 실행 시 자동으로 가상환경을 생성하고 필요한 패키지를 설치합니다.

### 방법 2: 수동 실행

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 📊 사용 방법

1. **티커 입력**: 사이드바에 주식 티커 입력
   - 미국주식: AAPL, MSFT, GOOGL 등
   - 한국주식: 005930.KS (삼성전자) 등

2. **분석 기간 선택**: 분석할 기간을 월 단위로 설정

3. **이동평균 기간**: SMA 크로스오버 전략의 기간 조정

4. **무위험 이율**: 샤프 지수 계산에 사용할 무위험 이율 설정

5. **거래 전략 선택**: SMA 크로스오버 또는 Buy & Hold 선택

## 📈 분석 지표 설명

### 샤프 지수 (Sharpe Ratio)
- 위험 대비 수익의 효율성을 나타냄
- 값이 클수록 좋음
- 공식: (수익률 - 무위험율) / 변동성

### 최대 낙폭 (MDD - Maximum Drawdown)
- 피크에서 저점까지의 최대 하락률
- 작을수록 좋음

### 연 수익률 (Annual Return)
- 연간 기대 수익률

### 연 변동성 (Volatility)
- 수익의 변동성 정도
- 작을수록 안정적

## 📝 라이선스

MIT License

## 🔗 참고 자료

- [Sharpe Ratio 설명](https://log-of.tistory.com/21)
- [yfinance 문서](https://github.com/ranaroussi/yfinance)
- [Streamlit 문서](https://docs.streamlit.io)

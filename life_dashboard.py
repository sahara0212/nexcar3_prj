import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

# ==========================================
# 1. 데이터 생성 (기존 유지)
# ==========================================
def generate_life_data():
    # 데이터 프레임 생성 로직 (동일)
    df_test = pd.DataFrame({
        '시스템': ['기간계', '기간계', '기간계', '기간계', '채널계', '채널계'],
        '업무분류': ['제지급(연금)', '제지급(해약)', '신계약', '입금', 'SFA', '온라인'],
        '전체수량': [842, 500, 600, 270, 986, 300],
        '성공수량': [490, 480, 510, 270, 700, 280],
        '실패수량': [352, 20, 90, 0, 286, 20],
        '실패원인': ['요건불명확(현업)', '데이터미비', '인터페이스오류', '-', '요건변경(현업)', '단순버그'],
        '담당자': ['천개발', '배개발', '송개발', '길개발', '천개발', '배개발']
    })
    df_schedule = pd.DataFrame({
        'Task': ['통테 5차', '인수테스트', '이행리허설', '본이행(Go-Live)'],
        'Start': ['2024-01-29', '2024-02-05', '2024-02-12', '2024-02-19'],
        'Finish': ['2024-02-04', '2024-02-11', '2024-02-18', '2024-02-25'],
        'Resource': ['Testing', 'Biz Check', 'Infra', 'All Hands']
    })
    df_issues = pd.DataFrame({
        '담당자': ['천개발', '배개발', '송개발', '길개발'],
        '할당된_이슈': [30, 15, 12, 5],
        '금일_처리': [2, 5, 4, 3],
        '상태': ['Critical (병목)', 'Warning', 'Normal', 'Idle']
    })
    
    if not os.path.exists('라이프_통합테스트_현황.xlsx'): df_test.to_excel('라이프_통합테스트_현황.xlsx', index=False)
    if not os.path.exists('라이프_오픈공정.xlsx'): df_schedule.to_excel('라이프_오픈공정.xlsx', index=False)
    if not os.path.exists('라이프_이슈리스트.xlsx'): df_issues.to_excel('라이프_이슈리스트.xlsx', index=False)

generate_life_data()

# ==========================================
# 2. 대시보드 UI (5W1H & Action Item 강화)
# ==========================================
st.set_page_config(layout="wide", page_title="라이프차세대 위기관리 타워")

# 스타일링
st.markdown("""
    <style>
    .report-box { background-color: #fff5f5; border: 1px solid #ffcccc; padding: 20px; border-radius: 5px; color: #333; }
    .action-header { font-weight: bold; color: #1f77b4; font-size: 1.1em; }
    .success-box { background-color: #e8f5e9; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 헤더
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🚁 라이프차세대 - Emergency Control Tower")
    st.caption("CEO 보고용 실시간 의사결정 지원 시스템 (Powered by BI Matrix AUD)")
with col_h2:
    st.info(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 데이터 로드
try:
    df_test = pd.read_excel('라이프_통합테스트_현황.xlsx')
    df_schedule = pd.read_excel('라이프_오픈공정.xlsx')
    df_issues = pd.read_excel('라이프_이슈리스트.xlsx')
except:
    st.error("데이터 로딩 중...")
    st.stop()

# --- [섹션 1] 5W1H 원인 규명 리포트 ---
st.markdown("### 1. [Insight] 위기 원인 정밀 진단 (5W1H)")
with st.container():
    st.markdown("""
    <div class="report-box">
        <h4 style="margin-top:0;">🚨 제지급 영역 지연 원인 분석 보고서</h4>
        <ul>
            <li><b>Who (누가):</b> 현업 상품팀(요건) & 수행사 개발팀(구현)</li>
            <li><b>When (언제):</b> 통합테스트 5차 기간 (현재)</li>
            <li><b>Where (어디서):</b> '해약환급금 산출' 및 '연금 개시' 모듈</li>
            <li><b>What (무엇을):</b> 결함 조치율 20%대 정체 (병목 발생)</li>
            <li><b>Why (핵심원인):</b> <span style="color:red; font-weight:bold;">1/20 요건 뒤늦은 확정</span>으로 인한 수정 요청 폭주 (3일간 150건)</li>
            <li><b>How (결과예측):</b> 현 상태 지속 시 <u>본이행 2주(3/18) 지연 불가피</u></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- [섹션 2] 부서별 Action Item & 시뮬레이션 ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("2. [Solution] 부서별 긴급 Action Plan")
    
    # 탭으로 부서별 할 일 정리
    tab1, tab2, tab3 = st.tabs(["🏛️ 전략기획/현업", "💻 IT수행사", "📡 PMO/상황실"])
    
    with tab1:
        st.markdown("**책임자:** 상품본부장 / 계리팀장")
        st.info("✅ **요건 동결 (Freeze):** 금일부로 신규 요건 변경 절대 금지\n\n"
                "✅ **현장 결재:** 매일 09:00/16:00 상황실에서 요건 해석 즉시 판정")
        if st.button("결재: 요건 동결(Freeze) 승인", key='btn_freeze'):
            st.success("시스템에 '요건 동결' 상태가 적용되었습니다. 신규 변경 요청이 차단됩니다.")
            
    with tab2:
        st.markdown("**책임자:** 수행사 PM / 개발리더")
        st.info("✅ **특공대 투입:** 입금 파트(진척 100%) 인력 5명 → 제지급 파트 이관\n\n"
                "✅ **검증 자동화:** 엑셀 수기 검증 → SQL 자동 검증 전환")
        
    with tab3:
        st.markdown("**책임자:** PMO / 품질팀장")
        st.info("✅ **우선순위 조정:** Critical 이슈 100건 선별 집중 관리\n\n"
                "✅ **핫라인 가동:** 대외기관 테스트 시간 24시간 확보")

with c2:
    st.subheader("3. [Simulation] 액션 실행 시 일정 예측")
    
    # 시뮬레이션 로직
    sim_mode = st.radio("시나리오 선택:", ["현재 상태 유지 (Do Nothing)", "Action Plan 전면 가동"], horizontal=True)
    
    sim_df = df_schedule.copy()
    if sim_mode == "Action Plan 전면 가동":
        sim_df['Finish'] = pd.to_datetime(sim_df['Finish']) - timedelta(days=7)
        st.markdown("""
        <div class="success-box">
            <b>🔮 예측 결과:</b><br>
            위 Action Item 수행 시, <b>2월 18일</b> 정상 오픈 가능합니다. (Catch-up 성공)
        </div>
        """, unsafe_allow_html=True)
    else:
        sim_df['Finish'] = pd.to_datetime(sim_df['Finish']) + timedelta(days=14)
        st.markdown("""
        <div style="background-color:#ffebee; padding:10px; border-radius:5px;">
            <b>🔮 예측 결과:</b><br>
            현재 속도 유지 시, <b>3월 4일</b> 이후로 오픈 지연됩니다. (Risk High)
        </div>
        """, unsafe_allow_html=True)

    fig_gantt = px.timeline(sim_df, x_start="Start", x_end="Finish", y="Task", color="Resource", height=300)
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)

# --- [섹션 3] 현황판 ---
st.markdown("---")
st.subheader("4. [Monitoring] 실시간 품질 현황")
col_q1, col_q2 = st.columns([2, 1])

with col_q1:
    df_test['성공률'] = (df_test['성공수량'] / df_test['전체수량'] * 100).round(1)
    st.dataframe(df_test, use_container_width=True, hide_index=True)

with col_q2:
    fig_bar = px.bar(df_issues, x='담당자', y='할당된_이슈', color='상태', title="개발자 부하 현황")
    st.plotly_chart(fig_bar, use_container_width=True)


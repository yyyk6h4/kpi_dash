# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import altair as alt

# --- 1. KPI 계층 구조 데이터 ---
# 사용자가 제공한 kpi_structure 사용
kpi_structure = \
{   '지역전략산업 연계 특성화': {   'G-10 지역전략산업 특성화 대학 육성': [   {   'name': '지역 소재기업 취업률 실적',
                                                          'unit': '건',
                                                          'format': '%d',
                                                          'default_chart_type': 'bar',
                                                          'label_tag': '프로젝트',
                                                          'step': 1},
                                                      {   'name': '지역 주력산업분야 인력양성 실적 향상률',
                                                          'unit': '%',
                                                          'format': '%.1f',
                                                          'default_chart_type': 'line',
                                                          'label_tag': '프로젝트',
                                                          'step': 0.1},
                                                      {   'name': '현장형 수요 맞춤형 교육과정 참여실적',
                                                          'unit': '%',
                                                          'format': '%.1f',
                                                          'default_chart_type': 'line',
                                                          'label_tag': '프로젝트',
                                                          'step': 0.1},
                                                      {   'name': '지산학연 연구건수 및 연구비 규모(교수 1인당 연구건수)',
                                                          'unit': '건',
                                                          'format': '%d',
                                                          'default_chart_type': 'bar',
                                                          'label_tag': '대학',
                                                          'step': 1},
                                                      {   'name': '지산학연 연구건수 및 연구비 규모(교수 1인당 연구비)',
                                                          'unit': '천원',
                                                          'format': '%d',
                                                          'default_chart_type': 'bar_line',
                                                          'label_tag': '대학',
                                                          'step': 1000},
                                                      {   'name': '지산학연 연구 기술이전 실적(건당 수입료)',
                                                          'unit': '천원',
                                                          'format': '%d',
                                                          'default_chart_type': 'bar_line',
                                                          'label_tag': '대학',
                                                          'step': 1000}],
                         '산학연계 중점대학 육성 (연구개발, 인력양성, 산학협력)': {   '대학의 산학친화적 프로그램 운영': [   {   'name': '지역 소재기업 취업률 실적',
                                                                                             'unit': '건',
                                                                                             'format': '%d',
                                                                                             'default_chart_type': 'bar',
                                                                                             'label_tag': '프로젝트',
                                                                                             'step': 1},
                                                                                         {   'name': '현장형 수요 맞춤형 교육과정 참여실적',
                                                                                             'unit': '%',
                                                                                             'format': '%.1f',
                                                                                             'default_chart_type': 'line',
                                                                                             'label_tag': '프로젝트',
                                                                                             'step': 0.1},
                                                                                         {   'name': '지산학연 연구건수 및 연구비 규모(교수 1인당 연구건수)',
                                                                                             'unit': '건',
                                                                                             'format': '%d',
                                                                                             'default_chart_type': 'bar',
                                                                                             'label_tag': '대학',
                                                                                             'step': 1},
                                                                                         {   'name': '지산학연 연구건수 및 연구비 규모(교수 1인당 연구비)',
                                                                                             'unit': '천원',
                                                                                             'format': '%d',
                                                                                             'default_chart_type': 'bar_line',
                                                                                             'label_tag': '대학',
                                                                                             'step': 1000},
                                                                                         {   'name': '지산학연 연구 기술이전 실적(건당 수입료)',
                                                                                             'unit': '천원',
                                                                                             'format': '%d',
                                                                                             'default_chart_type': 'bar_line',
                                                                                             'label_tag': '대학',
                                                                                             'step': 1000}],
                                                                '취업역량 강화 프로그램': [   {   'name': '현장형 수요 맞춤형 교육과정 참여실적',
                                                                                        'unit': '%',
                                                                                        'format': '%.1f',
                                                                                        'default_chart_type': 'line',
                                                                                        'label_tag': '프로젝트',
                                                                                        'step': 0.1},
                                                                                    {   'name': '취업역량 강화 프로그램 참여학생 수',
                                                                                        'unit': '명',
                                                                                        'format': '%d',
                                                                                        'default_chart_type': 'bar',
                                                                                        'label_tag': '프로젝트',
                                                                                        'step': 1},
                                                                                    {   'name': '취업 활성화를 위한 프로그램 운영 실적',
                                                                                        'unit': '건',
                                                                                        'format': '%d',
                                                                                        'default_chart_type': 'bar',
                                                                                        'label_tag': '프로젝트',
                                                                                        'step': 1}]},
                         '공유대학 2.0': [   {   'name': '지역 공유대학 교육과정 운영 실적',
                                             'unit': '건',
                                             'format': '%d',
                                             'default_chart_type': 'bar',
                                             'label_tag': '대학',
                                             'step': 1},
                                         {   'name': '지역 공유대학 교육과정 참여 실적',
                                             'unit': '명',
                                             'format': '%d',
                                             'default_chart_type': 'bar',
                                             'label_tag': '대학',
                                             'step': 1},
                                         {   'name': '공유대학 이수자 취업률',
                                             'unit': '%',
                                             'format': '%.1f',
                                             'default_chart_type': 'line',
                                             'label_tag': '대학',
                                             'step': 0.1}]},
    '지역 연구 특성화': {   '지역연구 중심대학 육성': [   {   'name': '협약기관 취업 연계 실적',
                                             'unit': '건',
                                             'format': '%d',
                                             'default_chart_type': 'bar',
                                             'label_tag': '프로젝트',
                                             'step': 1},
                                         {   'name': '내.외부 우수인력의 유입.순환실적',
                                             'unit': '명',
                                             'format': '%d',
                                             'default_chart_type': 'bar',
                                             'label_tag': '프로젝트',
                                             'step': 1},
                                         {   'name': '외부기관과의 협력연구 실적',
                                             'unit': '건',
                                             'format': '%d',
                                             'default_chart_type': 'bar',
                                             'label_tag': '프로젝트',
                                             'step': 1},
                                         {   'name': '지산학연 연구 건수 및 연구비 규모(교수 1인당 연구 건수)',
                                             'unit': '건',
                                             'format': '%d',
                                             'default_chart_type': 'bar',
                                             'label_tag': '대학',
                                             'step': 1},
                                         {   'name': '지산학연 연구 건수 및 연구비 규모(교수 1인당 연구비)',
                                             'unit': '천원',
                                             'format': '%d',
                                             'default_chart_type': 'bar_line',
                                             'label_tag': '대학',
                                             'step': 1000},
                                         {   'name': '지산학연 연구 기술이전 실적',
                                             'unit': '천원',
                                             'format': '%d',
                                             'default_chart_type': 'bar_line',
                                             'label_tag': '대학',
                                             'step': 1000},
                                         {   'name': '지산학연 연구.개발 지식재산권 실적',
                                             'unit': '건',
                                             'format': '%d',
                                             'default_chart_type': 'bar',
                                             'label_tag': '대학',
                                             'step': 1}],
                     '연구특화 워케이션 클러스터 조성(남해안)': [   {   'name': '협약기관 취업 연계 실적',
                                                       'unit': '건',
                                                       'format': '%d',
                                                       'default_chart_type': 'bar',
                                                       'label_tag': '프로젝트',
                                                       'step': 1},
                                                   {   'name': '내.외부 우수인력의 유입.순환실적',
                                                       'unit': '명',
                                                       'format': '%d',
                                                       'default_chart_type': 'bar',
                                                       'label_tag': '프로젝트',
                                                       'step': 1},
                                                   {   'name': '외부기관과의 협력연구 실적',
                                                       'unit': '건',
                                                       'format': '%d',
                                                       'default_chart_type': 'bar',
                                                       'label_tag': '프로젝트',
                                                       'step': 1},
                                                   {   'name': '지산학연 연구 건수 및 연구비 규모(교수 1인당 연구 건수)',
                                                       'unit': '건',
                                                       'format': '%d',
                                                       'default_chart_type': 'bar',
                                                       'label_tag': '대학',
                                                       'step': 1},
                                                   {   'name': '지산학연 연구 건수 및 연구비 규모(교수 1인당 연구비)',
                                                       'unit': '천원',
                                                       'format': '%d',
                                                       'default_chart_type': 'bar_line',
                                                       'label_tag': '대학',
                                                       'step': 1000},
                                                   {   'name': '지산학연 연구 기술이전 실적',
                                                       'unit': '천원',
                                                       'format': '%d',
                                                       'default_chart_type': 'bar_line',
                                                       'label_tag': '대학',
                                                       'step': 1000},
                                                   {   'name': '지산학연 연구.개발 지식재산권 실적',
                                                       'unit': '건',
                                                       'format': '%d',
                                                       'default_chart_type': 'bar',
                                                       'label_tag': '대학',
                                                       'step': 1}]},
    '평생교육 체계 마련': {   '평생교육 거점대학 육성(권역, 단일형)': {   '경남형 평생교육 공동교육과정 체계 운영': [   {   'name': '성인학습자 고등교육 참여실적',
                                                                                    'unit': '%',
                                                                                    'format': '%.1f',
                                                                                    'default_chart_type': 'line',
                                                                                    'label_tag': '대학',
                                                                                    'step': 0.1},
                                                                                {   'name': '성인친화적 교육과정 개발.운영 실적',
                                                                                    'unit': '%',
                                                                                    'format': '%.1f',
                                                                                    'default_chart_type': 'line',
                                                                                    'label_tag': '프로젝트',
                                                                                    'step': 0.1},
                                                                                {   'name': '성인친화적 교육과정을 통한 인력배출 실적',
                                                                                    'unit': '%',
                                                                                    'format': '%.1f',
                                                                                    'default_chart_type': 'line',
                                                                                    'label_tag': '프로젝트',
                                                                                    'step': 0.1},
                                                                                {   'name': '대학-지역 간 네트워크 구축 및 운영 실적',
                                                                                    'unit': '건',
                                                                                    'format': '%d',
                                                                                    'default_chart_type': 'bar',
                                                                                    'label_tag': '대학',
                                                                                    'step': 1},
                                                                                {   'name': '대학 간 네트워크 구축 및 운영 실적',
                                                                                    'unit': '건',
                                                                                    'format': '%d',
                                                                                    'default_chart_type': 'bar',
                                                                                    'label_tag': '대학',
                                                                                    'step': 1}]},
                      '고등직업교육 거점대학 육성(권역, 단일형)': {   '산업기능인력양성(전문대-시군)': [   {   'name': '거버넌스 구축.운영 추진율',
                                                                                 'unit': '%',
                                                                                 'format': '%.1f',
                                                                                 'default_chart_type': 'line',
                                                                                 'label_tag': '대학',
                                                                                 'step': 0.1},
                                                                             {   'name': '특화분야 연계 교육과정 개발.운영 성과',
                                                                                 'unit': '%',
                                                                                 'format': '%.1f',
                                                                                 'default_chart_type': 'line',
                                                                                 'label_tag': '프로젝트',
                                                                                 'step': 0.1},
                                                                             {   'name': '직업교육 심화과정 이수율',
                                                                                 'unit': '%',
                                                                                 'format': '%.1f',
                                                                                 'default_chart_type': 'line',
                                                                                 'label_tag': '프로젝트',
                                                                                 'step': 0.1},
                                                                             {   'name': '지역 소재기업 취업률 실적',
                                                                                 'unit': '건',
                                                                                 'format': '%d',
                                                                                 'default_chart_type': 'bar',
                                                                                 'label_tag': '프로젝트',
                                                                                 'step': 1}]},
                      '외국인 유학생 유치': {   '외국인 유학생 유치‧지역정주 원스톱 지원': [   {   'name': '외국인 유학생 유치 실적',
                                                                          'unit': '명',
                                                                          'format': '%d',
                                                                          'default_chart_type': 'bar',
                                                                          'label_tag': '프로젝트',
                                                                          'step': 1},
                                                                      {   'name': '외국인 유학생 취업.정주 실적',
                                                                          'unit': '%',
                                                                          'format': '%.1f',
                                                                          'default_chart_type': 'line',
                                                                          'label_tag': '프로젝트',
                                                                          'step': 0.1},
                                                                      {   'name': '산학협력 유학생 역량향상 실적',
                                                                          'unit': '%',
                                                                          'format': '%.1f',
                                                                          'default_chart_type': 'line',
                                                                          'label_tag': '프로젝트',
                                                                          'step': 0.1},
                                                                      {   'name': '외국인 유학생 취업지원 실적',
                                                                          'unit': '%',
                                                                          'format': '%.1f',
                                                                          'default_chart_type': 'line',
                                                                          'label_tag': '프로젝트',
                                                                          'step': 0.1}],
                                        '산업인력 공급형 외국인 유학생 지원': [   {   'name': '외국인 유학생 유치 실적',
                                                                       'unit': '명',
                                                                       'format': '%d',
                                                                       'default_chart_type': 'bar',
                                                                       'label_tag': '프로젝트',
                                                                       'step': 1},
                                                                   {   'name': '외국인 유학생 취업.정주 실적',
                                                                       'unit': '%',
                                                                       'format': '%.1f',
                                                                       'default_chart_type': 'line',
                                                                       'label_tag': '프로젝트',
                                                                       'step': 0.1},
                                                                   {   'name': '산학협력 유학생 역량향상 실적',
                                                                       'unit': '%',
                                                                       'format': '%.1f',
                                                                       'default_chart_type': 'line',
                                                                       'label_tag': '프로젝트',
                                                                       'step': 0.1},
                                                                   {   'name': '외국인 유학생 취업지원 실적',
                                                                       'unit': '%',
                                                                       'format': '%.1f',
                                                                       'default_chart_type': 'line',
                                                                       'label_tag': '프로젝트',
                                                                       'step': 0.1}]}},
    '창업 및 지역문제 해결': {   '창업교육 거점대학 육성': {   '산업인력 공급형 외국인 유학생 지원': [   {   'name': '학생 및 교원 창업실적(창업 건수)',
                                                                             'unit': '건',
                                                                             'format': '%d',
                                                                             'default_chart_type': 'bar',
                                                                             'label_tag': '대학',
                                                                             'step': 1},
                                                                         {   'name': '학생 및 교원 창업실적(창업기업 수익금)',
                                                                             'unit': '천원',
                                                                             'format': '%d',
                                                                             'default_chart_type': 'bar',
                                                                             'label_tag': '대학',
                                                                             'step': 1000},
                                                                         {   'name': '창업 학점 교류제 참여학생 수',
                                                                             'unit': '명',
                                                                             'format': '%d',
                                                                             'default_chart_type': 'bar',
                                                                             'label_tag': '대학',
                                                                             'step': 1},
                                                                         {   'name': '창업동아리 참여학생 수',
                                                                             'unit': '명',
                                                                             'format': '%d',
                                                                             'default_chart_type': 'bar',
                                                                             'label_tag': '프로젝트',
                                                                             'step': 1},
                                                                         {   'name': '대학 간 연계 협력 및 지역사회와의 네트워크 활성화',
                                                                             'unit': '건',
                                                                             'format': '%d',
                                                                             'default_chart_type': 'bar',
                                                                             'label_tag': '프로젝트',
                                                                             'step': 1}]},
                          '지역문제 해결 리빙랩 선도대학 육성': {   '시군 연계형 지역문제 해결사업': [   {   'name': '거버넌스 구축.운영 추진율',
                                                                                 'unit': '%',
                                                                                 'format': '%.1f',
                                                                                 'default_chart_type': 'line',
                                                                                 'label_tag': '대학',
                                                                                 'step': 0.1},
                                                                             {   'name': '대학-지역 간 네트워크 구축 및 운영 실적',
                                                                                 'unit': '건',
                                                                                 'format': '%d',
                                                                                 'default_chart_type': 'bar',
                                                                                 'label_tag': '대학',
                                                                                 'step': 1},
                                                                             {   'name': '대학-지역 간 프로그램 참여인원 수',
                                                                                 'unit': '명',
                                                                                 'format': '%d',
                                                                                 'default_chart_type': 'bar',
                                                                                 'label_tag': '프로젝트',
                                                                                 'step': 1}],
                                                     '기초학문 등 사회참여 리빙랩 분야': [   {   'name': '거버넌스 구축.운영 추진율',
                                                                                   'unit': '%',
                                                                                   'format': '%.1f',
                                                                                   'default_chart_type': 'line',
                                                                                   'label_tag': '대학',
                                                                                   'step': 0.1},
                                                                               {   'name': '대학-지역 간 네트워크 구축 및 운영 실적',
                                                                                   'unit': '건',
                                                                                   'format': '%d',
                                                                                   'default_chart_type': 'bar',
                                                                                   'label_tag': '대학',
                                                                                   'step': 1},
                                                                               {   'name': '대학-지역 간 프로그램 참여인원 수',
                                                                                   'unit': '명',
                                                                                   'format': '%d',
                                                                                   'default_chart_type': 'bar',
                                                                                   'label_tag': '프로젝트',
                                                                                   'step': 1}]}}}

st.set_page_config(layout="wide")
st.title("종합성과지표(KPI) 대시보드") # 제목 변경
st.markdown("---")

def convert_c_to_d3_format(c_format_str, default_d3_format=".2~f"):
    """C-style printf format string을 D3 format string으로 변환 (Altair Tooltip용)"""
    if isinstance(c_format_str, str):
        if c_format_str == '%d':
            return 'd'
        elif '.f' in c_format_str and '%' in c_format_str:
            return c_format_str.replace('%', '') 
    return default_d3_format 

def render_kpi_item_details(kpi_item_info, unique_key_base):
    """개별 KPI 항목을 UI에 렌더링하는 함수"""
    항목_name = kpi_item_info.get("name", "N/A") 
    항목_unit = kpi_item_info.get("unit", "")
    항목_label = kpi_item_info.get("label_tag", "")
    항목_step_orig = kpi_item_info.get("step") 
    항목_format = kpi_item_info.get("format", "%.2f") 
    default_chart = kpi_item_info.get("default_chart_type", "막대")

    label_display = f" <font color='blue'>[{항목_label}]</font>" if 항목_label else "" # 라벨에 색상 추가 (선택사항)
    st.markdown(f"### **{항목_name}**{label_display}", unsafe_allow_html=True)
    st.caption(f"단위: {항목_unit if 항목_unit else '없음'}")
    
    is_int_format = "%d" in 항목_format if isinstance(항목_format, str) else False

    if is_int_format:
        default_step_for_type = 1
        default_value_for_state = 0
    else: 
        default_step_for_type = 0.1
        default_value_for_state = 0.0

    try:
        current_step_val = str(항목_step_orig).strip() if 항목_step_orig is not None else ""
        processed_step = float(current_step_val if current_step_val else default_step_for_type)
        if is_int_format:
            processed_step = int(processed_step)
            if processed_step == 0: processed_step = 1
        elif processed_step == 0.0: 
            processed_step = 0.01 
    except (ValueError, TypeError):
        processed_step = default_step_for_type
    
    chart_options = ["막대", "꺾은선", "막대+꺾은선"]
    chart_type_key = f"{unique_key_base}_chart_type_selection"
    
    current_selection_in_session = st.session_state.get(chart_type_key, default_chart)
    try:
        selected_idx = chart_options.index(current_selection_in_session)
    except ValueError: 
        selected_idx = chart_options.index(default_chart) if default_chart in chart_options else 0
            
    selected_chart_type = st.radio(
        "차트 종류 선택:", # 레이블 명확화
        options=chart_options,
        key=chart_type_key,
        index=selected_idx,
        horizontal=True,
        label_visibility="collapsed" # 차트 바로 위에 있으므로 레이블 숨김 (선택사항)
    )
    
    # --- 데이터 처리 및 그래프 ---
    years_to_input = range(2025, 2031) 
    기준값_key = f"{unique_key_base}_기준값"
    연도별_값_keys = {year: f"{unique_key_base}_{year}값" for year in years_to_input}

    # 기준값 가져오기 및 타입 처리
    기준값_from_state = st.session_state.get(기준값_key, default_value_for_state)
    processed_기준값 = default_value_for_state
    try:
        processed_기준값 = int(float(기준값_from_state)) if is_int_format else float(기준값_from_state)
    except (ValueError, TypeError):
        pass 

    # 연도별 값 가져오기 및 타입 처리
    yearly_data_for_chart = []
    all_input_values_for_has_data_check = [] # 그래프 표시 여부 확인용
    연도별_입력값_dict_processed = {}

    for year in years_to_input:
        연도값_from_state = st.session_state.get(연도별_값_keys[year], default_value_for_state)
        processed_연도값 = default_value_for_state
        try:
            processed_연도값 = int(float(연도값_from_state)) if is_int_format else float(연도값_from_state)
        except (ValueError, TypeError):
            pass
        연도별_입력값_dict_processed[year] = processed_연도값
        yearly_data_for_chart.append({'구분': str(year), '값': processed_연도값})
        all_input_values_for_has_data_check.append(processed_연도값)

    # 그래프 표시 조건 (기준값 또는 연도별 값 중 하나라도 기본값이 아니면 표시)
    has_meaningful_data = (processed_기준값 != default_value_for_state) or \
                           any(val != default_value_for_state for val in all_input_values_for_has_data_check)

    if not has_meaningful_data:
        st.caption("수치를 입력하면 그래프가 표시됩니다.")
    else:
        yearly_display_df = pd.DataFrame(yearly_data_for_chart)
        y_axis_title = f'값 ({항목_unit})' if 항목_unit else '값'
        d3_tooltip_format = convert_c_to_d3_format(항목_format)
        
        # 연도 정렬 순서
        x_axis_sort_order = [str(y) for y in years_to_input]

        layers_to_render = []

        # 연도별 데이터 차트 레이어
        if not yearly_display_df.empty and any(val != default_value_for_state for val in all_input_values_for_has_data_check) : # 연도별 데이터가 있을때만 그림
            base_yearly_chart = alt.Chart(yearly_display_df).encode(
                x=alt.X('구분:N', sort=x_axis_sort_order, title='연도'),
                tooltip=[alt.Tooltip('구분:N', title='연도'), 
                         alt.Tooltip('값:Q', title='값', format=d3_tooltip_format)]
            )
            if selected_chart_type == "막대":
                layers_to_render.append(base_yearly_chart.mark_bar().encode(y=alt.Y('값:Q', title=y_axis_title)))
            elif selected_chart_type == "꺾은선":
                layers_to_render.append(base_yearly_chart.mark_line(point=True).encode(y=alt.Y('값:Q', title=y_axis_title)))
            elif selected_chart_type == "막대+꺾은선":
                layers_to_render.append(base_yearly_chart.mark_bar().encode(y=alt.Y('값:Q', title=y_axis_title)))
                layers_to_render.append(base_yearly_chart.mark_line(color='red', point=True).encode(y=alt.Y('값:Q')))
        
        # 기준값 가로선 레이어 (기준값이 의미있는 경우)
        # (processed_기준값 != default_value_for_state) 조건은 기준값이 초기 기본값과 다를 때만 선을 그림.
        # 만약 0도 의미있는 기준값으로 선을 그리고 싶다면 이 조건 수정 필요.
        if processed_기준값 != default_value_for_state or has_meaningful_data : # 연도별 데이터가 있거나, 기준값이 초기 기본값이 아닐때
            rule_data = pd.DataFrame({'기준선': [processed_기준값]})
            baseline_rule = alt.Chart(rule_data).mark_rule(
                color='firebrick', # 눈에 띄는 색으로 변경
                strokeDash=[4,4], 
                size=2
            ).encode(y='기준선:Q')
            layers_to_render.append(baseline_rule)

        if layers_to_render:
            final_chart = alt.layer(*layers_to_render).resolve_scale(y='shared').properties(height=300)
            st.altair_chart(final_chart, use_container_width=True)
            # 단위 캡션은 차트 아래보다는 항목 정보에 이미 포함되어 있으므로 중복 제거 가능
        elif not has_meaningful_data : # 위에서 이미 처리했지만, 방어적으로 한번 더
            st.caption("수치를 입력하면 그래프가 표시됩니다.")


    # --- 수치 입력 칸 ---
    col_기준값_label, col_기준값_input = st.columns([1,4]) # 너비 비율 조절
    with col_기준값_label:
        # CSS를 사용한 수직 정렬은 복잡하고 깨지기 쉬우므로, st.empty()나 st.markdown("<br>", unsafe_allow_html=True) 등으로 공간 확보 시도
        # 또는 그냥 st.write/markdown 으로 레이블 표시
        st.markdown("<p style='margin-top:28px; text-align:right; font-weight:bold;'>기준값:</p>", unsafe_allow_html=True)
    with col_기준값_input:
        st.number_input(
            label=" ", # 레이블은 위에서 markdown으로 처리했으므로 여기서는 숨김 또는 최소화
            label_visibility="collapsed",
            key=기준값_key,
            value=processed_기준값,
            step=processed_step,
            format=항목_format,
            help=f"단위: {항목_unit}, 변경 단위: {processed_step}"
        )
    
    st.markdown("###### 연도별 목표치")
    num_year_cols = len(years_to_input)
    cols_per_row_for_years = 3 if num_year_cols >= 3 else num_year_cols 
    if cols_per_row_for_years == 0: cols_per_row_for_years = 1 

    for i in range(0, num_year_cols, cols_per_row_for_years):
        year_chunk = list(years_to_input)[i : i + cols_per_row_for_years]
        if not year_chunk: continue

        year_cols = st.columns(len(year_chunk))
        for col_idx, year in enumerate(year_chunk):
            with year_cols[col_idx]:
                st.number_input(
                    label=f"{year}년", 
                    key=연도별_값_keys[year],
                    value=연도별_입력값_dict_processed[year],
                    step=processed_step,
                    format=항목_format
                )
    st.markdown("<br>", unsafe_allow_html=True) # 각 KPI 항목 사이에 간격 추가
    st.markdown("---")


# --- 메인 UI 구성 로직 ---
if not kpi_structure:
    st.error("KPI 구조 데이터(kpi_structure)가 비어있습니다. 데이터를 확인해주세요.")
else:
    대분류_keys = list(kpi_structure.keys())
    if not 대분류_keys:
        st.info("설정된 대분류 KPI가 없습니다.")
    else:
        대분류_tabs_widgets = st.tabs(대분류_keys) 
        
        for i, 대분류_name in enumerate(대분류_keys):
            with 대분류_tabs_widgets[i]:
                st.header(f"{대분류_name}") 
                중분류_data = kpi_structure[대분류_name]
                
                if not 중분류_data:
                    st.info(f"'{대분류_name}'에 해당하는 중간 목표 데이터가 없습니다.")
                    continue

                중분류_keys = list(중분류_data.keys())
                if not 중분류_keys:
                    st.info(f"'{대분류_name}'에 해당하는 중간 목표가 없습니다.")
                    continue
                
                중분류_tabs_widgets = st.tabs(중분류_keys)
                for j, 중분류_name in enumerate(중분류_keys):
                    with 중분류_tabs_widgets[j]:
                        st.subheader(f"{중분류_name}") 
                        
                        소분류_data_or_항목_list = 중분류_data[중분류_name]

                        if isinstance(소분류_data_or_항목_list, dict): 
                            소분류_keys = list(소분류_data_or_항목_list.keys())
                            if not 소분류_keys:
                                st.info(f"'{중분류_name}'에 해당하는 세부 영역(소분류)이 없습니다.")
                                continue
                            
                            소분류_tabs_widgets = st.tabs(소분류_keys)
                            for k, 소분류_name in enumerate(소분류_keys):
                                with 소분류_tabs_widgets[k]:
                                    st.write(f"##### {소분류_name}") 
                                    항목_info_list = 소분류_data_or_항목_list[소분류_name]
                                    if not 항목_info_list:
                                        st.info(f"'{소분류_name}'에 해당하는 핵심 지표(항목)가 아직 없습니다.")
                                        continue
                                    for item_idx, kpi_item_info_dict in enumerate(항목_info_list):
                                        key_base = f"L{i}_M{j}_S{k}_I{item_idx}" 
                                        render_kpi_item_details(kpi_item_info_dict, key_base)
                        
                        elif isinstance(소분류_data_or_항목_list, list): 
                            항목_info_list_direct = 소분류_data_or_항목_list
                            if not 항목_info_list_direct:
                                st.info(f"'{중분류_name}'에 해당하는 핵심 지표(항목)가 아직 없습니다.")
                            else:
                                for item_idx, kpi_item_info_dict in enumerate(항목_info_list_direct):
                                    key_base = f"L{i}_M{j}_direct_I{item_idx}" 
                                    render_kpi_item_details(kpi_item_info_dict, key_base)
                        else:
                            st.error(f"'{중분류_name}' 아래의 데이터 ('{소분류_data_or_항목_list}')는 딕셔너리 또는 리스트여야 합니다.")

st.markdown("---") 
if st.sidebar.checkbox("디버깅: Session State 값 보기", value=False, key="debug_session_state_checkbox"): # 기본값 False로 변경
    st.sidebar.subheader("Session State 현재 값")
    session_state_dict = {key: str(value) for key, value in st.session_state.items()}
    if session_state_dict:
        st.sidebar.json(session_state_dict)
    else:
        st.sidebar.write("세션 상태가 비어있습니다.")
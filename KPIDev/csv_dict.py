# -*- coding: utf-8 -*-
import pandas as pd
import pprint # 예쁘게 출력하기 위한 라이브러리

# --- 설정 (사용자가 자기 환경에 맞게 수정해야 할 수 있는 부분) ---

# 1. CSV 파일 경로: 
#    이 스크립트 파일과 kpi_dic.csv 파일이 같은 폴더에 있다면 'kpi_dic.csv' 그대로 두면 된다.
#    만약 다른 곳에 있다면, 전체 경로를 적어줘야 한다. (예: 'C:/Users/조카/Documents/kpi_dic.csv')
CSV_FILE_PATH = '/Users/yookyeonghoon/Desktop/KPIDev/kpi_dic.csv' 

# 2. CSV 파일 컬럼 이름: 
#    CSV 파일의 첫 번째 줄(헤더)에 있는 컬럼 이름과 정확히 일치해야 한다!
#    (괄호, 띄어쓰기 모두 중요함)
EXPECTED_COL_NAMES = {
    '대분류_col': '대분류',
    '중분류_col': '중분류',
    '소분류_col': '소분류',
    '항목명_col': '항목명 (name)', # 사용자가 제공한 CSV 헤더에 맞춤
    '단위_col': '단위 (unit)',
    '스텝_col': '스텝 (step)',
    '포맷_col': '포맷 (format)',
    '기본차트_col': '기본차트 (default_chart_type)',
    '라벨_col': '라벨 (label_tag)'
}

# 3. 항목 정보의 기본값 (CSV에 값이 비어있을 경우 사용됨)
DEFAULT_UNIT = ""
DEFAULT_STEP = 1.0 
DEFAULT_FORMAT = "%.2f"
DEFAULT_CHART_TYPE = "bar"
DEFAULT_LABEL_TAG = ""
# --- 설정 끝 ---

def create_kpi_structure_from_csv(file_path):
    """CSV 파일을 읽어 kpi_structure 딕셔너리를 생성하는 함수"""
    kpi_structure = {}
    skipped_rows_info = [] # 건너뛴 행 정보를 담을 리스트

    try:
        # CSV 파일 인코딩 처리 (UTF-8 시도 후 안되면 cp949 시도)
        try:
            df = pd.read_csv(file_path, encoding='utf-8', dtype=str) # 모든 컬럼을 문자열로 읽어옴
        except UnicodeDecodeError:
            print(f"정보: '{file_path}' 파일을 UTF-8로 읽기 실패. cp949(한글 Windows) 인코딩으로 다시 시도합니다.")
            df = pd.read_csv(file_path, encoding='cp949', dtype=str)
        
        # 모든 셀의 NaN 값을 빈 문자열로 대체하고, 컬럼명과 데이터의 앞뒤 공백 제거
        df.fillna("", inplace=True)
        df.columns = df.columns.str.strip()
        for col in df.columns:
            df[col] = df[col].str.strip()

        # 설정된 컬럼 이름들이 실제 CSV 헤더에 모두 있는지 확인
        for key, col_name in EXPECTED_COL_NAMES.items():
            if col_name not in df.columns:
                print(f"--- 중요 에러 ---")
                print(f"CSV 파일에 필수 컬럼인 '{col_name}'이(가) 없습니다!")
                print(f"CSV 파일의 첫 번째 줄(헤더)을 확인하여, 다음 이름과 정확히 일치하는지 확인해주세요:")
                print(f"'{EXPECTED_COL_NAMES.values()}'")
                print(f"특히 '{col_name}' 컬럼의 이름이 정확한지 (띄어쓰기, 괄호 등 포함) 확인이 필요합니다.")
                return None, None # 오류 발생 시 None 반환

        # 데이터프레임의 각 행을 순회하며 딕셔너리 구성
        for index, row in df.iterrows():
            대분류 = row[EXPECTED_COL_NAMES['대분류_col']]
            중분류 = row[EXPECTED_COL_NAMES['중분류_col']]
            소분류 = row[EXPECTED_COL_NAMES['소분류_col']]
            항목명 = row[EXPECTED_COL_NAMES['항목명_col']]

            # 필수 값인 대분류, 중분류, 항목명이 없으면 해당 행 건너뛰기
            if not 대분류: # 대분류도 필수라고 가정
                skipped_info = row.to_dict()
                skipped_info['row_index (0-based)'] = index
                skipped_info['reason'] = "대분류 필드가 비어있음"
                skipped_rows_info.append(skipped_info)
                continue
            if not 중분류:
                skipped_info = row.to_dict()
                skipped_info['row_index (0-based)'] = index
                skipped_info['reason'] = "중분류 필드가 비어있음"
                skipped_rows_info.append(skipped_info)
                continue
            if not 항목명:
                skipped_info = row.to_dict()
                skipped_info['row_index (0-based)'] = index
                skipped_info['reason'] = "항목명 필드가 비어있음"
                skipped_rows_info.append(skipped_info)
                continue

            # 항목 정보 딕셔너리 생성
            item_info = {
                "name": 항목명,
                "unit": row.get(EXPECTED_COL_NAMES['단위_col'], DEFAULT_UNIT) or DEFAULT_UNIT, # 비어있으면 기본값
                "format": row.get(EXPECTED_COL_NAMES['포맷_col'], DEFAULT_FORMAT) or DEFAULT_FORMAT,
                "default_chart_type": row.get(EXPECTED_COL_NAMES['기본차트_col'], DEFAULT_CHART_TYPE) or DEFAULT_CHART_TYPE,
                "label_tag": row.get(EXPECTED_COL_NAMES['라벨_col'], DEFAULT_LABEL_TAG) or DEFAULT_LABEL_TAG
            }
            
            # 스텝(step) 값 처리 (숫자 변환, 오류 시 기본값)
            try:
                step_val_str = row.get(EXPECTED_COL_NAMES['스텝_col'], str(DEFAULT_STEP)) # 기본값을 문자열로
                if not step_val_str: # 비어있는 문자열도 기본값으로 처리
                    item_info["step"] = DEFAULT_STEP
                else:
                    step_float = float(step_val_str)
                    item_info["step"] = int(step_float) if step_float.is_integer() else step_float
            except ValueError:
                item_info["step"] = DEFAULT_STEP # 변환 실패 시 기본값

            # 계층 구조에 따라 kpi_structure 딕셔너리 채우기
            current_level = kpi_structure.setdefault(대분류, {})
            
            # 중분류 처리: 소분류 유무에 따라 리스트 또는 딕셔너리로 초기화
            if 중분류 not in current_level:
                current_level[중분류] = [] if not 소분류 else {}
            
            # 소분류 처리
            if 소분류:
                # 소분류가 있는데 중분류 값이 리스트면, 구조가 꼬인 것. (이전 항목은 소분류가 없었다는 뜻)
                # 이런 경우를 대비해, 소분류가 있으면 중분류 값은 무조건 딕셔너리여야 함.
                if not isinstance(current_level[중분류], dict):
                    # print(f"경고: 데이터 구조 불일치! '{대분류}'-'{중분류}'에 소분류 '{소분류}'가 있지만, 이전 항목은 소분류가 없었습니다. 이 중분류는 소분류를 갖는 구조로 처리합니다.")
                    current_level[중분류] = {} # 딕셔너리로 강제 또는 에러 처리
                
                target_list = current_level[중분류].setdefault(소분류, [])
                target_list.append(item_info)
            else: # 소분류가 없는 경우 (중분류 아래 바로 항목 리스트)
                # 소분류가 없는데 중분류 값이 딕셔너리면, 구조가 꼬인 것.
                if not isinstance(current_level[중분류], list):
                    # print(f"경고: 데이터 구조 불일치! '{대분류}'-'{중분류}'에 직접 항목이 있지만, 이전 항목은 소분류를 가졌습니다. 이 중분류는 직접 항목을 갖는 구조로 처리합니다.")
                    current_level[중분류] = [] # 리스트로 강제 또는 에러 처리
                current_level[중분류].append(item_info)
        
        return kpi_structure, skipped_rows_info

    except FileNotFoundError:
        print(f"--- 중요 에러 ---")
        print(f"파일을 찾을 수 없습니다: '{file_path}'")
        print(f"스크립트와 같은 폴더에 '{CSV_FILE_PATH}' 파일이 있는지, 또는 파일 경로가 정확한지 확인해주세요.")
        return None, None
    except ValueError as ve: # 주로 데이터 타입 변환 에러
        print(f"--- 중요 에러 ---")
        print(f"데이터 처리 중 값 관련 에러가 발생했습니다: {ve}")
        print(f"CSV 파일 내용을 확인해주세요. 특히 숫자여야 하는 '스텝 (step)' 같은 컬럼에 이상한 값이 없는지 확인이 필요합니다.")
        return None, None
    except Exception as e: # 그 외 모든 예외
        print(f"--- 중요 에러 ---")
        print(f"알 수 없는 에러가 발생했습니다: {e}")
        print(f"CSV 파일 형식이나 내용, 또는 컬럼 이름이 예상과 다른지 확인해보세요.")
        return None, None

if __name__ == '__main__':
    print(f"정보: '{CSV_FILE_PATH}' 파일을 읽어서 kpi_structure 딕셔너리를 생성합니다...")
    
    final_kpi_structure, skipped_info = create_kpi_structure_from_csv(CSV_FILE_PATH)
    
    # 건너뛴 행 정보 출력
    if skipped_info:
        print("\n--- 다음은 처리 중 건너뛴 행들에 대한 정보입니다 (경고) ---")
        print(f"총 {len(skipped_info)}개 행에서 '대분류', '중분류' 또는 '항목명' 필드가 비어있어서 `kpi_structure`에 포함되지 않았습니다.")
        print("이 항목들을 포함시키려면, CSV 파일에서 해당 필드에 적절한 값을 채워넣어 주십시오.")
        if skipped_info:
            # 건너뛴 첫 번째 항목의 주요 정보만 요약해서 보여주기
            first_skipped_item = skipped_info[0]
            summary = {
                "CSV 행 번호 (대략, 0부터 시작)": first_skipped_item.get('row_index (0-based)', 'N/A'),
                "대분류": first_skipped_item.get(EXPECTED_COL_NAMES['대분류_col'], 'N/A'),
                "중분류": first_skipped_item.get(EXPECTED_COL_NAMES['중분류_col'], 'N/A'),
                "항목명": first_skipped_item.get(EXPECTED_COL_NAMES['항목명_col'], 'N/A'),
                "건너뛴 이유": first_skipped_item.get('reason', 'N/A')
            }
            print("\n예시로 건너뛴 첫 번째 항목의 정보:")
            pprint.pprint(summary, indent=2, width=120)
            if len(skipped_info) > 1:
                print(f"... 외 {len(skipped_info)-1}개의 건너뛴 항목이 더 있습니다 ...")
        print("----------------------------------------------------------\n")

    # 최종 딕셔너리 출력
    if final_kpi_structure is not None: # 함수가 정상적으로 딕셔너리 (비어있을지라도) 또는 None을 반환
        if final_kpi_structure: 
            print("\n--- 생성된 kpi_structure 딕셔너리입니다 ---")
            print("# -*- coding: utf-8 -*-") # 파이썬 파일에 복붙할 때 한글 인식용
            print("kpi_structure = \\")
            # sort_dicts=False 는 Python 3.7+에서 딕셔너리 삽입 순서 유지를 위해 pprint에 전달
            formatted_dict_str = pprint.pformat(final_kpi_structure, indent=4, width=120, sort_dicts=False)
            print(formatted_dict_str)
            print("\n--- 위 내용을 복사해서 파이썬 코드에 사용하세요 ---")
        elif not skipped_info : # 건너뛴 행도 없고, 결과도 없을 때 (예: CSV가 헤더만 있을 때)
             print("정보: CSV 데이터를 처리했지만, 결과 kpi_structure 딕셔너리가 비어있습니다.")
             print("CSV 파일에 처리할 수 있는 데이터가 충분히 있는지 확인해주십시오.")
    else: # create_kpi_structure_from_csv 함수에서 에러로 None이 반환된 경우
        print("\n오류로 인해 kpi_structure를 생성하지 못했습니다. 위에 나온 에러 메시지를 확인해주세요.")
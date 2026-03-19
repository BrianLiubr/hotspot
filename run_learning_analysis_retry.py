# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

DATA_FILE = "/Users/znyj1/Desktop/学情分析报告-演示/测试数据/东平高级中学校本1-1.xls"
BASE_SAVE_DIR = "/Users/znyj1/Desktop/学情分析报告-演示/测试数据/东平高级中学校本1-1"
API_URL = "http://192.168.200.151:9081/v1/workflows/run"
HEADERS = {
    "Authorization": "Bearer app-suxs0SRmNiFztUwVOzfIbrkF",
    "Content-Type": "application/json"
}
BASE_PAYLOAD = {
    "response_mode": "blocking",
    "user": "xiaoyuqi",
    "inputs": {}
}
INTERVAL = 0
TARGET_KEYS = ["data", "report"]

BASE_DIR = Path(BASE_SAVE_DIR)
RUN_TS = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_DIR = BASE_DIR / "_run_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
ABNORMAL_XLSX = LOG_DIR / f"abnormal_rows_{RUN_TS}.xlsx"
SUMMARY_TXT = LOG_DIR / f"summary_{RUN_TS}.txt"
RETRY_SUMMARY_TXT = LOG_DIR / f"retry_summary_{RUN_TS}.txt"


def pick_sys_card_no(row):
    for key in ["系统准考证号", "准考证号", "考号", "准考号"]:
        if key in row and pd.notna(row.get(key)):
            v = str(row.get(key)).strip()
            if v and v.lower() != 'nan':
                return v, key
    return "", ""


def download_file(file_url, save_path, file_name):
    os.makedirs(save_path, exist_ok=True)
    with requests.get(file_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        file_path = os.path.join(save_path, file_name)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return file_path


def process_response(response_json, student_name):
    student_dir = os.path.join(BASE_SAVE_DIR, student_name)
    result_data = response_json.get("data", {})
    outputs = result_data.get("outputs", {}) or {}
    downloaded = []

    for key in TARGET_KEYS:
        file_list = outputs.get(key, [])
        if isinstance(file_list, list):
            for item in file_list:
                file_url = item.get("url")
                file_name = item.get("filename")
                if file_url and file_name:
                    path = download_file(file_url, student_dir, file_name)
                    downloaded.append(path)
    return downloaded, outputs


def run_rows(df, phase_name):
    results = []
    total = len(df)
    for index, row in df.iterrows():
        school_id = str(row.get('学校id', '')).strip()
        student_name = str(row.get('姓名', '')).strip()
        class_name = str(row.get('班级', '')).strip()
        sys_card_no, card_source = pick_sys_card_no(row)

        record = {col: row.get(col, None) for col in df.columns}
        record.update({
            "_phase": phase_name,
            "_row_index": int(index) + 1,
            "_status": "",
            "_reason": "",
            "_http_status": "",
            "_download_count": 0,
            "_downloaded_files": "",
            "_card_source": card_source,
        })

        if not student_name or student_name.lower() == 'nan':
            record["_status"] = "abnormal"
            record["_reason"] = "缺失学生姓名"
            results.append(record)
            continue

        print(f"[{datetime.now().strftime('%H:%M:%S')}] {phase_name} 处理第 {index+1}/{total} 行: {student_name} | {class_name}")

        payload = BASE_PAYLOAD.copy()
        payload["inputs"] = {
            "schoolId": school_id,
            "sysCardNo": sys_card_no,
            "studentName": student_name,
            "className": class_name
        }

        if not sys_card_no:
            record["_status"] = "abnormal"
            record["_reason"] = "缺失准考证号/系统准考证号"
            results.append(record)
            continue

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=300)
            record["_http_status"] = response.status_code
            if response.status_code != 200:
                record["_status"] = "abnormal"
                text = response.text[:1000] if response.text else ""
                record["_reason"] = f"接口错误: HTTP {response.status_code} | {text}"
            else:
                try:
                    res_json = response.json()
                except Exception as e:
                    record["_status"] = "abnormal"
                    record["_reason"] = f"响应非JSON: {e}"
                    results.append(record)
                    continue

                try:
                    downloaded, outputs = process_response(res_json, student_name)
                    record["_download_count"] = len(downloaded)
                    record["_downloaded_files"] = "\n".join(downloaded)
                    if len(downloaded) == 0:
                        record["_status"] = "abnormal"
                        record["_reason"] = f"未发现可下载文件; outputs keys={list(outputs.keys())}"
                    else:
                        record["_status"] = "success"
                except Exception as e:
                    record["_status"] = "abnormal"
                    record["_reason"] = f"解析/下载失败: {e}"
        except Exception as e:
            record["_status"] = "abnormal"
            record["_reason"] = f"请求异常: {e}"

        results.append(record)
        time.sleep(INTERVAL)

    return pd.DataFrame(results)


def write_summary(path, title, df):
    total = len(df)
    abnormal = len(df[df['_status'] == 'abnormal']) if total else 0
    success = len(df[df['_status'] == 'success']) if total else 0
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n")
        f.write(f"数据文件: {DATA_FILE}\n")
        f.write(f"输出目录: {BASE_SAVE_DIR}\n")
        f.write(f"总行数: {total}\n成功: {success}\n异常: {abnormal}\n\n")
        if abnormal:
            f.write("异常明细:\n")
            for _, row in df[df['_status'] == 'abnormal'].iterrows():
                f.write(f"- 第{row['_row_index']}行 {row.get('姓名','')} | 原因: {row['_reason']}\n")


def main():
    print(f"读取数据文件: {DATA_FILE}")
    if DATA_FILE.endswith('.csv'):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.read_excel(DATA_FILE)
    df.columns = df.columns.astype(str).str.strip()
    print(f"读取成功: {len(df)} 行, 列: {list(df.columns)}")

    first_df = run_rows(df, 'first_run')
    write_summary(SUMMARY_TXT, '首次运行摘要', first_df)

    abnormal_df = first_df[first_df['_status'] == 'abnormal'].copy()
    if len(abnormal_df):
        export_cols = list(df.columns) + ['_phase','_row_index','_reason','_http_status','_card_source']
        abnormal_df[export_cols].to_excel(ABNORMAL_XLSX, index=False)
        print(f"异常数据已导出: {ABNORMAL_XLSX}")
    else:
        print("首次运行无异常数据。")

    if len(abnormal_df):
        retry_input = abnormal_df[df.columns].copy()
        retry_df = run_rows(retry_input, 'retry_run')
        write_summary(RETRY_SUMMARY_TXT, '异常数据重跑摘要', retry_df)
        retry_abnormal = retry_df[retry_df['_status'] == 'abnormal'].copy()
        retry_abnormal_xlsx = LOG_DIR / f"abnormal_rows_after_retry_{RUN_TS}.xlsx"
        if len(retry_abnormal):
            export_cols = list(df.columns) + ['_phase','_row_index','_reason','_http_status','_card_source']
            retry_abnormal[export_cols].to_excel(retry_abnormal_xlsx, index=False)
            print(f"重跑后仍异常的数据已导出: {retry_abnormal_xlsx}")
        else:
            print("异常数据重跑后全部成功。")
    print("全部执行完成。")
    print(f"日志目录: {LOG_DIR}")

if __name__ == '__main__':
    main()

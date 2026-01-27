#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取和清洗脚本
自动从API获取数据，清洗后保存为JSON
"""

import sys
import io
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from io import BytesIO

# 设置标准输出编码为UTF-8（兼容Windows）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API配置
API_URL = 'http://blchat.ksbao.com:8001/api/events/export_v2?type=xls'

# 排除的测试ID列表
EXCLUDE_IDS = [
    'trial-e5b50d8e-3856-49d4-8633-2a67f41923ce',
    'trial-e21c6843-aea3-4910-ac71-9aff35dc91e1',
    'trial-2b26b557-4022-44ad-9cb1-f58b3f495468',
    'trial-2da1f8c6-6f9e-40a4-a528-73ffc3b448d5',
    'trial-2f87736a-0290-42a7-b4a3-f613c97ae1d4',
    'trial-7b89c5d1-1e5c-43ab-b3fd-639765f9673c',
    'trial-ca39a16e-5bf4-4343-9a2e-4d9bfb2f958f',
    'trial-0855ab37-8162-4796-ad94-a5c50d59496a',
    'trial-958b9b91-bd45-4e1a-aadf-6f3b075cee26',
    'trial-4e1078af-2d27-46f5-9ec0-f0d471739d9b',
    'trial-4f494b3a-dc0c-4060-bfc9-0b668698e0ff',
    'trial-b63973da-6d4c-4115-a2f1-6acf5c046895',
    'trial-3d5b5e7c-987d-4046-be68-39c7ba6ca430',
    'trial-abac2152-7833-40f0-8f65-b37de1456ee3',
    'trial-0a91baac-888a-4d27-a7c5-8077c73389e1',
    'trial-9396417e-5275-4449-98c0-e770d2c116a0',
    'a277d75e-ffee-45ff-94bf-9a6026506444',
    'da8106e5-2185-466e-bf6d-40ad88eeaa08',
    '5808ec25-e74e-4d54-821c-891079f42de8',
    '493a1fbb-d2d6-45a2-a161-3abea8d97265',
    'a4cb4615-b699-4356-940b-010d739b1ea1',
    '824c588c-a177-4737-95c6-9b94cb1aa5c9'
]

def fetch_data():
    """从API获取数据"""
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 开始获取数据...')
    print(f'API地址: {API_URL}')

    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()

        print(f'✓ API响应成功: {response.status_code}')
        print(f'✓ 数据大小: {len(response.content) / 1024:.2f} KB')

        return response.content
    except Exception as e:
        print(f'✗ 数据获取失败: {e}')
        raise

def clean_data(excel_data):
    """清洗数据"""
    print('\n开始清洗数据...')

    # 读取Excel
    df = pd.read_excel(BytesIO(excel_data))
    print(f'✓ 原始数据: {len(df)}行, {df["user_id"].nunique()}个用户')

    # 排除测试ID
    df = df[~df['user_id'].isin(EXCLUDE_IDS)]
    print(f'✓ 排除测试ID后: {len(df)}行, {df["user_id"].nunique()}个用户')

    # 排除ksbaoUserId为空
    df = df[df['ksbaoUserId'].notna()]
    print(f'✓ 排除空ksbaoUserId后: {len(df)}行, {df["user_id"].nunique()}个用户')

    # 转换时间格式
    df['time'] = pd.to_datetime(df['time'])

    print(f'✓ 数据时间范围: {df["time"].min()} 至 {df["time"].max()}')

    return df

def save_data(df):
    """保存数据为JSON"""
    print('\n开始保存数据...')

    # 转换为JSON格式（处理时间字段和NaN值）
    data_dict = df.to_dict('records')
    for record in data_dict:
        # 处理时间字段
        if isinstance(record['time'], pd.Timestamp):
            record['time'] = record['time'].isoformat()

        # 将 NaN 值替换为 None（JSON中的null）
        for key, value in list(record.items()):
            if pd.isna(value):
                record[key] = None

    # 保存最新数据
    output_file = 'data/latest.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'updateTime': datetime.now().isoformat(),
            'dataCount': len(data_dict),
            'userCount': df['user_id'].nunique(),
            'timeRange': {
                'start': df['time'].min().isoformat(),
                'end': df['time'].max().isoformat()
            },
            'data': data_dict
        }, f, ensure_ascii=False, indent=2)

    print(f'✓ 数据已保存到: {output_file}')
    print(f'  - 记录数: {len(data_dict)}')
    print(f'  - 用户数: {df["user_id"].nunique()}')

    # 同时保存一份带时间戳的历史数据
    history_file = f'data/history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False)
    print(f'✓ 历史数据已保存到: {history_file}')

def main():
    """主函数"""
    print('=' * 60)
    print('AI病例研习平台 - 数据获取和清洗')
    print('=' * 60)

    try:
        # 1. 获取数据
        excel_data = fetch_data()

        # 2. 清洗数据
        df = clean_data(excel_data)

        # 3. 保存数据
        save_data(df)

        print('\n' + '=' * 60)
        print('✓ 数据处理完成！')
        print('=' * 60)

        return 0

    except Exception as e:
        print('\n' + '=' * 60)
        print(f'✗ 处理失败: {e}')
        print('=' * 60)
        return 1

if __name__ == '__main__':
    exit(main())

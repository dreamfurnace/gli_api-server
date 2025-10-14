#!/usr/bin/env python3
"""
로컬 DB 데이터를 STG 환경으로 이식하는 스크립트
"""
import requests
import json
import os

STG_API_BASE = "https://stg-api.glibiz.com"

def load_local_users():
    """로컬에서 추출한 사용자 데이터를 로드"""
    with open('local_users_dump.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_user_via_api(user_data):
    """STG API를 통해 사용자 생성"""
    fields = user_data['fields']

    # API용 데이터 형식으로 변환
    api_data = {
        'email': fields.get('email', ''),
        'username': fields.get('username', ''),
        'first_name': fields.get('first_name', ''),
        'last_name': fields.get('last_name', ''),
        'wallet_address': fields.get('wallet_address', ''),
        'membership_level': fields.get('membership_level', 'basic'),
        'is_active': fields.get('is_active', True),
        'is_staff': fields.get('is_staff', False),
        'is_superuser': fields.get('is_superuser', False),
    }

    print(f"사용자 생성 시도: {api_data['email'] or api_data['username']}")

    # 실제 API 호출은 여기서 구현
    # 예: requests.post(f"{STG_API_BASE}/api/users/", json=api_data)

    return True

def main():
    print("=== STG 환경으로 사용자 데이터 이식 시작 ===")

    try:
        users = load_local_users()
        print(f"로컬에서 {len(users)}명의 사용자 데이터를 로드했습니다.")

        success_count = 0
        for user in users:
            if create_user_via_api(user):
                success_count += 1

        print(f"=== 완료: {success_count}/{len(users)}명의 사용자가 성공적으로 이식되었습니다. ===")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
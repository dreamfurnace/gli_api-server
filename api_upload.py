#!/usr/bin/env python3
import requests
import json

STG_BASE_URL = "https://stg-api.glibiz.com"

def load_user_data():
    with open('local_users_dump.json', 'r') as f:
        return json.load(f)

def create_user_via_api(user_data):
    """API를 통해 사용자 직접 생성"""
    fields = user_data['fields']

    # 회원가입 데이터 준비
    user_payload = {
        'email': fields.get('email', ''),
        'username': fields.get('username', ''),
        'first_name': fields.get('first_name', ''),
        'last_name': fields.get('last_name', ''),
        'wallet_address': fields.get('wallet_address'),
        'membership_level': fields.get('membership_level', 'basic'),
        'is_active': True,
        'password': 'TempPassword123!'  # 임시 비밀번호
    }

    # API 요청
    try:
        response = requests.post(f"{STG_BASE_URL}/api/members/",
                               json=user_payload,
                               timeout=10)

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code in [200, 201]:
            print(f"✅ 성공: {user_payload['email']}")
            return True
        else:
            print(f"❌ 실패: {user_payload['email']} - {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 오류: {e}")
        return False

def main():
    print("=== STG API를 통한 사용자 생성 시작 ===")

    users_data = load_user_data()
    success_count = 0

    for user_data in users_data:
        fields = user_data['fields']
        email = fields.get('email', fields.get('username', 'Unknown'))

        print(f"\n🔄 생성 시도: {email}")

        if create_user_via_api(user_data):
            success_count += 1

    print(f"\n=== 결과: {success_count}/{len(users_data)}명 성공 ===")

if __name__ == "__main__":
    main()
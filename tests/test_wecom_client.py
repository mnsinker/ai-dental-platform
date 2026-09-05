from integrations.wecom.client import get_access_token

def test_get_access_token():
    token = get_access_token()

    assert token
    print("access_token 获取成功")

if __name__ == '__main__':
    test_get_access_token()
from django.test import TestCase, Client
from unittest.mock import patch

from users.views import KakaoAPI

class KakaoSignInTest(TestCase):
    @patch.object(KakaoAPI, "request_user_info")
    @patch.object(KakaoAPI, "request_access_token")
    def test_kakao_signin_request_access_token(self, mocked_token, mocked_kakao_user_info):
        client = Client()

        class MockedToken:
            def json(self):
                return {"access_token" : "XYZ123"}

        class MockedKakaoUserInformation:
            def json(self):
                return {
                    "id" : 123456789,
                    "kakao_account" : {
                        "email" : 'lo123@gmail.com'
                    },
                    "properties" : {
                        "nickname" : 'onbin'
                    }
                }

        mocked_token.return_value           = MockedToken().json()
        mocked_kakao_user_info.return_value = MockedKakaoUserInformation().json()
        response                            = client.get('/users/signin/kakao')

        self.assertEqual(response.status_code, 200)
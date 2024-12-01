from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from django.conf import settings

RATE_API_KEY = 'L2S1VakQkMnlHxoJWjgWvvWHCoxvjcy1'

@api_view(['GET'])
def api_test(request):
    URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': RATE_API_KEY,
        # 'searchdate' : '20150101',
        'data': 'AP01'
    }
    
    # SSL 인증서 검증 비활성화
    response = requests.get(URL, params=params, verify=False).json()
    print('----')
    print(response)
    print('---r---')
    
    return JsonResponse({'response': response})

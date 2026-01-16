#!/usr/bin/env python3
import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import json

BASE_URL = "https://carproject.duckdns.org"

def test_homepage_response():
    """홈페이지 응답 시간 테스트"""
    times = []
    for i in range(10):
        start = time.time()
        response = requests.get(BASE_URL)
        end = time.time()
        times.append(end - start)
        print(f"Request {i+1}: {response.status_code} - {(end-start)*1000:.2f}ms")
    
    print(f"\n홈페이지 응답 시간:")
    print(f"평균: {statistics.mean(times)*1000:.2f}ms")
    print(f"최소: {min(times)*1000:.2f}ms")
    print(f"최대: {max(times)*1000:.2f}ms")
    return times

def test_api_endpoint():
    """API 엔드포인트 응답 시간 테스트"""
    url = f"{BASE_URL}/api/logs/"
    times = []
    for i in range(5):
        start = time.time()
        response = requests.get(url)
        end = time.time()
        times.append(end - start)
        print(f"API Request {i+1}: {response.status_code} - {(end-start)*1000:.2f}ms")
    
    print(f"\nAPI 응답 시간:")
    print(f"평균: {statistics.mean(times)*1000:.2f}ms")
    return times

def concurrent_test(num_users=5):
    """동시 사용자 테스트"""
    def single_request():
        start = time.time()
        response = requests.get(BASE_URL)
        end = time.time()
        return end - start, response.status_code
    
    print(f"\n{num_users}명 동시 접속 테스트:")
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = [executor.submit(single_request) for _ in range(num_users)]
        results = [future.result() for future in futures]
    
    times = [result[0] for result in results]
    statuses = [result[1] for result in results]
    
    print(f"성공률: {statuses.count(200)}/{len(statuses)}")
    print(f"평균 응답시간: {statistics.mean(times)*1000:.2f}ms")
    print(f"최대 응답시간: {max(times)*1000:.2f}ms")

if __name__ == "__main__":
    print("🚀 CarLogoDetection 성능 테스트 시작\n")
    
    # 1. 홈페이지 응답 시간
    test_homepage_response()
    
    # 2. API 응답 시간  
    test_api_endpoint()
    
    # 3. 동시 접속 테스트
    concurrent_test(5)
    concurrent_test(10)
    
    print("\n✅ 테스트 완료")

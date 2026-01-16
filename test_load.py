#!/usr/bin/env python3
import requests
import time
import threading
from datetime import datetime
import json

BASE_URL = "https://carproject.duckdns.org"

class LoadTester:
    def __init__(self):
        self.results = []
        self.errors = []
        self.lock = threading.Lock()
    
    def single_request(self, user_id):
        """단일 요청 실행"""
        try:
            start = time.time()
            response = requests.get(BASE_URL, timeout=10)
            end = time.time()
            
            with self.lock:
                self.results.append({
                    'user_id': user_id,
                    'response_time': end - start,
                    'status_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            with self.lock:
                self.errors.append({
                    'user_id': user_id,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    def ramp_up_test(self, max_users=20, duration=60):
        """점진적 사용자 증가 테스트"""
        print(f"🔄 Ramp-up 테스트: {max_users}명까지 {duration}초간")
        
        threads = []
        start_time = time.time()
        
        for user_id in range(max_users):
            # 점진적으로 사용자 추가
            if time.time() - start_time < duration:
                thread = threading.Thread(target=self.continuous_requests, args=(user_id, duration))
                threads.append(thread)
                thread.start()
                time.sleep(duration / max_users)  # 균등하게 분산
        
        # 모든 스레드 완료 대기
        for thread in threads:
            thread.join()
        
        self.print_results()
    
    def continuous_requests(self, user_id, duration):
        """지속적인 요청 생성"""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.single_request(user_id)
            time.sleep(1)  # 1초마다 요청
    
    def burst_test(self, num_requests=50):
        """버스트 테스트 (동시 대량 요청)"""
        print(f"💥 버스트 테스트: {num_requests}개 동시 요청")
        
        threads = []
        for i in range(num_requests):
            thread = threading.Thread(target=self.single_request, args=(i,))
            threads.append(thread)
        
        # 모든 요청 동시 시작
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        print(f"총 소요시간: {total_time:.2f}초")
        self.print_results()
    
    def print_results(self):
        """결과 출력"""
        if not self.results:
            print("❌ 결과 없음")
            return
        
        response_times = [r['response_time'] for r in self.results]
        success_count = len([r for r in self.results if r['status_code'] == 200])
        
        print(f"\n📊 테스트 결과:")
        print(f"총 요청: {len(self.results)}")
        print(f"성공: {success_count}")
        print(f"실패: {len(self.errors)}")
        print(f"성공률: {success_count/len(self.results)*100:.1f}%")
        print(f"평균 응답시간: {sum(response_times)/len(response_times)*1000:.2f}ms")
        print(f"최소 응답시간: {min(response_times)*1000:.2f}ms")
        print(f"최대 응답시간: {max(response_times)*1000:.2f}ms")
        
        if self.errors:
            print(f"\n❌ 에러 목록:")
            for error in self.errors[:5]:  # 처음 5개만 표시
                print(f"  - {error['error']}")
        
        # 결과 초기화
        self.results = []
        self.errors = []

if __name__ == "__main__":
    tester = LoadTester()
    
    print("🚀 CarLogoDetection 로드 테스트 시작\n")
    
    # 1. 버스트 테스트
    tester.burst_test(20)
    
    print("\n" + "="*50 + "\n")
    
    # 2. 점진적 증가 테스트
    tester.ramp_up_test(10, 30)
    
    print("\n✅ 로드 테스트 완료")

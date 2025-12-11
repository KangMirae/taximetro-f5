import time
import logging

class Taximeter:
    def __init__(self, rates):
        self.rates = rates
        self.total_fare = 0.0
        self.is_running = False      # 여정 시작 여부
        self.current_state = None    # '1'(이동), '2'(정지) 등
        self.last_update_time = 0.0  # 마지막으로 상태가 바뀐 시간

    def start_journey(self):
        """여정 시작"""
        self.is_running = True
        self.total_fare = 0.0
        self.current_state = '1'  # 기본적으로 이동하며 시작 (혹은 선택 가능)
        self.last_update_time = time.time()
        logging.info("Journey started.")

    def change_state(self, new_state):
        """상태 변경 (이동 <-> 정지) 시 요금 정산"""
        if not self.is_running:
            return

        now = time.time()
        duration = now - self.last_update_time
        
        # 이전 상태에 대한 요금 계산 및 추가
        rate = self.rates.get(self.current_state, 0.0)
        segment_fare = duration * rate
        self.total_fare += segment_fare

        logging.info(f"State: {self.current_state}->{new_state}, Duration: {duration:.2f}s, Added: {segment_fare:.2f}")

        # 상태 업데이트
        self.current_state = new_state
        self.last_update_time = now

    def stop_journey(self):
        """여정 종료 및 최종 계산"""
        if not self.is_running:
            return 0.0
            
        # 마지막 구간 계산
        self.change_state("ENDED") 
        self.is_running = False
        
        logging.info(f"Journey finished. Total Fare: {self.total_fare:.2f}")
        return self.total_fare
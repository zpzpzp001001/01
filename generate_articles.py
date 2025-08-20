#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기존 기사를 복사하여 새로운 날짜로 기사 생성하는 스크립트
17일~21일까지 하루 10개씩 총 50개 기사 생성
"""

import os
import random
import re
from datetime import datetime, timedelta
import shutil
import hashlib

def generate_hash():
    """8자리 랜덤 해시 생성"""
    return hashlib.md5(str(random.random()).encode()).hexdigest()[:8]

def get_existing_articles(directory):
    """기존 기사 파일 목록 가져오기"""
    articles = []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            articles.append(os.path.join(directory, filename))
    return articles

def update_article_content(content, new_date, new_hash, new_filename):
    """기사 내용에서 날짜와 해시, URL 업데이트"""
    # 날짜 업데이트
    content = re.sub(r'date: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+09:00', 
                     f'date: {new_date}T{random.randint(9,19):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}+09:00', 
                     content)
    
    # 해시 업데이트
    content = re.sub(r'hash: [a-f0-9]{8}', f'hash: {new_hash}', content)
    
    # URL과 slug 업데이트 (파일명에서 .md 제거)
    base_name = new_filename.replace('.md', '')
    content = re.sub(r'url: "/automotive/[^"]*"', f'url: "/automotive/{base_name}/"', content)
    content = re.sub(r'slug: "[^"]*"', f'slug: "{base_name}"', content)
    
    return content

def create_new_articles(source_dir, target_dates, articles_per_day=10):
    """새로운 기사들 생성"""
    existing_articles = get_existing_articles(source_dir)
    
    if len(existing_articles) < articles_per_day:
        print(f"경고: 기존 기사가 {len(existing_articles)}개뿐입니다.")
        return
    
    total_created = 0
    
    for date_str in target_dates:
        print(f"{date_str} 기사 {articles_per_day}개 생성 중...")
        
        # 해당 날짜에 사용할 기사들을 랜덤 선택
        selected_articles = random.sample(existing_articles, articles_per_day)
        
        for i, source_file in enumerate(selected_articles):
            try:
                # 원본 파일 읽기
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 새로운 파일명 생성 (원본 파일명에 날짜 접미사 추가)
                base_name = os.path.basename(source_file).replace('.md', '')
                new_filename = f"{base_name}-{date_str.replace('-', '')}.md"
                new_filepath = os.path.join(source_dir, new_filename)
                
                # 파일이 이미 존재하는지 확인
                if os.path.exists(new_filepath):
                    print(f"파일이 이미 존재합니다: {new_filename}")
                    continue
                
                # 새로운 해시 생성
                new_hash = generate_hash()
                
                # 내용 업데이트
                updated_content = update_article_content(content, date_str, new_hash, new_filename)
                
                # 새 파일 저장
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                total_created += 1
                print(f"  생성: {new_filename}")
                
            except Exception as e:
                print(f"오류 발생 ({source_file}): {e}")
    
    print(f"\n총 {total_created}개 기사가 생성되었습니다.")

def main():
    # 기사 디렉토리 경로
    articles_dir = "content/automotive"
    
    # 생성할 날짜 목록 (2025-08-17 ~ 2025-08-21)
    target_dates = [
        "2025-08-17",
        "2025-08-18", 
        "2025-08-19",
        "2025-08-20",
        "2025-08-21"
    ]
    
    # 하루에 생성할 기사 수
    articles_per_day = 10
    
    print("=== 기사 자동 생성 스크립트 ===")
    print(f"대상 기간: {target_dates[0]} ~ {target_dates[-1]}")
    print(f"일일 생성 기사 수: {articles_per_day}개")
    print(f"총 생성 예정 기사 수: {len(target_dates) * articles_per_day}개")
    print()
    
    # 기사 생성 실행
    create_new_articles(articles_dir, target_dates, articles_per_day)
    
    print("\n기사 생성이 완료되었습니다!")

if __name__ == "__main__":
    main()
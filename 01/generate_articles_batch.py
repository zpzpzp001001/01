#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기존 기사를 복사하여 제목을 변형하고 새로운 날짜로 기사 생성하는 스크립트
22일~25일까지 하루 10개씩 총 40개 기사 생성
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
    """기존 기사 파일 목록 가져오기 (날짜 접미사가 없는 원본 기사들만)"""
    articles = []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            # 날짜 패턴이 없는 원본 파일들만 선택 (20250817 같은 패턴이 없는 것)
            if not re.search(r'-\d{8}\.md$', filename):
                articles.append(os.path.join(directory, filename))
    return articles

def modify_title(title):
    """제목을 약간 변형하는 함수"""
    title_variations = [
        # 따옴표 패턴 변경
        lambda t: t.replace('"', "'") if '"' in t else t.replace("'", '"'),
        
        # 감탄사 추가/제거
        lambda t: t + "!" if not t.endswith("!") else t[:-1],
        
        # 연결어 변경
        lambda t: t.replace("그런데", "하지만").replace("하지만", "그런데"),
        lambda t: t.replace("또한", "그리고").replace("그리고", "또한"),
        lambda t: t.replace("따라서", "그래서").replace("그래서", "따라서"),
        
        # 어미 변경
        lambda t: t.replace("했다", "됐다").replace("됐다", "했다"),
        lambda t: t.replace("한다", "된다").replace("된다", "한다"),
        lambda t: t.replace("이다", "다").replace("다", "이다") if t.endswith("이다") or t.endswith("다") else t,
        
        # 조사 변경
        lambda t: t.replace("에서", "에게").replace("에게", "에서"),
        lambda t: t.replace("으로", "로").replace("로", "으로"),
        
        # 순서/위치 표현 변경
        lambda t: t.replace("첫", "최초").replace("최초", "첫"),
        lambda t: t.replace("마지막", "최종").replace("최종", "마지막"),
        
        # 숫자 표현 변경
        lambda t: t.replace("1위", "첫째").replace("첫째", "1위"),
        lambda t: t.replace("2위", "둘째").replace("둘째", "2위"),
        
        # 시제 변경
        lambda t: t.replace("될 예정", "예정").replace("예정", "될 예정") if "예정" in t else t,
        
        # 의문문/평서문 전환
        lambda t: t + "?" if not t.endswith("?") and random.random() < 0.3 else t,
        lambda t: t[:-1] if t.endswith("?") and random.random() < 0.3 else t,
    ]
    
    # 랜덤하게 1-3개의 변형 적용
    num_changes = random.randint(1, 3)
    selected_changes = random.sample(title_variations, min(num_changes, len(title_variations)))
    
    modified = title
    for change_func in selected_changes:
        try:
            modified = change_func(modified)
        except:
            continue
    
    # 너무 길거나 짧은 제목은 원본 사용
    if len(modified) < 10 or len(modified) > 200:
        return title
    
    return modified

def update_article_content(content, new_date, new_hash, new_filename):
    """기사 내용에서 날짜, 해시, URL, 제목 업데이트"""
    # 제목 추출 및 변형
    title_match = re.search(r'title: "([^"]*)"', content)
    if title_match:
        original_title = title_match.group(1)
        modified_title = modify_title(original_title)
        content = content.replace(f'title: "{original_title}"', f'title: "{modified_title}"')
    
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
    
    print(f"사용 가능한 원본 기사: {len(existing_articles)}개")
    
    if len(existing_articles) < articles_per_day:
        print(f"경고: 기존 기사가 {len(existing_articles)}개뿐입니다.")
        # 부족한 경우 중복 선택 허용
    
    total_created = 0
    
    for date_str in target_dates:
        print(f"{date_str} 기사 {articles_per_day}개 생성 중...")
        
        # 해당 날짜에 사용할 기사들을 랜덤 선택 (중복 허용)
        if len(existing_articles) >= articles_per_day:
            selected_articles = random.sample(existing_articles, articles_per_day)
        else:
            # 부족한 경우 중복해서 선택
            selected_articles = [random.choice(existing_articles) for _ in range(articles_per_day)]
        
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
                    print(f"  파일이 이미 존재합니다: {new_filename}")
                    continue
                
                # 새로운 해시 생성
                new_hash = generate_hash()
                
                # 내용 업데이트 (제목 변형 포함)
                updated_content = update_article_content(content, date_str, new_hash, new_filename)
                
                # 새 파일 저장
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                total_created += 1
                print(f"  생성: {new_filename}")
                
            except Exception as e:
                print(f"  오류 발생 ({source_file}): {e}")
    
    print(f"\n총 {total_created}개 기사가 생성되었습니다.")

def main():
    # 기사 디렉토리 경로
    articles_dir = "content/automotive"
    
    # 생성할 날짜 목록 (2025-08-22 ~ 2025-08-25)
    target_dates = [
        "2025-08-22",
        "2025-08-23", 
        "2025-08-24",
        "2025-08-25"
    ]
    
    # 하루에 생성할 기사 수
    articles_per_day = 10
    
    print("=== 기사 자동 생성 스크립트 (제목 변형 버전) ===")
    print(f"대상 기간: {target_dates[0]} ~ {target_dates[-1]}")
    print(f"일일 생성 기사 수: {articles_per_day}개")
    print(f"총 생성 예정 기사 수: {len(target_dates) * articles_per_day}개")
    print("제목 변형: 활성화")
    print()
    
    # 현재 디렉토리 확인
    if not os.path.exists(articles_dir):
        print(f"오류: 디렉토리가 존재하지 않습니다: {articles_dir}")
        return
    
    # 기사 생성 실행
    create_new_articles(articles_dir, target_dates, articles_per_day)
    
    print("\n기사 생성이 완료되었습니다!")

if __name__ == "__main__":
    main()
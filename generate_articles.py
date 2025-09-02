import os
import random
from datetime import datetime, timedelta

# 브랜드별 키워드
brands = ['BMW', '벤츠', '아우디', '토요타', '현대', '기아', '제네시스', '테슬라', '볼보', '혼다', '포르쉐', '렉서스']

# 주제별 템플릿
topics = [
    {
        'title_template': 'AI 기반 자율주행, {brand} 브랜드 최신 모델에 적용',
        'description_template': '자율주행 기술의 급속한 발전으로 {brand}은/는 레벨 {level} 자율주행 시스템을 량산차에 적용했다.\n\n이 시스템은 {brand}가지 센서를 통해 주변 환경을 실시간으로 분석하며, {accuracy}% 이상의 정확도를 보인다.\n\n특히 도심 주행에서의 안전성이 크게 향상되어 교통사고 위험을 {reduction}% 이상 줄일 수 있다...',
        'content_template': '자율주행 기술의 급속한 발전으로 {brand}은/는 레벨 {level} 자율주행 시스템을 량산차에 적용했다.\n\n이 시스템은 {brand}가지 센서를 통해 주변 환경을 실시간으로 분석하며, {accuracy}% 이상의 정확도를 보인다.\n\n특히 도심 주행에서의 안전성이 크게 향상되어 교통사고 위험을 {reduction}% 이상 줄일 수 있다.\n\n향후 {years}년 내에 완전 자율주행 단계로 발전할 것으로 예상된다고 전문가들은 전망했다.\n\n소비자 조사 결과, 해당 모델에 대한 관심도가 전월 대비 {interest}% 상승한 것으로 나타났다.'
    },
    {
        'title_template': 'SUV 시장 판도 변화, {brand} 모델이 {segment} 부문 1위 달성',
        'description_template': '국내 SUV 시장에서 {brand}은/는 전년 대비 {growth}% 성장한 판매실적을 기록했다.\n\n특히 {brand} 세그먼트에서 뛰어난 상품성으로 소비자들의 높은 관심을 받고 있다.\n\n{brand}만원대 가격으로 프리미엄 기능들을 제공하여 가성비 측면에서 경쟁우위를 확보했다...',
        'content_template': '국내 SUV 시장에서 {brand}은/는 전년 대비 {growth}% 성장한 판매실적을 기록했다.\n\n특히 {brand} 세그먼트에서 뛰어난 상품성으로 소비자들의 높은 관심을 받고 있다.\n\n{brand}만원대 가격으로 프리미엄 기능들을 제공하여 가성비 측면에서 경쟁우위를 확보했다.\n\n업계에서는 이러한 트렌드가 {brand}년까지 지속될 것으로 전망하고 있다.\n\n향후 글로벌 시장 진출도 계획하고 있어 {brand}의 해외 경쟁력 강화에도 기여할 것으로 예상된다.'
    },
    {
        'title_template': '{brand} 전기차 혁신적인 배터리 기술로 주행거리 {range} 달성',
        'description_template': '{brand}가 개발한 신형 배터리 기술은 1회 충전으로 최대 {range}km 주행이 가능하다.\n\n이는 기존 {brand} 전기차 대비 {improvement}% 향상된 성능으로, 전기차 시장에 새로운 기준을 제시했다.\n\n특히 고속 충전 기능이 크게 개선되어 30분 내 80% 충전이 가능하다...',
        'content_template': '{brand}가 개발한 신형 배터리 기술은 1회 충전으로 최대 {range}km 주행이 가능하다.\n\n이는 기존 {brand} 전기차 대비 {improvement}% 향상된 성능으로, 전기차 시장에 새로운 기준을 제시했다.\n\n특히 고속 충전 기능이 크게 개선되어 30분 내 80% 충전이 가능하다.\n\n배터리 수명도 기존 대비 {lifespan}% 연장되어 장기 사용 시 경제성을 크게 개선했다.\n\n업계에서는 이 기술이 전기차 대중화에 크게 기여할 것으로 평가하고 있다.'
    },
    {
        'title_template': '대형 SUV 수요 증가, {brand} 브랜드 신모델 출시 계획',
        'description_template': '프리미엄 대형 SUV 시장의 성장에 맞춰 {brand}가 새로운 모델 출시를 예고했다.\n\n이번 신모델은 {brand}의 최신 디자인 철학과 첨단 기술이 집약된 플래그십 모델이다.\n\n특히 7인승 구조와 럭셔리한 내장재로 프리미엄 고객층을 타겟으로 한다...',
        'content_template': '프리미엄 대형 SUV 시장의 성장에 맞춰 {brand}가 새로운 모델 출시를 예고했다.\n\n이번 신모델은 {brand}의 최신 디자인 철학과 첨단 기술이 집약된 플래그십 모델이다.\n\n특히 7인승 구조와 럭셔리한 내장재로 프리미엄 고객층을 타겟으로 한다.\n\n예상 출시가는 {price}억원대로 경쟁 모델 대비 합리적인 가격대를 형성할 예정이다.\n\n사전 예약 결과 이미 {preorder}건 이상의 주문이 접수되어 높은 관심을 보여주고 있다.'
    },
    {
        'title_template': '럭셔리 SUV 시장 경쟁 심화, {brand1} vs {brand2} 비교분석',
        'description_template': '프리미엄 SUV 시장에서 {brand1}과 {brand2}의 경쟁이 치열해지고 있다.\n\n{brand1} 모델은 성능과 연비에서, {brand2} 모델은 디자인과 편의성에서 각각 강점을 보이고 있다.\n\n가격대별로 세분화된 전략으로 고객 선택의 폭이 넓어졌다...',
        'content_template': '프리미엄 SUV 시장에서 {brand1}과 {brand2}의 경쟁이 치열해지고 있다.\n\n{brand1} 모델은 성능과 연비에서, {brand2} 모델은 디자인과 편의성에서 각각 강점을 보이고 있다.\n\n가격대별로 세분화된 전략으로 고객 선택의 폭이 넓어졌다.\n\n업계 분석에 따르면 올해 해당 세그먼트 판매량이 전년 대비 {growth}% 증가할 것으로 예상된다.\n\n소비자들은 브랜드별 특성을 고려해 신중한 선택을 하고 있는 것으로 나타났다.'
    },
    {
        'title_template': '친환경 자동차 시대, {brand} 브랜드가 제시하는 미래상',
        'description_template': '탄소중립 시대에 맞춰 {brand}가 친환경 모빌리티 비전을 발표했다.\n\n2030년까지 전체 라인업의 {percentage}%를 전동화 차량으로 전환한다는 계획이다.\n\n특히 수소연료전지와 배터리 전기차를 동시에 개발해 다양한 선택권을 제공한다...',
        'content_template': '탄소중립 시대에 맞춰 {brand}가 친환경 모빌리티 비전을 발표했다.\n\n2030년까지 전체 라인업의 {percentage}%를 전동화 차량으로 전환한다는 계획이다.\n\n특히 수소연료전지와 배터리 전기차를 동시에 개발해 다양한 선택권을 제공한다.\n\n이를 위해 향후 5년간 {investment}조원을 투자할 예정이라고 발표했다.\n\n환경부와의 협력을 통해 충전 인프라 확충에도 적극 참여할 계획이다.'
    },
    {
        'title_template': '소형 SUV 인기 상승, 젊은층 타겟 {brand} 모델 주목',
        'description_template': '20-30대 젊은 소비자층을 겨냥한 {brand}의 소형 SUV가 큰 인기를 끌고 있다.\n\n합리적인 가격과 실용적인 공간 설계로 도심형 라이프스타일에 최적화되었다.\n\n특히 연비 성능이 {fuel_efficiency}km/L로 경제성 면에서도 우수한 평가를 받고 있다...',
        'content_template': '20-30대 젊은 소비자층을 겨냥한 {brand}의 소형 SUV가 큰 인기를 끌고 있다.\n\n합리적인 가격과 실용적인 공간 설계로 도심형 라이프스타일에 최적화되었다.\n\n특히 연비 성능이 {fuel_efficiency}km/L로 경제성 면에서도 우수한 평가를 받고 있다.\n\n젊은층이 선호하는 스마트 기능과 커넥티비티 옵션이 풍부하게 제공된다.\n\n출시 3개월 만에 {sales}대의 판매량을 기록하며 시장의 뜨거운 반응을 보여주고 있다.'
    },
    {
        'title_template': '자율주행차 안전성 테스트 결과, {brand} 모델이 최고 등급',
        'description_template': '국제 자율주행 안전성 평가에서 {brand} 모델이 {rating}등급을 획득했다.\n\n이는 {brand}의 첨단 센서 기술과 AI 알고리즘의 우수성을 입증하는 결과다.\n\n특히 돌발상황 대응 능력에서 {response_time}초의 빠른 반응속도를 보였다...',
        'content_template': '국제 자율주행 안전성 평가에서 {brand} 모델이 {rating}등급을 획득했다.\n\n이는 {brand}의 첨단 센서 기술과 AI 알고리즘의 우수성을 입증하는 결과다.\n\n특히 돌발상황 대응 능력에서 {response_time}초의 빠른 반응속도를 보였다.\n\n테스트 과정에서 {scenarios}가지 시나리오를 모두 성공적으로 통과했다.\n\n안전성 전문가들은 이 결과가 자율주행 기술 상용화에 중요한 이정표가 될 것이라고 평가했다.'
    },
    {
        'title_template': '자율주행 기술 상용화 임박, {brand} 레벨 {level} 시스템 도입',
        'description_template': '{brand}가 레벨 {level} 자율주행 시스템의 상용화 일정을 공개했다.\n\n이 시스템은 고속도로에서 완전 무인 주행이 가능한 수준의 기술력을 보유하고 있다.\n\n특히 악천후나 복잡한 교통상황에서도 안정적인 성능을 발휘한다...',
        'content_template': '{brand}가 레벨 {level} 자율주행 시스템의 상용화 일정을 공개했다.\n\n이 시스템은 고속도로에서 완전 무인 주행이 가능한 수준의 기술력을 보유하고 있다.\n\n특히 악천후나 복잡한 교통상황에서도 안정적인 성능을 발휘한다.\n\n정부 인증 과정을 거쳐 {year}년 하반기 출시 예정이라고 발표했다.\n\n이로써 {brand}는 자율주행 기술 분야에서 선두 그룹에 합류하게 되었다.'
    },
    {
        'title_template': '스마트 교통시스템과 연계된 자율주행 기술 발전 현황',
        'description_template': 'V2X(Vehicle to Everything) 기술을 활용한 스마트 교통시스템이 자율주행차 성능 향상에 기여하고 있다.\n\n교통신호, 도로 인프라와의 실시간 통신으로 더욱 안전하고 효율적인 주행이 가능해졌다.\n\n특히 교차로에서의 사고 위험이 {reduction}% 감소하는 효과를 보였다...',
        'content_template': 'V2X(Vehicle to Everything) 기술을 활용한 스마트 교통시스템이 자율주행차 성능 향상에 기여하고 있다.\n\n교통신호, 도로 인프라와의 실시간 통신으로 더욱 안전하고 효율적인 주행이 가능해졌다.\n\n특히 교차로에서의 사고 위험이 {reduction}% 감소하는 효과를 보였다.\n\n국토교통부는 전국 주요 도로에 V2X 인프라를 확대 설치할 계획이라고 밝혔다.\n\n이러한 기술 발전으로 완전 자율주행 시대가 {timeline}년 앞당겨질 것으로 전망된다.'
    },
    {
        'title_template': '전기차 충전 인프라 확충, {brand} 지역 {locations}개소 신설 예정',
        'description_template': '전기차 보급 확산에 따라 {brand} 전용 충전소가 전국 {locations}개 지역에 신설된다.\n\n각 충전소는 초고속 충전기 {chargers}기를 설치하여 대기시간을 최소화할 예정이다.\n\n특히 고속도로 휴게소와 대형 마트를 중심으로 접근성을 높였다...',
        'content_template': '전기차 보급 확산에 따라 {brand} 전용 충전소가 전국 {locations}개 지역에 신설된다.\n\n각 충전소는 초고속 충전기 {chargers}기를 설치하여 대기시간을 최소화할 예정이다.\n\n특히 고속도로 휴게소와 대형 마트를 중심으로 접근성을 높였다.\n\n충전 요금도 기존 대비 {discount}% 할인된 요금으로 제공하여 경제적 부담을 줄였다.\n\n이로써 {brand} 전기차 사용자들의 충전 편의성이 크게 개선될 것으로 기대된다.'
    },
    {
        'title_template': '전기차 시장의 새로운 변화, {brand} 모델이 주목받는 이유',
        'description_template': '최근 전기차 시장에서 {brand} 모델이 주목받고 있는 이유는 혁신적인 기술력에 있다.\n\n특히 배터리 효율성과 충전 속도 면에서 경쟁사 대비 우수한 성능을 보이고 있다.\n\n소비자 만족도 조사에서도 {satisfaction}점의 높은 점수를 기록했다...',
        'content_template': '최근 전기차 시장에서 {brand} 모델이 주목받고 있는 이유는 혁신적인 기술력에 있다.\n\n특히 배터리 효율성과 충전 속도 면에서 경쟁사 대비 우수한 성능을 보이고 있다.\n\n소비자 만족도 조사에서도 {satisfaction}점의 높은 점수를 기록했다.\n\n디자인과 성능을 모두 만족시키는 균형잡힌 제품력이 시장에서 인정받고 있다.\n\n향후 출시 예정인 신모델들도 이러한 기술력을 바탕으로 더욱 발전된 모습을 보여줄 것으로 기대된다.'
    }
]

authors = ['김민수', '이수진', '박성호', '최민우', '한지민', '정다은', '윤서준', '장민지', '오태현', '신예진']

def generate_hash():
    return ''.join(random.choices('0123456789abcdef', k=8))

def generate_article(date_str, index, topic_template, brand_data):
    # 날짜 객체 생성
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    
    # 시간 생성 (08:00 ~ 23:59)
    hour = random.randint(8, 23)
    minute = random.randint(0, 59)
    time_str = f"{hour:02d}:{minute:02d}:00+09:00"
    
    # 작성자 랜덤 선택
    author = random.choice(authors)
    
    # 제목과 내용 생성
    title = topic_template['title_template'].format(**brand_data)
    description = topic_template['description_template'].format(**brand_data)
    content = topic_template['content_template'].format(**brand_data)
    
    # 파일명 생성 (제목을 URL 친화적으로 변환)
    slug = title.replace(' ', '-').replace(',', '').replace(':', '').replace('(', '').replace(')', '').replace('/', '-').replace('%', '')
    filename = f"{slug}-{date_str}-{index:02d}.md"
    
    # URL과 slug 생성
    url = f"/automotive/{slug}-{date_str}-{index:02d}/"
    slug_final = f"{slug}-{date_str}-{index:02d}"
    
    # 메타데이터 생성
    metadata = f"""---
title: "{title}"
description: "{description[:150]}..."
date: {date_obj.strftime('%Y-%m-%d')}T{time_str}
author: "{author}"
categories: ['automotive']
tags: ['뉴스', '이슈', '자동차', '기술', '시장동향']
hash: {generate_hash()}
source_url: "https://example-news-site.com/article-{generate_hash()}"
url: "{url}"
slug: "{slug_final}"
type: "post"
layout: "single"
draft: false
---

{content}"""
    
    return filename, metadata

def generate_brand_data(topic_template, brand=None):
    """주제에 맞는 브랜드별 데이터 생성"""
    if not brand:
        brand = random.choice(brands)
    
    data = {'brand': brand}
    
    # 모든 템플릿에서 사용될 수 있는 기본값들 설정
    template_text = topic_template['title_template'] + topic_template['description_template'] + topic_template['content_template']
    
    if 'level' in template_text:
        data['level'] = random.choice(['2', '3', '4', '5'])
    if 'accuracy' in template_text:
        data['accuracy'] = random.randint(85, 95)
    if 'reduction' in template_text:
        data['reduction'] = random.randint(25, 45)
    if 'years' in template_text:
        data['years'] = random.choice(['2', '3', '4', '5'])
    if 'interest' in template_text:
        data['interest'] = random.randint(35, 65)
    if 'segment' in template_text:
        data['segment'] = random.choice(['2', '3', '4', '5'])
    if 'growth' in template_text:
        data['growth'] = random.randint(15, 55)
    if 'range' in template_text:
        data['range'] = random.choice(['350km', '420km', '500km', '580km', '650km'])
    if 'improvement' in template_text:
        data['improvement'] = random.randint(15, 35)
    if 'lifespan' in template_text:
        data['lifespan'] = random.randint(20, 40)
    if 'price' in template_text:
        data['price'] = random.choice(['6', '7', '8', '9', '10'])
    if 'preorder' in template_text:
        data['preorder'] = random.randint(500, 2000)
    if 'brand1' in template_text:
        brand1 = random.choice(brands)
        remaining_brands = [b for b in brands if b != brand1]
        brand2 = random.choice(remaining_brands)
        data['brand1'] = brand1
        data['brand2'] = brand2
    if 'percentage' in template_text:
        data['percentage'] = random.choice(['70', '80', '85', '90'])
    if 'investment' in template_text:
        data['investment'] = random.choice(['5', '7', '10', '12', '15'])
    if 'fuel_efficiency' in template_text:
        data['fuel_efficiency'] = random.choice(['12.5', '13.2', '14.1', '15.3', '16.2'])
    if 'sales' in template_text:
        data['sales'] = random.randint(1500, 5000)
    if 'rating' in template_text:
        data['rating'] = random.choice(['A+', 'A', 'S급'])
    if 'response_time' in template_text:
        data['response_time'] = random.choice(['0.3', '0.4', '0.5'])
    if 'scenarios' in template_text:
        data['scenarios'] = random.randint(50, 100)
    if 'year' in template_text:
        data['year'] = random.choice(['2025', '2026'])
    if 'timeline' in template_text:
        data['timeline'] = random.choice(['2', '3', '5'])
    if 'locations' in template_text:
        data['locations'] = random.choice(['4', '5', '6', '7', '8'])
    if 'chargers' in template_text:
        data['chargers'] = random.choice(['6', '8', '10', '12'])
    if 'discount' in template_text:
        data['discount'] = random.randint(10, 30)
    if 'satisfaction' in template_text:
        data['satisfaction'] = random.choice(['8.5', '8.7', '8.9', '9.1', '9.3'])
    
    return data

def main():
    # 9월 2일과 3일 각각 10개씩 생성
    dates = ['20250902', '20250903']
    
    for date in dates:
        print(f"\n{date} 날짜의 기사 10개 생성 중...")
        
        # 이미 사용된 조합을 추적
        used_combinations = set()
        
        for i in range(1, 11):
            # 중복 방지를 위한 시도
            attempts = 0
            while attempts < 50:  # 무한 루프 방지
                topic = random.choice(topics)
                brand_data = generate_brand_data(topic)
                
                # 조합 키 생성 (제목 + 주요 브랜드)
                combination_key = (topic['title_template'], brand_data.get('brand', ''), brand_data.get('brand1', ''))
                
                if combination_key not in used_combinations:
                    used_combinations.add(combination_key)
                    break
                attempts += 1
            
            # 파일 생성
            filename, content = generate_article(date, i, topic, brand_data)
            filepath = os.path.join('content', 'automotive', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"생성 완료: {filename}")
    
    print("\n모든 기사 생성이 완료되었습니다!")

if __name__ == "__main__":
    main()
// News Processor - 뉴스 관련 기능 처리
// 자동차, 경제, 엔터테인먼트 뉴스 사이트용

document.addEventListener('DOMContentLoaded', function() {
    initializeNewsProcessor();
});

function initializeNewsProcessor() {
    console.log('[NewsProcessor] Initializing...');
    
    // 뉴스 카테고리 처리
    initializeNewsCategories();
    
    // 뉴스 이미지 로딩 처리
    initializeNewsImages();
    
    // 뉴스 카드 호버 효과
    initializeNewsCardEffects();
    
    // 뉴스 검색 기능
    initializeNewsSearch();
    
    // 뉴스 필터 기능
    initializeNewsFilters();
    
    console.log('[NewsProcessor] Initialization complete');
}

// 뉴스 카테고리 처리
function initializeNewsCategories() {
    const categoryButtons = document.querySelectorAll('.category-filter');
    
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            filterNewsByCategory(category);
        });
    });
}

// 카테고리별 뉴스 필터링
function filterNewsByCategory(category) {
    const newsItems = document.querySelectorAll('.news-item');
    
    newsItems.forEach(item => {
        const itemCategory = item.getAttribute('data-category');
        
        if (category === 'all' || itemCategory === category) {
            item.style.display = 'block';
            item.classList.add('fade-in');
        } else {
            item.style.display = 'none';
            item.classList.remove('fade-in');
        }
    });
}

// 뉴스 이미지 로딩 처리
function initializeNewsImages() {
    const newsImages = document.querySelectorAll('.news-image img');
    
    newsImages.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });
        
        img.addEventListener('error', function() {
            console.log('[NewsProcessor] Image load error:', this.src);
            this.src = '/images/placeholder-news.jpg';
            this.classList.add('error');
        });
    });
}

// 뉴스 카드 호버 효과
function initializeNewsCardEffects() {
    const newsCards = document.querySelectorAll('.news-card');
    
    newsCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover-effect');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover-effect');
        });
    });
}

// 뉴스 검색 기능
function initializeNewsSearch() {
    const searchInput = document.getElementById('news-search');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            searchNews(searchTerm);
        });
    }
}

// 뉴스 검색 실행
function searchNews(searchTerm) {
    const newsItems = document.querySelectorAll('.news-item');
    
    newsItems.forEach(item => {
        const title = item.querySelector('.news-title')?.textContent.toLowerCase() || '';
        const description = item.querySelector('.news-description')?.textContent.toLowerCase() || '';
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            item.style.display = 'block';
            item.classList.add('search-match');
        } else {
            item.style.display = 'none';
            item.classList.remove('search-match');
        }
    });
}

// 뉴스 필터 기능
function initializeNewsFilters() {
    const filterButtons = document.querySelectorAll('.news-filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 활성 버튼 상태 변경
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // 필터 적용
            const filterType = this.getAttribute('data-filter');
            applyNewsFilter(filterType);
        });
    });
}

// 뉴스 필터 적용
function applyNewsFilter(filterType) {
    const newsItems = document.querySelectorAll('.news-item');
    
    newsItems.forEach(item => {
        const itemDate = new Date(item.getAttribute('data-date'));
        const now = new Date();
        let shouldShow = true;
        
        switch(filterType) {
            case 'today':
                shouldShow = isToday(itemDate);
                break;
            case 'week':
                shouldShow = isThisWeek(itemDate);
                break;
            case 'month':
                shouldShow = isThisMonth(itemDate);
                break;
            case 'all':
            default:
                shouldShow = true;
                break;
        }
        
        if (shouldShow) {
            item.style.display = 'block';
            item.classList.add('filter-match');
        } else {
            item.style.display = 'none';
            item.classList.remove('filter-match');
        }
    });
}

// 날짜 유틸리티 함수들
function isToday(date) {
    const today = new Date();
    return date.toDateString() === today.toDateString();
}

function isThisWeek(date) {
    const today = new Date();
    const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
    return date >= weekAgo && date <= today;
}

function isThisMonth(date) {
    const today = new Date();
    return date.getMonth() === today.getMonth() && date.getFullYear() === today.getFullYear();
}

// 뉴스 관련 유틸리티 함수들
function formatNewsDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('ko-KR', options);
}

function getNewsCategory(section) {
    const categories = {
        'automotive': '자동차',
        'economy': '경제',
        'entertainment': '엔터테인먼트'
    };
    return categories[section] || '기타';
}

function getCategoryIcon(section) {
    const icons = {
        'automotive': 'fas fa-car',
        'economy': 'fas fa-chart-line',
        'entertainment': 'fas fa-star'
    };
    return icons[section] || 'fas fa-newspaper';
}

// 뉴스 공유 기능
function shareNews(title, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        }).catch(console.error);
    } else {
        // 폴백: 클립보드에 복사
        navigator.clipboard.writeText(url).then(() => {
            showNotification('링크가 클립보드에 복사되었습니다.');
        });
    }
}

// 알림 표시
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'news-notification';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 전역 함수로 노출
window.NewsProcessor = {
    filterByCategory: filterNewsByCategory,
    searchNews: searchNews,
    shareNews: shareNews,
    formatDate: formatNewsDate,
    getCategoryIcon: getCategoryIcon
};

console.log('[NewsProcessor] Module loaded successfully'); 
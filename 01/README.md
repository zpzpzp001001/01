# 넷파일즈 - 자동차 경제 전문매체

자동차, 전기차, 모빌리티 정보와 경제 분석을 전문적으로 다루는 넷파일즈 자동차 경제 전문매체입니다.

## 🚀 Cloudflare Pages 자동 배포 설정

### 자동 배포 프로세스
1. **GitHub에 푸시** → **Cloudflare Pages 자동 감지** → **Hugo 빌드** → **자동 배포**
2. 새로운 기사를 `content/` 폴더에 추가하고 커밋/푸시하면 자동으로 사이트가 업데이트됩니다.

### Cloudflare Pages 설정 방법

#### 1. Cloudflare Pages 프로젝트 생성
1. Cloudflare Dashboard → Pages → "Create a project"
2. "Connect to Git" 선택 → GitHub 리포지토리 연결
3. 빌드 설정:
   - **Build command**: `hugo --minify --gc`
   - **Build output directory**: `public`
   - **Root directory**: `/` (루트)

#### 2. 환경 변수 설정
**Production 환경**:
```
HUGO_VERSION=0.147.9
HUGO_ENV=production
HUGO_ENVIRONMENT=production
NODE_VERSION=18
```

**Preview 환경**:
```
HUGO_VERSION=0.147.9
HUGO_ENV=development
NODE_VERSION=18
```

#### 3. 빌드 설정 확인
- **Framework preset**: Hugo
- **Build command**: `hugo --minify --gc`
- **Build output directory**: `public`
- **Node.js version**: 18

### 빌드 문제 해결

#### 엔터테인먼트 섹션 404 오류 해결
최근 수정사항으로 엔터테인먼트 섹션이 사이트맵과 메인 페이지에 포함되었습니다:
- ✅ 사이트맵에 entertainment 섹션 추가
- ✅ 메인 페이지에 엔터테인먼트 기사 표시
- ✅ 엔터테인먼트 섹션 아이콘 및 스타일 적용

#### 일반적인 빌드 문제
1. **Hugo 버전 불일치**: 환경 변수에서 `HUGO_VERSION=0.147.9` 설정
2. **Base URL 문제**: 빌드 명령어에 `--baseURL $CF_PAGES_URL` 추가
3. **캐시 문제**: Cloudflare Pages에서 "Clear cache and deploy" 실행

### 수동 배포 (로컬에서)
```bash
# 빌드
hugo --minify --gc

# Cloudflare Pages에 배포 (wrangler 사용)
npx wrangler pages deploy public
```
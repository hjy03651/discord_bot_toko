# Toko Discord 봇

Toko는 도서 관리, 이벤트 관리, 물품 보관 등 다양한 기능을 제공하는 Discord 봇입니다.

## 목차

- [기능](#기능)
- [요구사항](#요구사항)
- [설치](#설치)
- [설정](#설정)
- [사용법](#사용법)
- [명령어](#명령어)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## 기능

### 📚 도서 관리 (BookRetrieval)
- 도서 검색 및 목록 조회
- 도서 대출/반납 시스템
- 도서 추가/수정/삭제
- 대출 현황 확인
- 페이지네이션을 통한 검색 결과 표시

### 🎉 이벤트 관리 (Event)
- 이벤트 참여자 집계
- 당첨자 추첨 기능
- 이벤트 통계 및 관리

### 📦 물품 보관 (Saving)
- 물품 보관 등록
- 보관 기한 알림 (6일 후 DM 발송)
- 물품 회수 처리

### 🎮 재미있는 기능 (ForFun)
- 끝말잇기 게임
- 이미지 처리 기능
- 다양한 엔터테인먼트 명령어

### 🔧 관리자 기능 (Sql)
- SQL 쿼리 실행 (관리자 전용)
- 데이터베이스 직접 관리

## 요구사항

- Python 3.13+
- PostgreSQL 데이터베이스
- Discord Bot 토큰
- 필요한 Python 패키지 (requirements.txt 참조)

## 설치

1. 저장소 클론
```bash
git clone https://github.com/yourusername/toko.git
cd toko
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 입력:
```env
DISCORD_TOKEN=your_discord_bot_token
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=5432
```

5. 데이터베이스 설정
PostgreSQL 데이터베이스를 생성하고 필요한 테이블을 설정합니다.

## 사용법

### 봇 실행
```bash
python InuiBot130.py
```

### Docker로 실행
```bash
docker build -t discord-bot-toko .
docker run --rm -d --name discord-bot-toko --env-file .env discord-bot-toko
```

## 명령어

자세한 명령어 목록은 [commands.md](commands.md)를 참조하세요.

### 주요 명령어 예시
- `/목록 [도서명]` - 도서 검색
- `/대출 [도서ID]` - 도서 대출
- `/반납 [도서ID]` - 도서 반납
- `/event [이벤트명] [당첨자수]` - 이벤트 추첨
- `/보관 [@사용자] [물품]` - 물품 보관 등록

## 개발

### 테스트 실행
```bash
pytest tests/
```

### 코드 품질 검사
```bash
# Flake8 실행
flake8 .

# Pylint 실행
pylint $(git ls-files '*.py')
```

## 배포

GitHub Actions를 통한 자동 배포가 설정되어 있습니다. 자세한 내용은 [DEPLOY_SETUP.md](DEPLOY_SETUP.md)를 참조하세요.

## 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이선스

[LICENSE](../../LICENSE)

# 배포 워크플로우 설정 가이드

이 가이드는 배포 워크플로우를 위한 GitHub Secrets 설정 방법을 설명합니다.

## 필수 GitHub Secrets

GitHub 저장소에 다음 시크릿을 설정해야 합니다:

1. **KEY** - AWS Lightsail 개인 키 내용
2. **SSH_USER** - SSH 사용자명
3. **SSH_HOST** - 서버 IP 주소

## GitHub Secrets 설정 방법

1. GitHub 저장소로 이동
2. **Settings** 탭 클릭
3. 왼쪽 사이드바에서 **Secrets and variables** → **Actions** 클릭
4. **New repository secret** 클릭
5. 각 시크릿 추가:

### LIGHTSAIL_SSH_KEY
- **Name**: `KEY`
- **Value**: `.pem` 파일의 전체 내용을 복사하여 붙여넣기 (다음 내용 포함):
  ```
  -----BEGIN RSA PRIVATE KEY-----
  [여기에 키 내용]
  -----END RSA PRIVATE KEY-----
  ```

### SSH_USER
- **Name**: `SSH_USER`

### SSH_HOST
- **Name**: `SSH_HOST`

## 배포 실행 방법

1. GitHub 저장소의 **Actions** 탭으로 이동
2. **Deploy to Lightsail Server** 워크플로우 선택
3. **Run workflow** 클릭
4. 브랜치 선택 (보통 `main`)
5. **Run workflow** 버튼 클릭

워크플로우는 다음 작업을 수행합니다:
- SSH를 사용하여 Lightsail 서버에 연결
- `toko` 디렉토리로 이동
- GitHub에서 최신 변경사항 가져오기
- 기존 Docker 컨테이너 중지 및 제거
- 새 Docker 이미지 빌드
- `.env` 파일의 환경 변수를 사용하여 새 컨테이너 시작

## 서버 사전 요구사항

Lightsail 서버에 다음이 설치되어 있어야 합니다:
- Docker 설치됨
- `toko` 디렉토리에 Git 저장소 클론됨
- `toko` 디렉토리에 Discord 봇 설정이 포함된 `.env` 파일
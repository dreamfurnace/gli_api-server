# GLI API GitHub Actions 워크플로우

## 필요한 AWS 인프라

배포 전에 다음 AWS 리소스가 필요합니다:

### ECR (Elastic Container Registry)
```bash
aws ecr create-repository --repository-name gli-api-staging --region ap-northeast-2
aws ecr create-repository --repository-name gli-api-production --region ap-northeast-2
```

### ECS 클러스터 및 서비스
- Staging: `staging-gli-cluster`, `staging-django-api-service`
- Production: `production-gli-cluster`, `production-django-api-service`

### ALB (Application Load Balancer)
- Staging: `stg-api.glibiz.com`
- Production: `api.glibiz.com`

### RDS
- ✅ 이미 생성됨
  - Production: `gli-db-production.cp4ems4wqez2.ap-northeast-2.rds.amazonaws.com`
  - Staging: `gli-db-staging.cp4ems4wqez2.ap-northeast-2.rds.amazonaws.com`

## 필요한 GitHub Secrets

다음 secrets를 GitHub repository에 설정해야 합니다:

### AWS 자격 증명
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Django 설정
- `SECRET_KEY_STAGING`
- `SECRET_KEY_PRODUCTION`

### 데이터베이스 (Secrets Manager에서 가져옴)
- RDS 연결은 Secrets Manager를 통해 자동 관리됨
- Secret ARN:
  - Production: `arn:aws:secretsmanager:ap-northeast-2:917891822317:secret:gli/db/production-u1ubhz`
  - Staging: `arn:aws:secretsmanager:ap-northeast-2:917891822317:secret:gli/db/staging-jnPMCP`

### CORS 및 Allowed Hosts
- `CORS_ALLOWED_ORIGINS_STAGING`=https://stg.glibiz.com,https://stg-admin.glibiz.com
- `CORS_ALLOWED_ORIGINS_PRODUCTION`=https://glibiz.com,https://admin.glibiz.com
- `FRONTEND_BASE_URL_STAGING`=https://stg.glibiz.com
- `FRONTEND_BASE_URL_PRODUCTION`=https://glibiz.com

### JWT 키
- `JWT_PRIVATE_KEY_STAGING`
- `JWT_PUBLIC_KEY_STAGING`
- `JWT_PRIVATE_KEY_PRODUCTION`
- `JWT_PUBLIC_KEY_PRODUCTION`

## 배포 흐름

### Staging 배포
```
stg 브랜치 push → GitHub Actions → ECR 이미지 빌드 → RDS 마이그레이션 → ECS 서비스 업데이트
```

### Production 배포
```
main 브랜치 push → GitHub Actions → ECR 이미지 빌드 → RDS 마이그레이션 → ECS 서비스 업데이트
```

## 워크플로우 파일

### ✅ 생성 완료
- `deploy-staging.yml` - stg 브랜치 push 시 자동 배포
- `deploy-production.yml` - main 브랜치 push 시 자동 배포

### 주요 기능
- AWS Secrets Manager에서 DB 정보 자동 가져오기
- Django 마이그레이션 자동 실행
- Docker 이미지 빌드 및 ECR 푸시
- ECS 서비스 업데이트
- Health check 검증

## 다음 단계

### 1. AWS ECR 리포지토리 생성
```bash
aws ecr create-repository --repository-name gli-api-staging --region ap-northeast-2
aws ecr create-repository --repository-name gli-api-production --region ap-northeast-2
```

### 2. AWS ECS 클러스터 생성
```bash
aws ecs create-cluster --cluster-name staging-gli-cluster --region ap-northeast-2
aws ecs create-cluster --cluster-name production-gli-cluster --region ap-northeast-2
```

### 3. Security Group 생성
```bash
# Staging
aws ec2 create-security-group \
  --group-name staging-ecs-sg \
  --description "ECS Staging Security Group" \
  --vpc-id <VPC_ID>

# Production
aws ec2 create-security-group \
  --group-name production-ecs-sg \
  --description "ECS Production Security Group" \
  --vpc-id <VPC_ID>
```

### 4. ALB 설정 및 ECS 서비스 생성
- Target Group 생성
- ALB 리스너 규칙 설정
- ECS 서비스 생성 (Auto Scaling 설정)

### 5. Route53 레코드 추가
- stg-api.glibiz.com → Staging ALB
- api.glibiz.com → Production ALB

### 6. GitHub Secrets 설정
리포지토리 Settings → Secrets and variables → Actions에서 설정

### 7. 테스트 배포 실행
```bash
# Staging 테스트
git checkout stg
git push origin stg

# Production 테스트 (신중하게!)
git checkout main
git push origin main
```

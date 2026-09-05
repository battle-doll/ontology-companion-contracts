# 버전과 호환성

현재 구현 (2026-09-05): 계약·validator·로컬 plugin의 버전은 `0.1.0-draft.1`입니다. `artifact-manifest.json`은 배포 대상 파일의 무결성을 기록하며 서명/신원 인증이 아닙니다. 현재 호환성 지원은 각 profile의 동일 초안 버전 합성 reader fixture뿐이며, 이관은 동일 profile/version 보존 계획만 제공합니다. DESIGN_VERSION은 별도로 유지합니다.

설계 문서 버전, 계약 schema/profile 버전, validator 버전, public plugin 버전, 각 소비자 제품 버전을 별도로 관리합니다. 설계 버전 0.2.0은 기존 Context schema 0.1.0-draft.1의 의미 변경을 뜻하지 않습니다.

계약 릴리스에는 schema/profile 파일, 합성 fixtures, artifact digest, producer/consumer 지원표, changes/migration 문서를 포함합니다. digest는 파일 무결성 단서이지 서명이나 작성자 신원 인증이 아닙니다.

최신 floating dependency 대신 확인한 버전을 pin합니다. Code의 최소 의존성 요구를 유지하려면 필요한 JSON 계약의 vendoring도 선택할 수 있습니다. 이 경우 출처, 원본 버전, 라이선스, 갱신/회귀 검사를 남깁니다. Context 설치 시 Contracts plugin을 자동 설치하게 만들지 않습니다.

strict reader가 extra field를 거절한다면 새 optional field도 호환되지 않을 수 있습니다. 호환성은 방향(producer→consumer), profile, 버전 쌍, 실제 fixtures로 명시합니다. unsupported 결과를 임의로 성공 처리하지 않습니다.

계약 릴리스는 public plugin 심사와 독립적으로 진행할 수 있습니다. plugin 승인은 schema의 영구 표준 인증이 아닙니다.

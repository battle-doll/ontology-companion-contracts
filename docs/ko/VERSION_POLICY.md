# Ontology Companion Contracts — 버전 정책

설계 버전은 런타임·플러그인 버전이 아닙니다. schema/profile·validator·소비자 버전을 구분하고 지원 산출물과 digest를 고정합니다. 호환성에는 명시적 producer→consumer 조합과 실행한 fixtures가 필요하며 버전 번호만으로 추론하지 않습니다. 과거 초안은 보존하고 미지원 버전은 거절합니다.

로컬 런타임은 교환 envelope 초안과 별도 Code/Context 프로필을 오프라인으로 검증합니다. 명시적으로 선택한 JSON 파일을 읽고 구조화 결과를 출력하며, 호스트에 수동 설정할 수 있는 선택적 stdio 어댑터도 구현했습니다. 로컬 합성 시험을 통과했습니다. 공개 플러그인 설치·실제 이관 실행·실제 데이터 사용·실제 호스트 연동은 미지원 또는 대기 상태입니다.

[상세 정책(영어)](../VERSION_POLICY.md) · [문서 목차](README.md)

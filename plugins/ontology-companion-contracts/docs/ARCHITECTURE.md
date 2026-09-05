# Contracts 아키텍처

현재 구현 (2026-09-05): `src/companion_contracts/`의 표준 라이브러리 validator가 번들 `_schemas/`만 읽습니다. CLI와 선택적 로컬 stdio adapter를 구현했으며, Context 소비자는 이 모듈·schema를 vendor합니다. 이는 `0.1.0-draft.1` 로컬 초안이며 Code 전체 export importer나 공통 실행 core를 출시한 상태는 아닙니다.

## 의존 방향

```text
                  versioned contract artifacts
               ontology-companion-contracts
                    /                 \
     code-ontology-companion   context-ontology-companion
```

같은 이름의 Contracts public plugin은 artifact의 검증/호환성 workflow를 제공합니다. 위 선은 artifact 의존을 뜻하며 ChatGPT plugin 설치/호출/권한 상속이 아닙니다. 자동 플랫폼 dependency 필드는 확인 없이 생성하지 않습니다.

## 공통화할 최소 의미

공유 영역은 교환 형식 식별, profile 식별/버전, producer, 출처 참조, 근거 종류와 한계, 교환물 무결성 정도입니다. 공통화 대상마다 실제 Code와 Context 예제를 비교합니다. 양쪽에서 같은 의미가 아닌 항목은 공통 필수 필드로 만들지 않습니다.

Code profile은 기존 symbol/relationship/정적 evidence/runtime-unknown 의미를 유지합니다. Context profile은 주장/결정/승인 상태/적용 시점/변경 이력을 다룹니다. Code node마다 user-approved memory record를 강요하거나, Context의 승인만으로 코드 관계를 runtime 사실로 바꾸지 않습니다.

## 기존 스키마 처리

이 번들의 Context 폴더에 보존한 draft-0.1 knowledge-envelope는 Context 전용입니다. 이는 계약 후보의 입력 자료이지 새 공통 규격의 정식 릴리스가 아닙니다. 새 profile 확정 시 source mapping과 losses를 명시하고, 지원하지 않는 값은 조용히 삭제하지 않습니다.

## 실행 구조

계약 파일과 golden fixtures → 순수 validator → CLI adapter → 필요할 때 skill/MCP adapter 순서입니다. 기본 검증에는 네트워크, DB, LLM API가 필요하지 않도록 설계합니다. 원격 MCP 도입 시 업로드되는 자료와 보존 정책을 별도로 검토합니다.

공통 실행 core 추출은 두 실제 소비자의 중복과 회귀 시험이 확인된 후 수행합니다. Contracts plugin이 다른 플러그인의 오케스트레이터나 개인 정보 저장소가 되지 않습니다.

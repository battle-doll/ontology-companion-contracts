# Contracts 출시 기준

현재 상태 (2026-09-05): 오프라인 validator, CLI, 선택적 stdio adapter, 실제 fixture 시험 이후 로컬 `.codex-plugin/plugin.json`과 설치용 skill을 작성했습니다. 로컬 실행 준비와 공개 출시를 구분합니다. 사용자 marketplace 등록, 외부 호스트 설치 시험, 공개 제출·승인은 수행하지 않았습니다. 계약과 plugin 모두 `0.1.0-draft.1` 초안입니다.

## 권장 순서

P0: 독립 사용 목적과 실제 실행 가능한 표면 확인.
P1a: 최소 envelope/profile + Context 단면 소비자 + Code legacy mapping fixture.
P1b: offline validator/호환성 fixture를 통과한 첫 계약 artifact 릴리스.
P2: 설치용 skill/script 패키지 구현; 독립 사용 흐름과 제한사항 시험.
P3: 실제 구현 기반 public listing/지원/개인정보 문서, host 시험 후 제출.

계약 artifact가 준비되면 Context 개발은 계속합니다. Contracts public plugin의 심사 대기 때문에 제품 구현을 기술적으로 차단하지 않습니다. Code plugin은 기존 제품이며 초기 단계에서 변경하지 않습니다.

## 별도 상태

계약: `draft → consumer-tested → versioned-release`.
플러그인: `design → implemented → local-tested → host-tested → submission-ready → submitted → approved → published`.

이번 폴더는 두 트랙 모두 초안입니다. `design/SKILL.draft.md`는 역사적 설계 자료로 유지하며, 실제 설치용 skill은 구현과 시험 후 별도로 작성했습니다. 구현되지 않은 tool명, 숨은 parent-plugin 의존성 또는 시험하지 않은 cross-host 지원을 공개 설명에 쓰지 않습니다.

## 독립성 시험

Code만, Context만, Contracts만 설치한 경우 각각 문서에 명시한 핵심 기능을 수행합니다. 공통 artifact는 각 소비자 릴리스에 맞게 배포됩니다. 세 plugin을 모두 설치한 경우에도 어느 도구를 호출할지 사용 목적이 명확해야 합니다. broad trigger로 모든 개발 작업을 Contracts가 가로채지 않습니다.

# 플랫폼 지원표 — 구현 시 실측 필요

공식 문서는 공통 디렉터리에서도 기능이 표면별로 다를 수 있다고 설명합니다. 같은 listing이 보인다고 executor나 hooks를 모두 지원한다고 가정하지 않습니다.

| 환경 | 첫 설계 | 확인 전 상태 |
| --- | --- | --- |
| Codex 로컬 | skill + 선택한 자료에 대한 offline validator script | not_tested |
| ChatGPT Work의 실행 가능한 환경 | 동일 workflow 재사용 후보 | not_tested |
| 실행 도구가 없는 ChatGPT 환경 | 규격 설명/검토만; 결정론적 PASS 선언 금지 | capability_limited |
| 선택적 원격 MCP | 업로드 동의/보존/인증 정책 승인 후 별도 adapter | not_implemented |

독립 공개 Contracts plugin은 사용자 지정 목표입니다. 이 표는 목표를 철회하는 것이 아니라 첫 공개 버전에서 정확히 무엇을 지원한다고 표시할지 결정하기 위한 기준입니다. ChatGPT 웹에서의 실행 지원이 필수라면 P0에서 원격 MCP 필요성을 확인하고 배포/개인정보 범위를 먼저 확정합니다.

read-only 검증 결과를 계산만 하면 비변경 동작일 수 있으나, 보고서 파일 저장/작업 enqueue/설정 변경이 포함되면 실제 effects에 맞춰 도구 hint를 설정합니다. 설계 단계에서는 정식 tool metadata를 확정하지 않습니다.

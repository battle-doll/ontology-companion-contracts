# Conformance 검증 계약

현재 상태 (2026-09-05): `0.1.0-draft.1` 오프라인 validator와 CLI, 별도 context/code profile, 합성 fixture 시험을 로컬 구현했습니다. 아래 규범의 기본 제한은 유지하며, 전체 Code 소비자 통합·외부 호스트 시험·정식 계약 출시는 완료하지 않았습니다. 현재 명령과 검증 범위는 [공개 안내](../README.md)와 `scripts/check.py`를 참고합니다.

## 검증 수준과 의미

| 수준 | 확인하는 것 | 확인하지 않는 것 |
| --- | --- | --- |
| L0 Parse | 크기 제한, 유효 JSON, 중복 키/비정상 숫자 정책 | 규격 적합성 |
| L1 Schema | 지원 schema/profile, 타입, 필수 필드, 추가 필드 정책 | 관계의 의미 |
| L2 Profile semantics | ID/참조, 시간 순서, 지원 enum, profile별 불변식 | 외부 세계의 사실 |
| L3 Compatibility | 실제 reader/producer fixtures, 지원 version pair | 미래 버전 일반 호환 |
| External verification | 별도 권한/출처/실행 증거가 필요함 | 기본 plugin은 이를 수행하지 않음 |

`PASS`는 실행한 수준에만 붙입니다. 미실행은 `not_checked`, 지원하지 않는 profile/version은 `unsupported`, 제약 위반은 `invalid`로 반환합니다. 전체 truth 인증이나 생산 환경 보안 인증을 만들지 않습니다.

## 예정 workflow

검증: 사용자가 선택한 자료를 읽고 지원되는 schema/profile로 검사합니다. 오류는 JSON Pointer, rule_id, 간단한 이유, 관련 규격 버전을 반환하며 민감 본문 전체를 로그로 남기지 않습니다.

호환성 비교: 지정된 producer/consumer 버전과 profile 쌍의 실제 지원표를 확인합니다. 모든 semantic version이 자동 호환된다고 추론하지 않습니다.

이관 계획: 입력 의미 중 유지/변환/손실/지원 불가를 정리합니다. 기본 동작은 계획만 출력하며 원본 덮어쓰기를 하지 않습니다. 실제 변환 파일 생성은 별도 명시적 작업으로 다룹니다.

위 이름은 기능 설명이지 구현된 MCP tool 이름이 아닙니다. 실제 transport를 정한 후 descriptor와 side effect를 맞춥니다.

## 자원·입력 경계

허용 schema는 배포된 고정 registry에서만 로드합니다. 미등록 `$ref`와 원격 URL은 해석하지 않습니다. symlink/zip 경로 탈출/과도한 depth·배열·문자열 크기를 제한합니다. parser 중복 key, NaN/Infinity 정책을 명시합니다. 임의 코드를 import/build/run하지 않습니다. 입력·출력의 실제 byte 한도와 제한 초과 상태를 시험합니다.

숫자로 표현한 confidence를 사실일 확률로 해석하지 않습니다. 정적 evidence의 runtime_unknown과 자연어의 model_inferred는 다른 profile 의미이며 서로 덮어쓰지 않습니다.

## 출시에 필요한 최소 시험

두 profile의 정상/금지 자료, 알려지지 않은 version, dangling reference, 중복 ID, 역전된 기간, 변환 손실, 외부 ref 차단, input 무변경, 통제된 자원 고갈, 실행기가 없는 호스트에서 PASS 금지. 전체 그래프가 의도적으로 부분 export라면 누락 참조의 상태도 profile 계약에 맞게 구분합니다.

# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

Context와 Code 교환 산출물을 오프라인으로 검증하고, 지원하는 계약 버전을 비교합니다. 선택한 Code Ontology 데이터를 `code-reference` 산출물로 변환하며 변환 과정에서 제외된 정보를 함께 보여줍니다.

macOS, Windows, Linux에서 Python 3.11 이상으로 실행합니다. Code·Context 플러그인 없이도 사용할 수 있으며 API 키나 원격 서비스는 필요하지 않습니다.

## 설치

```text
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

스킬, 서버, 스키마가 함께 제공되는 전체 플러그인을 설치하세요. 설치 후 프로젝트에서 새 Codex 작업을 열면 설치된 스킬을 사용할 수 있습니다.

## 현재 대화에 적용

```text
$apply-ontology-contracts
Contracts 여기에 적용해줘. 선택한 context-export.json을 context-decision 프로필로 검증해줘.
```

적용 스킬은 현재 노출된 MCP 도구나 확인된 번들 CLI로 실제 파일과 내용 해시에 연결된 검증을 수행하고 현재 작업을 이어갑니다. 입력이 없으면 미완료로 남깁니다. 일반 온톨로지 설정 요청은 현재 실행 가능한 제품만 선택하며, 명시한 제품명이 우선합니다. 대화 안의 공유 기록으로 중복 적용을 피하고 프로젝트·전역 설정은 바꾸지 않습니다. 직접 검증과 변환에는 계속 `$validate-ontology-contract`를 사용합니다.

## 프로젝트 연결

프로젝트의 새 Codex 작업에서 다음과 같이 요청하세요.

```text
$validate-ontology-contract
현재 프로젝트에 이 플러그인의 로컬 MCP 연결을 설정해줘.
```

설정 후 같은 프로젝트에서 새 작업을 열면 MCP 도구를 사용할 수 있습니다. 직접 실행할 명령, 설치된 플러그인 경로, 운영체제별 안내는 [로컬 MCP 설정](docs/LOCAL_MCP.md)과 [Windows 빠른 시작](docs/WINDOWS_QUICKSTART.md)을 참고하세요.

## 사용

파일명을 프로젝트에서 검증할 파일로 바꿔 요청하세요.

```text
$validate-ontology-contract
context-export.json을 검증하고 형식 오류가 있으면 설명해줘.
```

선택한 Code Ontology 스냅샷을 변환할 수도 있습니다.

```text
$validate-ontology-contract
ontology.json에서 src 경로를 선택해 code-reference 산출물로 변환해줘.
변환에서 제외되는 정보도 보여줘.
입력에 없는 저장소 식별자나 리비전이 필요하면 나에게 물어봐.
```

[로컬 사용 가이드](docs/LOCAL_USE.md)에서 검증, 변환, 버전 비교, 마이그레이션 계획과 MCP 없이 사용하는 CLI 명령을 확인할 수 있습니다. CLI 변환은 새 출력 파일을 만들 수 있으며 기존 파일을 덮어쓰지 않습니다.

지원하는 교환 형식은 `0.1.0-draft.1`이며 프로필은 `context-decision`, `code-reference`입니다. Code 변환은 Code Ontology Companion `0.6.0`에서 만든 원본 스키마 `1.0` 스냅샷과 네이티브 `code-ontology-reference` 버전 `1.0.0` 산출물을 받습니다. 필요한 심벌이나 경로를 선택하면 제외된 데이터가 함께 보고됩니다.

검증 대상은 구조와 프로필 규칙입니다. 내용의 사실 여부, 제공된 리비전과 스냅샷의 일치, 실행 중 동작을 증명하지 않습니다. 참조된 코드를 실행하거나 원격 스키마를 가져오지 않습니다. 클라우드에서만 실행되는 호스트는 로컬 런타임에 별도로 연결해야 합니다.

## 업데이트

```text
codex plugin marketplace upgrade ontology-contracts-preview
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

업데이트 후 프로젝트에서 새 Codex 작업을 열어 갱신된 스킬을 불러오세요. 그 작업에서 위의 프로젝트 연결을 다시 요청한 뒤, 새 작업을 한 번 더 열면 갱신된 MCP 연결을 사용할 수 있습니다.

## 도움말

[문서](docs/ko/README.md) · [지원](SUPPORT.md) · [개인정보](PRIVACY.md) · [보안](SECURITY.md) · [변경 이력](CHANGELOG.md)

[Apache-2.0](LICENSE) 라이선스로 배포합니다.

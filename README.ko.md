# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

**P1a 개발 프리뷰 · [현재 공개·검증 상태](release-state.json)**

온톨로지 교환 문서가 명시적으로 지원하는 계약에 맞는지 검사하고, 결정론적인 구조화 오류를 제공합니다. Ontology Companion Contracts는 버전별 계약 산출물과 독립 공개 검증 플러그인으로 개발 중입니다.

로컬 런타임은 교환 envelope 초안과 별도 Code/Context 프로필을 오프라인으로 검증합니다. 명시적으로 선택한 JSON 파일을 읽고 구조화 결과를 출력하며, 호스트에 수동 설정할 수 있는 선택적 stdio 어댑터도 구현했습니다. 로컬 합성 시험을 통과했습니다. macOS의 Codex 0.153.3에서 시험 표시가 있는 산출물로 수동 설정한 로컬 stdio 기본 동작 시험도 통과했습니다. 호스팅된 ChatGPT 연동·플러그인 마켓플레이스 설치 및 Directory 게시·실제 사람 승인은 미검증입니다. 실제 이관 실행과 운영 목적의 실제 데이터 사용은 아직 지원하지 않습니다.

## 공개 프리뷰 설치

저장소의 프리뷰가 공개되면 플러그인을 지원하는 Codex CLI에서 전체 패키지를 설치합니다.

```sh
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

새 Codex 작업에서 `$validate-ontology-contract`를 호출하고 설치된 패키지의 `examples/context-decision.json`을 검증해 달라고 요청합니다. 실행 코드와 스키마 자산이 필요하므로 `SKILL.md`만 복사하지 말고 전체 번들을 유지합니다. 이 검증에 Code나 Context 플러그인은 필요하지 않습니다.

[Windows 빠른 시작](docs/WINDOWS_QUICKSTART.md) · [현재 출시 상태](release-state.json). GitHub 마켓플레이스 설치와 universal Directory 게시는 별개입니다. 아래 시험 근거는 기록된 로컬 검증 시점의 결과이며, 이후 공개·OS 검증 상태는 출시 상태 파일에서 확인합니다.

## 로컬 프리뷰 실행

이 저장소 폴더에서 Python 3.11 이상을 사용합니다. 프리뷰 명령에는 추가 Python 패키지가 필요하지 않습니다. 가상 환경과 Windows 명령은 OS 안내를 참고하세요.

```sh
python3 --version
python3 scripts/run.py validate examples/context-decision.json
python3 scripts/check.py
```

아래 명령은 로컬 개발 코드를 실행합니다. 플러그인을 설치하거나 호스팅 서비스를 만들지 않습니다. 예제 자료는 합성 데이터입니다.

## 지원 OS와 검증 근거

지원 대상 OS는 **macOS·Windows·Linux**입니다. 소스 이식성, 실제 OS 시험, 플러그인 호스트 동작은 별도 항목입니다. 이 초안은 세 OS의 시험 통과를 주장하지 않습니다.

| OS | 실행 근거 |
| --- | --- |
| macOS | 로컬 Python 3.12.14 합성 시험 통과 |
| Windows | `not_run` — CI 구성 완료, 실행 대기 |
| Linux | `not_run` — CI 구성 완료, 실행 대기 |
| 플러그인 호스트 연동 | macOS Codex 0.153.3 수동 로컬 stdio 기본 동작 시험 통과; 호스팅 ChatGPT·마켓플레이스/Directory·실제 사람 승인 미검증 |

[macOS / Windows / Linux 안내](docs/ko/PLATFORMS.md)

## 제품 경계

Code·Context·Contracts는 독립 제품입니다. 소비자는 Contracts 플러그인을 설치하지 않고 계약 산출물을 버전 고정하거나 포함할 수 있습니다. 사용자 DB·권한의 공유, 자동 플러그인 호출, 기존 Code 제품 변경을 뜻하지 않습니다.

검증 통과는 실제 실행한 검사 범위에만 적용됩니다. 사실·작성자 신원·사용자 권한·런타임 동작을 입증하지 않습니다. 미지원 버전은 미지원으로, 미실행 검사는 `not_checked`로 남기며 외부 스키마를 자동으로 내려받지 않습니다.

## 문서

[문서 목차](docs/ko/README.md) · [구조와 로드맵](docs/ko/ARCHITECTURE_AND_ROADMAP.md) · [버전 정책](docs/ko/VERSION_POLICY.md) · [출시와 롤백](docs/ko/RELEASE_POLICY.md)

[보안](docs/ko/SECURITY.md) · [개인정보](docs/ko/PRIVACY.md) · [지원](docs/ko/SUPPORT.md) · [기여](docs/ko/CONTRIBUTING.md) · [변경 기록](CHANGELOG.md)

[Apache-2.0 라이선스](LICENSE)를 적용합니다. 현재 공개·검증 상태는 [release-state.json](release-state.json)을 확인하세요.

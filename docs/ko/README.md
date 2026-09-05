# Ontology Companion Contracts — 문서

[English](../README.md) | [한국어](README.md) | [日本語](../ja/README.md) | [简体中文](../zh-CN/README.md) | [Русский](../ru/README.md)

로컬 프리뷰와 제한사항부터 확인하세요. Context의 번호가 있는 설계 문서는 장기 로드맵이며 현재 런타임 지원 범위를 넓히지 않습니다.

- [로컬 프리뷰 실행](../../README.ko.md)
- [macOS / Windows / Linux 안내](PLATFORMS.md)
- [구조와 로드맵](ARCHITECTURE_AND_ROADMAP.md)
- [버전 정책](VERSION_POLICY.md)
- [출시와 롤백](RELEASE_POLICY.md)
- [보안](SECURITY.md)
- [개인정보](PRIVACY.md)
- [지원](SUPPORT.md)
- [기여](CONTRIBUTING.md)
- [변경 기록](../../CHANGELOG.md)
- [Apache-2.0](../../LICENSE)

로컬 런타임은 교환 envelope 초안과 별도 Code/Context 프로필을 오프라인으로 검증합니다. 명시적으로 선택한 JSON 파일을 읽고 구조화 결과를 출력하며, 호스트에 수동 설정할 수 있는 선택적 stdio 어댑터도 구현했습니다. 로컬 합성 시험을 통과했습니다. 공개 플러그인 설치·실제 이관 실행·실제 데이터 사용·실제 호스트 연동은 미지원 또는 대기 상태입니다.

Code·Context·Contracts는 독립 제품입니다. 소비자는 Contracts 플러그인을 설치하지 않고 계약 산출물을 버전 고정하거나 포함할 수 있습니다. 사용자 DB·권한의 공유, 자동 플러그인 호출, 기존 Code 제품 변경을 뜻하지 않습니다.

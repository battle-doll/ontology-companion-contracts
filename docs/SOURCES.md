# 출처와 검증 범위 — 2026-09-05

## 원본 자료

원본 파일은 Files Library에서 회수한 `context-ontology-companion-design-pack.zip`입니다. 생성일은 Library 메타데이터상 2026-08-29입니다. 57개 파일, 원본 schema 3개와 fixtures 8개를 확인했습니다.

현재 GitHub Code README blob SHA: `5e5b50d1b4798967cdc3724940b6204322dd8c90`. README는 0.5.3과 기존 읽기 전용 정적 분석 경계를 설명합니다. README blob 식별자와 저장소 commit 식별자를 혼동하지 않습니다. 두 새 저장소 조회는 404이며, 접근 불가/부재는 구분되지 않았습니다. 원격 변경은 없습니다.

## 공식 문서

- S-01: [GPT-5.6 and GPT-6 Pro in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt) — Astra/GPT-6 Pro 명칭과 제품별 제공 차이; 이 프로젝트의 성능 향상은 별도 측정해야 한다.
- S-02: [GPT-6 Astra introduction](https://openai.com/index/gpt-6-astra/) — 공식 제품 발표. 발표 벤치마크를 이 프로젝트 결과로 사용하지 않는다.
- S-03: [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins) — Skills/MCP/선택 UI를 조합할 수 있고 기능은 표면별로 다를 수 있다.
- S-04: [Package your plugin](https://developers.openai.com/plugins/build/plugins) — 패키징 지침. 임의 plugin 부모/자식 설치 및 권한 상속 기능을 추정하지 않는다.
- S-05: [Submit plugins](https://developers.openai.com/plugins/deploy/submission) — 실제 패키지/계정/검증/제출 절차는 개발 시 재확인; 소스 공개와 등록은 별개.
- S-06: [Plugin guidelines](https://developers.openai.com/plugins/app-guidelines) — 독립적인 목적, 실제 side effect와 맞는 도구, 최소 데이터 수집. 전체 채팅 자동 수집을 제품 목표로 두지 않는다.
- S-07: [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — 작업별 평가·반복 비교를 참고한다. 특정 외부 Evals 서비스에 제품 평가를 종속하지 않는다.
- S-08: [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275) — 제품별 사용량 체계와 Astra 사용량 차이를 설명한다. 구독/API 비용을 혼동하지 않는다.

공식 문서의 변경 가능성이 있으므로 실제 구현/제출 시 다시 확인합니다. 이 문서의 설계 제안은 OpenAI 보증이 아닙니다. 이 검토에서는 Sol/Astra 양 모델의 통제 실험, 실제 호스트 E2E 또는 공개 디렉터리 승인 확인을 수행하지 않았습니다.

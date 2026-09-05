# Ontology Companion Contracts — ドキュメント

[English](../README.md) | [한국어](../ko/README.md) | [日本語](README.md) | [简体中文](../zh-CN/README.md) | [Русский](../ru/README.md)

まずローカルプレビューと制限を確認してください。Context の番号付き設計文書は長期計画であり、現在のランタイム対応を拡大するものではありません。

- [ローカルプレビューを実行](../../README.ja.md)
- [macOS / Windows / Linux ガイド](PLATFORMS.md)
- [構成とロードマップ](ARCHITECTURE_AND_ROADMAP.md)
- [バージョン方針](VERSION_POLICY.md)
- [リリースとロールバック](RELEASE_POLICY.md)
- [セキュリティ](SECURITY.md)
- [プライバシー](PRIVACY.md)
- [サポート](SUPPORT.md)
- [貢献](CONTRIBUTING.md)
- [変更履歴](../../CHANGELOG.md)
- [Apache-2.0](../../LICENSE)

ローカルランタイムは、ドラフトの交換 envelope と個別の Code/Context プロファイルをオフラインで検証します。明示的に選んだ JSON を読み、構造化結果を出力します。ホストへ手動設定する任意の stdio アダプターも実装済みです。ローカル合成テストは成功しています。公開プラグインのインストール、移行実行、実データの利用、実際のホスト連携は未対応または保留です。

Code・Context・Contracts は独立した製品です。利用側は Contracts プラグインをインストールせずに契約成果物を固定または同梱できます。DB や権限の共有、自動プラグイン呼び出し、既存 Code 製品の変更は意味しません。

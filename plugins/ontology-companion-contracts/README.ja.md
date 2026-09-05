# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

Context と Code の交換用アーティファクトをオフラインで検証し、対応するコントラクトのバージョンを比較できます。選択した Code Ontology データを `code-reference` アーティファクトに変換し、変換時に省略された情報も表示します。

macOS、Windows、Linux と Python 3.11 以降に対応しています。Code や Context プラグインなしでも利用でき、API キーやリモートサービスは不要です。

## インストール

```text
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

スキル、サーバー、スキーマを含むプラグイン全体をインストールしてください。インストール後、プロジェクトで新しい Codex タスクを開くと、インストールしたスキルを利用できます。

## 現在の会話に適用

```text
$apply-ontology-contracts
Contracts をこの会話に適用し、選択した context-export.json を context-decision として検証してください。
```

適用スキルは現在呼び出せる MCP ツールまたは確認済みの同梱 CLI を使い、実際のファイルと内容のハッシュに結び付けて検証し、現在の作業を続けます。入力がなければ未完了のままです。一般的なオントロジー設定では現在実行可能な製品だけを選択し、明示された製品名を優先します。会話内の共有記録で重複適用を避け、プロジェクトやグローバル設定は変更しません。直接の検証・変換には引き続き `$validate-ontology-contract` を使います。

## プロジェクトに接続

対象プロジェクトの新しい Codex タスクで、次のように依頼します。

```text
$validate-ontology-contract
現在のプロジェクトに、このプラグインのローカル MCP 接続を設定してください。
```

設定後、同じプロジェクトで新しいタスクを開くと MCP ツールを利用できます。直接実行するコマンド、インストール先の確認方法、OS 別の手順は [ローカル MCP 設定](docs/LOCAL_MCP.md) と [Windows クイックスタート](docs/WINDOWS_QUICKSTART.md) を参照してください。

## 使い方

ファイル名をプロジェクト内の対象ファイルに置き換えて依頼します。

```text
$validate-ontology-contract
context-export.json を検証し、形式のエラーがあれば説明してください。
```

選択した Code Ontology スナップショットを変換することもできます。

```text
$validate-ontology-contract
ontology.json の src パスを選択し、code-reference アーティファクトに変換してください。
変換で省略される情報も表示してください。
入力にないリポジトリ識別子やリビジョンが必要な場合は、私に確認してください。
```

[ローカル利用ガイド](docs/LOCAL_USE.md) では、検証、変換、バージョン比較、移行計画と、MCP なしで使える CLI コマンドを説明しています。CLI 変換では新しい出力ファイルを作成でき、既存ファイルは上書きしません。

対応する交換形式は `0.1.0-draft.1`、プロファイルは `context-decision` と `code-reference` です。Code 変換は Code Ontology Companion `0.6.0` が生成した元のスキーマ `1.0` スナップショットと、ネイティブの `code-ontology-reference` バージョン `1.0.0` アーティファクトを受け付けます。必要なシンボルやパスを選択でき、省略されたデータが報告されます。

検証するのは構造とプロファイルの規則です。内容の事実性、指定したリビジョンとスナップショットの一致、実行時の動作は証明しません。参照されたコードの実行やリモートスキーマの取得は行いません。クラウド上だけで動くホストには、ローカルランタイムへの別途接続が必要です。

## アップデート

```text
codex plugin marketplace upgrade ontology-contracts-preview
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

アップデート後、プロジェクトで新しい Codex タスクを開き、更新されたスキルを読み込んでください。そのタスクで上記の接続設定を再度依頼し、さらに新しいタスクを開くと、更新された MCP 接続を利用できます。

## ヘルプ

[ドキュメント](docs/ja/README.md) · [サポート](SUPPORT.md) · [プライバシー](PRIVACY.md) · [セキュリティ](SECURITY.md) · [変更履歴](CHANGELOG.md)

[Apache-2.0](LICENSE) ライセンスで提供しています。

# Ontology Companion Contracts

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [Русский](README.ru.md)

**P1a 開発プレビュー · [現在の公開・検証状況](release-state.json)**

オントロジー交換文書を明示的に対応する契約と照合し、決定的で構造化された診断を返します。Ontology Companion Contracts は、バージョン付き契約成果物と独立した公開検証プラグインとして開発中です。

ローカルランタイムは、ドラフトの交換 envelope と個別の Code/Context プロファイルをオフラインで検証します。明示的に選んだ JSON を読み、構造化結果を出力します。ホストへ手動設定する任意の stdio アダプターも実装済みです。ローカル合成テストは成功しています。macOS の Codex 0.153.3 で、試験用と明記した成果物を用いた手動設定のローカル stdio スモークテストも成功しました。公開 GitHub マーケットプレイスからのインストールと、インストール済みランタイムのスモークテストも macOS で成功しました。ホスト型 ChatGPT 連携と実際の人による承認は未検証です。universal Directory への提出は別の手続きで、まだ行っていません。移行の実行と本番での実データ利用は未対応です。

## 公開プレビューをインストール

公開プレビューは現在インストールできます。プラグイン対応の Codex CLI で完全なパッケージをインストールします。

```sh
codex plugin marketplace add battle-doll/ontology-companion-contracts
codex plugin add ontology-companion-contracts@ontology-contracts-preview
```

新しい Codex タスクで `$validate-ontology-contract` を呼び出し、インストールしたパッケージの `examples/context-decision.json` を検証するよう依頼します。実行コードとスキーマ資産が必要なので、`SKILL.md` だけをコピーせず、バンドル全体を保持してください。この検証に Code や Context プラグインは不要です。

[Windows クイックスタート](docs/WINDOWS_QUICKSTART.md) · [現在のリリース状況](release-state.json)。GitHub マーケットプレイスからのインストールと universal Directory への公開は別の状態です。以下の CI 証拠はリンク先の完了した実行結果です。その後の公開・OS 検証状況はリリース状態ファイルを参照してください。

## ローカルプレビューを実行

このリポジトリのディレクトリで Python 3.11 以降を使用します。プレビューのコマンドに追加の Python パッケージは不要です。仮想環境と Windows コマンドは OS ガイドを参照してください。

```sh
python3 --version
python3 scripts/run.py validate examples/context-decision.json
python3 scripts/check.py
```

これらはローカル開発コードを実行するコマンドです。プラグインのインストールやホストサービスの作成は行いません。例は合成データです。

## 対応 OS と検証状況

対応対象 OS は **macOS・Windows・Linux** です。ソースの移植性、実行済み OS テスト、プラグインホストの動作は別々に確認します。リンク先の CI では 3 OS × 3 Python の全 9 組み合わせが成功しました。ホストへのインストールは別途検証します。

| OS | 実行証拠 |
| --- | --- |
| macOS | CI PASS — Python 3.11・3.12・3.13（3/3） |
| Windows | CI PASS — Python 3.11・3.12・3.13（3/3）。Windows Codex ホストへのインストールは未試験 |
| Linux | CI PASS — Python 3.11・3.12・3.13（3/3）。Linux Codex ホストへのインストールは未試験 |
| プラグインホスト連携 | macOS Codex 0.153.3 のローカル stdio と公開 GitHub マーケットプレイスからのインストールは成功。Windows/Linux ホストへのインストール・ホスト型 ChatGPT・実際の人による承認は未検証 |

[CI 証拠：全 9 ジョブ成功](https://github.com/battle-doll/ontology-companion-contracts/actions/runs/33975563666).

[macOS / Windows / Linux ガイド](docs/ja/PLATFORMS.md)

## 製品の境界

Code・Context・Contracts は独立した製品です。利用側は Contracts プラグインをインストールせずに契約成果物を固定または同梱できます。DB や権限の共有、自動プラグイン呼び出し、既存 Code 製品の変更は意味しません。

検証成功は実際に実施した検査だけを意味します。真実性・著者の身元・ユーザー権限・実行時動作を保証しません。未対応バージョンは未対応、未実施の層は `not_checked` のままとし、外部スキーマを自動取得しません。

## ドキュメント

[ドキュメント一覧](docs/ja/README.md) · [構成とロードマップ](docs/ja/ARCHITECTURE_AND_ROADMAP.md) · [バージョン方針](docs/ja/VERSION_POLICY.md) · [リリースとロールバック](docs/ja/RELEASE_POLICY.md)

[セキュリティ](docs/ja/SECURITY.md) · [プライバシー](docs/ja/PRIVACY.md) · [サポート](docs/ja/SUPPORT.md) · [貢献](docs/ja/CONTRIBUTING.md) · [変更履歴](CHANGELOG.md)

[Apache-2.0 ライセンス](LICENSE)を適用します。現在の公開・検証状況は [release-state.json](release-state.json) を参照してください。

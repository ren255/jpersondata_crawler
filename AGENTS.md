# AGENTS.md

このファイルは、このリポジトリで作業するClaude Code (claude.ai/code) への指示を記載する。

## これは何か

Wikidata(SPARQL/QLever経由)から日本人のデータセットを構築し、クリーニング・加工した上で分析・可視化するデータパイプライン。パッケージ/ビルドシステムは存在せず、Jupyter notebookと`#%%`区切りのスクリプト群で構成されており、通常のスクリプトとして最初から最後まで実行するのではなく、セル単位(VS Code / Jupyter interactive window形式)で実行することを前提としている。

## 環境

- Pythonのvenvは`.venv/`にある。依存関係は`requirements.txt`に記載(romkan2, namedivider-python, pandas, requests, ipykernel, matplotlib) — `pip install -r requirements.txt`でインストールする。
- テストスイート、リンター、ビルドステップはこのリポジトリには存在しない。

## パイプライン / データフロー

1. **`crawler.ipynb`** — メインパイプライン。notebookセルとして実行する:
   - QLeverのWikidataエンドポイント(`https://qlever.cs.uni-freiburg.de/api/wikidata`)にSPARQLクエリを送信し、職業・出身地・家族・受賞歴・軍歴など幅広いプロパティを持つ日本人全員を取得、生の結果を`data/jawikidata.json` / `data/jawikidata.csv`にキャッシュする。
   - SPARQLの生の変数名をsnake_caseのカラム名にリネーム(`rename_map`)して`wikidata_raw`に格納。
   - `wikidata_raw`から`wikidata`を導出する: QID URLから`qid`を抽出、`label`から`kanji`名を分離、`romkan2`と`namedivider-python`でローマ字化・名前の検証を行い、英字や特殊文字・非日本語表記を含むエントリを除外して`is_japanese_name`をフラグ付けする(ファイル全体で繰り返される`mask = ...; wikidata.loc[mask, ...] = ...; endL(...)`というパターンに注目 — 各ブロックが1種類の不正データをフィルタ/null化し、影響を受けた行数をログ出力している)。
   - 年齢、現在の年齢、身長/体重のメートル法換算など、派生する数値フィールドを計算。
   - 最終的な出力カラムは`main_columns` / `common_columns`に列挙されている(`docs/plan.md`にも重複して記載) — これがクリーニング済みデータセットの正規スキーマである。
   - 最後にクリーニング済みデータセットを`jpersondata.csv`へ書き出し(`wikidata.to_csv("jpersondata.csv")`)、`data/`(生データキャッシュ)を削除して終了する。
   - 複数値を持つフィールド(職業、出身校、受賞歴、家族など)はリストではなく`"|"`区切りの文字列として格納されている — カテゴリ/マルチラベルデータとして扱う前に`"|"`で分割すること。

2. **`image.py`** (`#%%`セル) — サンプル人物のWikidata Commons画像をダウンロードする:
   - `jpersondata.csv`から`wikidata`を読み込み、`image_url`がnullでない行を対象にする。
   - `ThreadPoolExecutor`(`MAX_WORKERS=3`)で並行ダウンロードし、失敗したURLに対してリトライパス(`MAX_PASSES=3`)を行い、`image/{qid}.jpg`に保存する。
   - すべてのリクエスト/失敗はロック保護された`log()`ヘルパー経由で`download.log`(タイムスタンプ付き、1イベント1行)に追記される — ダウンロードの問題を調査する際はstdoutだけでなくこのファイルを確認すること。

3. **`stat.py`** / **`tester.ipynb`** — クリーニング済み`wikidata`データフレームに対する探索的分析・プロット

## このリポジトリ固有の慣習

- `*.csv`、`*.json`、`image/`はgitignoreされている — 新規checkoutにデータファイルが存在すると仮定しないこと。`crawler.ipynb`(SPARQL取得)経由で再生成するか、ローカルに既に存在している必要がある。
- データ中の性別の値は日本語の文字列(`"男性"`, `"女性"`)

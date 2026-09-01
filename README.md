# 分散型スパイラル — 構造と事象で考える

The Decentralization Spiral — thinking in structure and events

Cardano の分散化とガバナンスを、検証済みの数字から分析する日英バイリンガルの一枚もの。

**https://hfot.github.io/cardano-spiral/**

---

## これは何か

「最も分散化されたチェーンは、同時に持続可能な状態にあるのか」を主題にした 19 章の構造分析。
設計として正しいことと、その設計が回り続けることを別の問いとして扱う。

- **立場と利害** — 誰が中心に残れるかを決める選抜圧力
- **数の単位** — 2,891 の登録プールは、母体クラスターの数ではない
- **責任の空白** — 権限は移り、責任はどこへも移らなかった
- **持続可能性** — トレジャリーの実測推移と枯渇までの距離

読み方は三つ。順に読む / 立場から読む（9 つの立場の語り口）/ 自分をシミュレートする（4 問）。

## 編集方針

意図的に辛口であり、同時に公平であろうとしている。ここでの辛口とは、

- すべての批判を、**公開された数字か、数字が公表されていないという事実**に紐づける
- 達成を失点と同じ筆致で記録する
- 最も強い反論を、告発の後ではなく**隣に**印刷する

価格を動かす目的では書かれておらず、筆者の建玉も表明していない。
訂正はいつでも歓迎する。

## 出典

主要な検証可能ソースは本文末尾に列挙。中心的なものは以下。

- CIP-1694（トレジャリー引き出しの定義）
- Cardano Constitution / interim-constitution リポジトリ（ガードレール、第4条）
- Cardano Foundation ICC 議事録（2026-03-11、300M NCL の否決）
- Intersect 各種発表（トレジャリー・スマートコントラクト、週次更新 #125）
- Koios API によるオンチェーン実測（トレジャリー残高、プール数、DRep、ステーキング比率）
- CoinDesk / The Block / CryptoSlate / DefiLlama

数値は取得時点のもの。オンチェーン値はエポックごとに動くため、日付を併記している。

## 編集と公開

正本は **`src/page.html`**。これだけを編集する。`index.html` は生成物なので直接触らない。

```bash
python build.py                       # src/page.html -> index.html
git add -A && git commit -m "..." && git push
```

push すると GitHub Pages が数十秒で再ビルドし、
https://hfot.github.io/cardano-spiral/ に反映される。

`src/page.html` は doctype も `<head>` も持たない断片で、Claude の Artifact
がそのまま受け取れる形。`build.py` が doctype・lang・charset・**viewport**・
description・OG・theme-color・favicon・最小リセットを被せて単体ページにする。
viewport を落とすとスマートフォンで崩れるので、生成を経ずに公開しないこと。

ローカル確認：

```bash
python -m http.server 8931 --bind 127.0.0.1
```

### アイコン

サイトマークは生成物。形を変えたいときは `tools/make_icons.py` の
`R0 / R1 / TURNS / STROKE / NODE_R` を触って再生成する。

```bash
python tools/make_icons.py    # favicon.svg / .png / .ico / apple-touch-icon / icon-512
```

中心から外へ開く螺旋。色は見出しと同じ シアン → アズール → インディゴ の
ランプで、外端の白い点は「止めるのに要る最小の主体」を指す。
ベクタと各ラスタは同じ幾何から生成されるので、ずれない。

## 技術

依存ゼロの単一 HTML ファイル。ビルドは上記の 1 スクリプトのみ。

- 日英切替（`data-en` 属性 + localStorage、初回はブラウザ言語で判定）
- 背景は Canvas。六方格子に 16 の波源を置き、二種類の波を伝播させてメッシュを点灯させる
- スクロール連動の全体図（7 層が順に組み上がる）
- ライト / ダーク両テーマ、`prefers-reduced-motion` 対応

## ライセンス

本文・分析は著者に帰属。引用の際は出典表示のうえ、原文の趣旨を損なわない形でお願いします。

# EXTREME SPEED

スピード × じゃんけんの2人用リアルタイム対戦ゲーム（HTML 1ファイル完結）。

- `index.html` … 公開用。画像・フォントをすべて埋め込んだ単体ファイル（Netlify にそのままアップロード可）
- `src/index.template.html` … 編集用ソース。`{{asset:パス}}` の箇所がビルド時に Base64 に置換される
- `assets/img/` … 画像（WebP）／ `assets/fonts/` … Orbitron・Rajdhani（SIL OFL）
- `tools/build.py` … ビルドスクリプト

```sh
python3 tools/build.py   # src → index.html
```

# EXTREME SPEED

スピード × じゃんけんの2人用リアルタイム対戦ゲーム（HTML 1ファイル完結）。
CPU対戦はオフラインで、オンライン対戦は Firebase Realtime Database で動作します。

| ファイル | 内容 |
| --- | --- |
| `index.html` | 公開用。画像・フォント・Firebase設定を埋め込んだ単体ファイル |
| `src/index.template.html` | 編集用ソース。`{{asset:…}}` / `{{json:…}}` がビルド時に置換される |
| `assets/img/` `assets/fonts/` | 画像（WebP）、Orbitron・Rajdhani（SIL OFL） |
| `tools/build.py` | ビルドスクリプト（`python3 tools/build.py`） |
| `firebase.config.json` | Firebase の Web 設定（各自作成。例: `firebase.config.example.json`） |
| `database.rules.json` | Realtime Database のセキュリティルール |
| `firebase.json` | Firebase CLI／エミュレータ用設定 |
| `netlify.toml` | Netlify 用設定 |

```sh
python3 tools/build.py   # src → index.html
```

## オンライン対戦の設定

### 1. Firebase プロジェクトを用意する
1. [Firebase コンソール](https://console.firebase.google.com/) でプロジェクトを作成（Google アナリティクスは不要）
2. **構築 → Realtime Database → データベースを作成**
   - ロケーション: `asia-southeast1`（シンガポール）が日本から近い
   - 「ロックモードで開始」を選ぶ
3. Realtime Database の **ルール** タブに `database.rules.json` の中身を貼り付けて **公開**
4. **構築 → Authentication → 始める → ログイン方法 → 匿名** を有効にする
5. **プロジェクトの設定 → 全般 → マイアプリ → ウェブ（`</>`）** でアプリを登録し、表示された `firebaseConfig` を
   `firebase.config.json` として保存する（`firebase.config.example.json` と同じ形。`databaseURL` を必ず含める）

### 2. ビルドして Netlify に公開する
1. `python3 tools/build.py` を実行（`firebase.config.json` の内容が `index.html` に埋め込まれる）
2. Netlify に公開
   - 手動: [Netlify Drop](https://app.netlify.com/drop) に `index.html` を入れたフォルダをドラッグ
   - GitHub 連携: このリポジトリを接続（`netlify.toml` によりビルド不要でルートを公開）
3. Firebase の **Authentication → 設定 → 承認済みドメイン** に `xxxx.netlify.app` を追加

### 遊び方
- タイトルの **オンライン対戦** → **ルームを作成** → 4文字のルームコード／招待リンクを相手に送る
- 相手は招待リンクを開く（自動で参加）か、コードを入力して **参加**
- 揃うと 3 カウント後に開始。モード・枚数・相手残数表示はルームを作った側の設定が使われる
- 終了後は双方が **再戦する** を押すと次の試合へ

### 仕組みと注意点
- 場札への出し手は Realtime Database のトランザクションで判定するため、同時に同じ場へ出しても先に届いた方だけが通る（後の方は `BLOCKED`、ペナルティなし）
- 自分の手は即座に予測表示し、勝敗はサーバで確定した状態だけで判定する
- Firebase の Web 設定（apiKey など）は公開されても問題ない値。アクセス制御はルールと匿名認証で行う
- 判定はクライアント側で行うため、改造したクライアントによる不正は防げない（試作段階の割り切り）
- 古いルームは自動で掃除される（サーバ処理なし。ロビーを開いた人のブラウザが最大25件ずつ削除）
  - 作成から24時間以上経ったルーム
  - 両者オフラインのまま10分以上経ったルーム
  - 退出時に相手もいなければ、そのルームはその場で削除
  - 削除できる条件はセキュリティルールで検証されるため、使用中のルームを他人が消すことはできない
- 相手の通信が一時的に切れた場合は 10 秒待ち（`RIVAL OFFLINE`）、戻れば試合を続行。自分の通信が戻ったときも自動で復帰する
- **`database.rules.json` を更新したら、Firebase コンソールのルールにも貼り直して公開すること**（掃除の検索用インデックスも含まれる）
- 無料の Spark プランは同時接続 100 まで

### ローカルでのテスト（任意）
Firebase CLI のエミュレータで、本番プロジェクトなしに動作確認できる。

```sh
npx firebase emulators:start --only auth,database --project demo-test
```

`firebase.config.json` に `"emulator": {"host": "127.0.0.1"}` を加えてビルドすると、エミュレータに接続する
（本番用にビルドするときは外すこと）。

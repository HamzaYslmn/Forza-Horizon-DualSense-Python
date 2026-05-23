<p align="right">
  <a href="../README.md">English</a> •
  <a href="ReadmeTR.md">Türkçe</a> •
  <strong>日本語</strong> •
  <a href="ReadmeZH.md">简体中文</a>
</p>

<div align="center">
  <h1>🏎️ Forza Horizon - DualSense Adaptive Triggers</h1>
  <p><strong>PC版 Forza Horizon 用のリアルなトリガーフィードバック。</strong></p>
  <p><em>ブレーキを感じろ。エンジンを感じろ。面倒な設定は不要。</em></p>
</div>

> Steam プロフィール: <https://steamcommunity.com/id/teccno/>
> 
> CS:GO アイテム支援用トレードリンク :D : <https://steamcommunity.com/tradeoffer/new/?partner=291638630&token=Xyg4vITU>

<div align="center">
  <a href="https://www.youtube.com/watch?v=-3Cp0PfL52Y">
    <img src="img/tuiyoutube.png" alt="Forza Horizon DualSense Adaptive Trigger Mod" style="width:100%;">
  </a>
</div>

> 💛 Forza Horizon 6 をプレゼントして本プロジェクトの継続を支援してくださった **[Jared (jmac122)](https://github.com/jmac122)** 氏に心から感謝いたします。

---

## 📜 目次
1. [機能概要](#-機能概要)
2. [インストール方法](#-インストール方法)
3. [ゲーム内設定](#-ゲーム内設定)
4. [Steam ハプティクスの有効化](#-steam-ハプティクスの有効化)
5. [実行方法](#-実行方法)
6. [Steam との連携自動起動](#-steam-との連携自動起動)
7. [フィードバックの微調整](#-フィードバックの微調整)
8. [トラブルシューティング](#-トラブルシューティング)
9. [支援者・クレジット](#-支援者クレジット)

---

## 💡 機能概要

Forza Horizon は車体のテレメトリデータを UDP 経由で送信しますが、Steam コントローラー入力（Steam Input）は DualSense の**アダプティブトリガー**をサポートしていません。この小さなアプリはその不足を補います。

- **左トリガー（ブレーキ）** - 踏み込むほどに反発（剛性）が強くなります。タイヤがスリップすると ABS のように細かく振動します。ハンドブレーキを引くとさらに反発が追加されます。
- **右トリガー（アクセル）** - 滑らかで漸進的な抵抗。シフトチェンジの瞬間にショック（衝撃）が走ります。レブリミットに達すると振動します。

### Steam と競合せずにコントローラーを操作する仕組み

```
┌──────────────────┐   UDP 5300 経由   ┌──────────────────┐   HID 直接書き込み   ┌─────────────┐
│  Forza Horizon   │ ────────────────► │  本アプリ        │ ──────────────────► │  DualSense  │
│  (Data Out)      │ テレメトリデータ  │  (トリガー用     │  (トリガーのみ操作) │ コントローラ │
└──────────────────┘    324 バイト     │  ビットのみ操作) │                     └─────────────┘
                                       └──────────────────┘                           ▲
                                                                                      │
                                       ┌──────────────────┐   HID 直接書き込み        │
                                       │  Steam Input     │ ─────────────────────────►│
                                       │ (通常の振動ビット)│ (通常の振動＋ボタン入力) │
                                       └──────────────────┘
```

本アプリと Steam は両方とも同じコントローラーに対して書き込みを行いますが、書き込む **バイト領域が異なります**。

- Steam は **通常の振動モーター** とボタン割り当てを制御します。
- 本アプリは **アダプティブトリガー** のビットのみを制御します（`valid_flag0` 内の `0x04` および `0x08` ビット）。
- HID デバイスは **非ブロッキングモード（non-blocking mode）** で開かれるため、コントローラーの応答を待たずに即座に書き込みが完了します。キューが溜まることも、Steam の動作をブロックすることもありません。

これにより、両者を干渉させることなく同時に動作させることができます。

---

## 🛠️ インストール方法

**必要な環境:** Windows 10/11 または Linux、および DualSense コントローラー（USB または Bluetooth 接続）。

1. [最新のリリースページ](https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python/releases/latest)へ行きます。
2. Windows の場合は **`win_start.bat`**、Linux の場合は **`linux_start.sh`** をダウンロードします。
3. 空のフォルダーを作成し、そこにダウンロードしたファイルを置きます。
4. **重要:** 最初にあらかじめ **`uv`** を手動でインストールしておくことを強く推奨します。PowerShell を開いて以下のコマンドを実行してください。
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   - この手順をスキップした場合、`win_start.bat` は自動で `uv` をインストールしようとしますが、Windows の PowerShell の実行ポリシー（Execution Policy）によりインストールがブロックされる場合があります。
   - **実行ポリシーエラーが発生した場合:** フォルダー内で **Shift キーを押しながら右クリック**し、**「PowerShell ウィンドウをここに開く」**をクリックして、`Set-ExecutionPolicy RemoteSigned -scope CurrentUser` と入力して Enter キーを押し、`Y` を入力してもう一度 Enter キーを押してください。
5. `win_start.bat` (または `linux_start.sh`) をダブルクリックして実行します。

起動用ランチャーがアプリのダウンロード、環境の構築、実行までをすべて自動で行います。次回以降の起動時にはアップデートの確認も行われます。

> [!NOTE]
> 各リリースには実験的な選択肢として、単体で動作する **Windows `.exe`** も添付されています。アプリを実行する**推奨**方法は引き続き **`win_start.bat`** です — 自動でアップデートされ、すべての Windows バージョンで同じように動作します。

> **Linux での補足:** `libhidapi` をインストールし（`sudo apt install libhidapi-hidraw0` / `sudo pacman -S hidapi` / `sudo dnf install hidapi`）、`app/packaging/linux/70-dualsense.rules` の udev ルールを追加してください。その後、コントローラーを一度抜いて挿し直してください。

### 🎮 SISR を使用してプレイする場合（Xbox アプリ / Windows ストア版のユーザー）

Xbox アプリや Microsoft Store を通じてプレイしている場合、ゲームにコントローラーを Xbox コントローラーとして認識させるツールが必要になります。選択肢の一つが **[SISR（Steam Input System Redirector）](https://github.com/Alia5/SISR)** です。SISR は Steam Input をシステムレベルにリダイレクトし、本物の Xbox コントローラーをエミュレートするため、Windows ストアアプリやアンチチート保護のあるゲームでも動作します。

SISR はコントローラーを **Steam Input** 経由で転送するため、Steam が物理 DualSense を排他的に掴んでしまい、本アプリが接続できなくなる場合があります。これを避けるために、**必ず以下の順序でプログラムを起動してください**。

1. **まず本アプリを起動します** (`win_start.bat`)。トリガーが短くポンと振動するまで待ちます。
2. **次に SISR（および Steam）を起動します。**
3. **最後に Forza Horizon を起動します。**

*(注意: プレイ中にコントローラーの接続が切れた場合は、SISR を一旦閉じ、本アプリを再起動してから、再度 SISR を開いてください。SISR のセットアップやエミュレーション設定については、[SISR README](https://github.com/Alia5/SISR) を参照してください。)*

<details>
<summary>手動インストール（開発者向け）</summary>

```bash
git clone https://github.com/HamzaYslmn/Forza-Horizon-DualSense-Python
cd Forza-Horizon-DualSense-Python/src
uv sync
uv run main.py
```

`uv` の導入: `pip install uv` または [astral.sh/uv](https://astral.sh/uv/)。
</details>

---

## 🎯 ゲーム内設定

Forza Horizon を起動し、**「設定」→「HUDとゲームプレイ」**を開き、一番下までスクロールします。

| 設定項目 | 設定値 |
|---------|-------|
| テレメトリの出力（Data Out） | **オン（ON）** |
| テレメトリ出力のIPアドレス | **127.0.0.1** |
| テレメトリ出力のポート | **5300** |

> [!NOTE]
> 一部の Forza バージョンでは、IPアドレスに `127.0.0.1` を設定しても通信が通らない場合があります。その場合は、IPアドレスに `::1`（IPv6 ループバックアドレス）を設定してみてください。

<p align="center">
  <img src="img/en.png" alt="英語設定画面" width="48%" style="border-radius: 8px;">
  &nbsp;
  <img src="img/tr.png" alt="トルコ語設定画面" width="48%" style="border-radius: 8px;">
</p>

---

## 🔊 Steam ハプティクスの有効化

**Steam** は、DualSense コントローラーの左右の通常振動モーターを動かすことができます。これを有効にする手順は以下の通りです。

### Steam での設定:
1. ライブラリ内の **Forza Horizon** を右クリック → **「プロパティ」**。
2. **「コントローラー」→「一般設定（追加の設定）」**を開きます。
3. **「DualSense の振動」**が**「オン」**になっていることを確認します。

### ゲーム内設定 (Forza Horizon):
1. **「設定」→「詳細コントロール」**を開きます。
2. **「振動」**の項目を見つけて「有効」にします。

### コントローラーのファームウェア確認:
最高の体験を得るために、公式の **PlayStation® Accessories** ソフトウェアを導入することをお勧めします。
- ダウンロード先: [PlayStation® Accessories](https://fwupdater.dl.playstation.net/fwupdater/PlayStationAccessoriesInstaller.exe)

これにより、Windows 上で DualSense のファームウェアが最新状態に保たれます。

> ℹ️ **アダプティブトリガーについて:** 本来、Steam はこのゲームで DualSense のアダプティブトリガーをサポートしていません。**本アプリ**の役目は、Steam が提供する振動の上に、リアルなトリガーフィードバック（ブレーキの踏み応え、エンジンの鼓動、ABS の脈動、シフトチェンジ時の衝撃、レブリミッターの振動）を重ねて再現することです。

---

## ▶️ 実行方法

**`win_start.bat`** (Windows) または **`linux_start.sh`** (Linux) をダブルクリックします。

トリガーが短く振動すれば動作確認完了です。Forza Horizon を起動してドライブを楽しんでください。

> 必ず Forza Horizon を起動する**前に**本アプリを実行してください。HidHide を使用している場合は、`python.exe` を許可リスト（Allowlist）に追加してください。

---

## 🎮 Steam との連携自動起動

ゲーム起動時に自動的にトリガー機能を有効にしたい場合、Steam でゲームを起動する前にランチャーを実行するように設定できます。
> ⚠️ **警告:** この自動起動設定を使用すると、環境によってはアプリの動作が不安定になることがあります。より安定した動作を望む場合は、ファイルをダブルクリックして手動で実行することを推奨します。

1. Steam で **Forza Horizon** を右クリック → **「プロパティ」**。
2. **「一般」**タブを開き、**「起動オプション」**の項目を見つけます。
3. プレイスタイルに合わせて、以下のコマンドのいずれかを入力してください（`win_start.bat` のパスはご自身の環境の実際のパスに書き換えてください）。

   * **パターンA: Steam オーバーレイやプレイ時間の記録を維持する（推奨）**
     コマンドを `cmd.exe /c` でラッピングすることで Steam にプロセスを正しく監視させます。これにより、**Steam オーバーレイ (Shift+Tab)** や **プレイ時間の記録** が正常に機能したまま、起動後にコンソールウィンドウが自動で閉じます。
     ```text
     "C:\Windows\System32\cmd.exe" /c ""C:\Your\Path\To\Forza-Horizon-DualSense-Python\win_start.bat" %command%"
     ```

   * **パターンB: よりシンプルな方法**
     直接起動しますが、Steam オーバーレイやプレイ時間の記録機能が正常に動かなくなる場合があります。
     ```text
     "C:\Your\Path\To\Forza-Horizon-DualSense-Python\win_start.bat" %command%
     ```

これで設定は完了です。**「プレイ」**ボタンを押すと、ランチャーが起動した後にゲームが始まります。

![Steam 起動オプション画面](img/steaming.png)

<details>
<summary>上級者向け - バッチファイルを使わず Python スクリプトを直接呼び出す場合</summary>

リポジトリをクローンして `uv` を使用している場合は、**「起動オプション」**に以下を入力してください。

```text
cmd /c "start /MIN /D C:\Your\Path\To\Forza-Horizon-DualSense-Python\src uv run main.py" && %command%
```
</details>

---

## 🎚️ フィードバックの微調整

各効果（ブレーキ強度、ABS 振動、シフトショック、レブリミッターなど）は、ファイルを直接編集することなく、**アプリ内の設定（Settings）画面**から調整・無効化が可能です。変更は次回起動時に適用されます。

> ⚠️ レブリミッターの振動は固定のエンジン回転数（RPM）ではなく、`rpm / max_rpm` の比率に基づいて作動します。車種によってレッドラインの比率が異なるため、車に合わせた微調整が必要になる場合があります。

---

## 🩺 トラブルシューティング

| 症状 | 対処法 |
|-----|--------|
| `DualSense gamepad interface not found` | コントローラーが接続されていないか、HidHide がコントローラーを隠しています。`python.exe` を許可リストに追加してください。 |
| `No UDP packets yet` | Forza の Data Out 設定がオフになっているか、IP/ポートの設定が間違っているか、Windows ファイアウォールが通信をブロックしています。または、IPアドレスを `127.0.0.1` から `::1` に変更してみてください。 |
| Windows Defender や SmartScreen が `win_start.bat` をブロックする | 1. 青い警告画面で **「詳細情報」** をクリックします。<br>2. 下部に表示される **「実行」** ボタンを押します（スクリプトは必要な依存関係をダウンロードするだけです）。 |
| トリガーの反発が弱すぎる | `brake_max_force` / `throttle_max_force` を上げるか、対応する `curve` 値を下げてください。 |
| トリガーがまるで壁のように硬すぎる | `brake_max_force` / `throttle_max_force` を下げるか、対応する `curve` 値を上げてください。 |
| トリガーを少し引いただけなのに反発が強すぎる | 基準フォース（baseline force）を下げるか、`curve` 値を上げてください。 |
| シフトチェンジ時にショック（振動）がない | 車が 3 km/h 以上で走行しており、有効なギア間で変速している必要があります。 |
| 起動時の振動パルスの後、コンソール画面が真っ白になる | テキストUI（TUI）を無効にするため、ターミナルから `cd src && uv run main.py --headless` で実行してください。 |

---

## 📁 プロジェクト構成

```
src/
├── main.py                          # エントリーポイント
└── modules/
    ├── settings.py                  # 👈 調整用設定ファイル
    ├── dualsense/
    │   ├── main.py                              # HID レイヤー
    │   └── adaptive_trigger.py                 # 汎用エフェクトプリミティブ
    └── forzahorizon/
        ├── udp_listener.py                     # UDP テレメトリ解析
        └── effects.py                          # Forza 専用 Controller + アニメーション
```

---

## 🙏 支援者・クレジット

開発者: **[HamzaYslmn](https://github.com/HamzaYslmn)**

### 💛 スポンサー・支援者の皆様

- **[Jared (jmac122)](https://github.com/jmac122)** - 本プロジェクトの継続と発展のため、Forza Horizon 6 をプレゼントしてくださいました。ありがとう、Jared!
- **[BeaudinSan](https://github.com/BeaudinSan)** - 非常に寛大なご支援に心から感謝いたします。励みになります！
- **[McLarenF1God](https://github.com/McLarenF1God)** - Forza Horizon 6 の DLC をプレゼントしていただきました！
- **[PlusMinusZer0](https://github.com/PlusMinusZer0)** - プリンの差し入れありがとうございます！
- **[dotcom](https://github.com/a0938670973-dotcom)** - ケーキの差し入れありがとうございます！
- **[wallbangz](https://github.com/wallbangz)** - ケーキの差し入れありがとうございます！
- **[BambinoPinguino](https://github.com/BambinoPinguino)** - お茶の差し入れありがとうございます！
- **[Ereldun](https://steamcommunity.com/)** - コーヒーの差し入れありがとうございます！
- **[Clevens克林](https://steamcommunity.com/)** - キャンディの差し入れありがとうございます！

---
*より没入感のあるレース体験のために開発されました*

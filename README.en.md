<div align="center">

<img src="assets/banner.svg" alt="GM/GN AI Agent for n8n" width="100%"/>

<br/>

[🇮🇩 Bahasa Indonesia](README.md) · **🇬🇧 English**

![n8n](https://img.shields.io/badge/n8n-self--hosted-ff6d5a?logo=n8n&logoColor=white)
![Railway](https://img.shields.io/badge/deploy-Railway-0b0d0e?logo=railway&logoColor=white)
![Google Sheets](https://img.shields.io/badge/data-Google%20Sheets-1d9e5a?logo=googlesheets&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-REST%20API-5865f2?logo=discord&logoColor=white)
![AI](https://img.shields.io/badge/AI-Gemini%20%7C%20Groq-3b82f6)
![License](https://img.shields.io/badge/license-MIT-green)

**Post GM &amp; GN to many Discord channels automatically, and manage everything by chatting.**
Channels, times, and messages live in Google Sheets. Delivery proof comes back to the channel where you gave the command.

[Features](#-features) · [How it works](#-how-it-works) · [Quick start](#-quick-start) · [Railway](#-install-on-railway) · [Credentials](#-credentials-setup) · [Commands](#-commands) · [Security](#-security-and-disclaimer) · [Privacy](#-privacy-and-data) · [FAQ](#-faq)

</div>

---

> [!WARNING]
> **Read first: Discord Terms of Service risk.** The original version of this project ([`gmgn-bot`](https://github.com/akndrn000/gmgn-bot)) used a *user account token* (self-bot). That violates Discord's ToS and the account can be banned. The workflow in this repo calls the Discord REST API with a **Header Auth** credential that you provide. Use `Bot <token>` for an official bot whenever the bot can be invited to the target channels (strongly recommended). Using a personal account token is entirely at your own risk.

> [!NOTE]
> The step-by-step guides in [`docs/`](docs) are written in Indonesian. The workflow, node names, and sheet schema are language-neutral, and the scripts are documented in English where needed.

## ✨ Features

- **Daily schedule.** The workflow starts every day at 07:00 (cron, follows the n8n timezone). GM goes out right then to every active channel; GN goes out at the universal `gn_time` in the `Config` sheet (default 19:00). The timezone is configurable.
- **One message for every channel.** Each day one GM message and one GN message are picked at random (weighted) from the `Messages` sheet ("gm", "gm all", "gm buddy", ...) and used **identically** for all registered channels.
- **Chat control with an AI Agent.** Type `!ai ...` in the monitor channel: add channels, disable a channel, add messages, send manually. Commands queue up during the day and are processed **once a day at 00:01**; replies appear after that.
- **Bulk channel add.** Paste several IDs, `<#ID>` mentions, or `discord.com/channels/...` links in one message.
- **Automatic delivery proof.** Every send is logged to the `Logs` sheet and posted to the monitor channel.
- **Card (embed) display.** With one webhook URL in the `Config` sheet, proof and agent replies appear as neat Discord cards: title, status color (green/yellow/red), and one field per channel with server name, clickable channel mention, ID, and time. Without a webhook they fall back to one plain-text line per entry. See [`docs/11`](docs/11-webhook-embed.md) (Indonesian).
- **Server and channel names resolved automatically.** Store only the channel ID.
- **Deterministic scheduling.** Scheduled sends run as plain code, no AI involved. The AI only interprets your commands.
- **No double sends.** One run per minute; duplicate channel rows are skipped.
- **Channel ID validation.** The agent verifies the channel with Discord before saving, so hallucinated IDs never reach the sheet.
- **Random delay between channels**, configured in `Config`.
- **Swappable AI model.** Gemini Flash-Lite by default; Groq (Llama) or any tool-calling model works.

## 📸 Preview

<div align="center">
<img src="assets/discord-preview.svg" alt="Illustration of the Discord output" width="760"/>
<br/><sub>Illustration of the embed cards with fictional server names and IDs. The real rendering may differ slightly.</sub>
</div>

## 🧠 How it works

<div align="center">
<img src="assets/architecture.svg" alt="System architecture" width="900"/>
</div>

One n8n workflow contains two independent flows:

| Flow | Trigger | AI? | Job |
|---|---|---|---|
| **1. Scheduler** | Cron `0 7 * * *` (once a day, node *Mulai 07:00*) | No | Builds today's queue from `Config`, `Channels`, `Messages`; GM immediately, GN waits for `gn_time`; logs to `Logs`; posts proof to the monitor channel |
| **2. AI Agent** | Cron `1 0 * * *` (once a day, node *Mulai 00:01*) | Yes | Reads all `!ai` messages queued since yesterday in the monitor channel, calls tools (Sheets and Discord), replies one by one |
| *Tes Manual* | Manual | No | Forces a "gm" to every active channel right now, for testing |
| *Tes Manual Perintah* | Manual | Yes | Processes existing `!ai` commands right now, without waiting for 00:01 |

The model is called only for queued `!ai` commands; reading messages uses no AI, so free-tier quotas are normally enough. Technical details: [`docs/09-arsitektur.md`](docs/09-arsitektur.md).

## 🚀 Quick start

Prerequisites: self-hosted n8n (a Railway guide is included), a Google account, a Discord account, and an AI model API key (Gemini or Groq).

1. Deploy n8n on Railway → [guide below](#-install-on-railway)
2. Collect Discord IDs → [`docs/03-id-discord.md`](docs/03-id-discord.md)
3. Prepare the Google Sheet from the template → [`docs/02-google-sheets.md`](docs/02-google-sheets.md)
4. Create credentials in n8n (Google Service Account, Discord Header Auth, Gemini/Groq) → [guide below](#-credentials-setup)
5. *(Optional, recommended)* Webhook for the monitor channel, so proof and replies appear as cards → [`docs/11-webhook-embed.md`](docs/11-webhook-embed.md)
6. Import the workflow → [`docs/05-import-workflow.md`](docs/05-import-workflow.md)
7. Test with the checklist → [`docs/07-checklist-tes.md`](docs/07-checklist-tes.md), then **Publish**.

```bash
git clone https://github.com/akndrn000/gmgn-n8n-agent.git
cd gmgn-n8n-agent

# 1) inject your spreadsheet ID into the workflow (output goes to dist/, which is git-ignored)
python scripts/set_sheet_id.py "https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit"

# 2) import dist/gmgn-ai-agent.json in n8n: Workflows > ... > Import from file
```

## 🚂 Install on Railway

Zero to a reachable n8n in the browser. About 10 minutes.

**1. Create the account and project**

1. Go to [railway.com](https://railway.com) → **Login** (GitHub login is easiest).
2. Pick a plan (trial or paid). n8n runs 24/7 and consumes credits continuously; check current pricing.
3. On the dashboard click **New Project** → **Deploy a Template**.
4. Search `n8n` and choose the **n8n** template that creates two services: **Postgres** and **n8n** (avoid worker/Redis variants unless you need them). Click **Deploy**.
5. Wait until both **Postgres** and **n8n** boxes show **Online** (the first deploy can take a few minutes).

**2. Expose a public domain**

1. Click the **n8n** box → **Settings** → **Networking**.
2. Click **Generate Domain** if none exists. You get `https://<name>.up.railway.app`. Copy it.

**3. Set variables**

1. In the **n8n** box open **Variables**. Keep the template's defaults (database, port, proxy, execution pruning).
2. Click **Raw Editor** and **append** these lines (do not delete existing ones):

   ```env
   GENERIC_TIMEZONE=Asia/Jakarta
   TZ=Asia/Jakarta
   ```

3. Check `WEBHOOK_URL`: it must be the domain from step 2 with `https://`. If empty or flagged with a yellow icon, set `https://${{RAILWAY_PUBLIC_DOMAIN}}`.
4. Check `DB_POSTGRESDB_HOST`: if flagged, it should reference the Postgres service in the same project (e.g. `${{Postgres.PGHOST}}`).
5. Click **Deploy** on the changes banner and wait for the redeploy.

**4. Make sure data persists (Volume)**

The **n8n** box must have a volume (e.g. `n8n-volume-xxxx`) mounted at `/home/node/.n8n`. If missing: right-click the canvas → **Volume** → attach to the n8n service → mount path `/home/node/.n8n`. Without it, the encryption key and settings can be lost on redeploy.

**5. Create the owner account**

Open the domain from step 2 and create the owner account. Store the password in a password manager.

**6. Back up the encryption key**

In the **n8n** box open **Console**, run `cat /home/node/.n8n/config`, and save the `encryptionKey` value in a password manager. Without it, credentials cannot be decrypted if you restore n8n elsewhere.

> Do not set `N8N_ENCRYPTION_KEY` to a new random value on an n8n that has already run. n8n refuses to start if it differs from the stored one.

**7. Final check**

**Deployments → View Logs** shows *Editor is now accessible via* and no repeating errors.

### Execution count

The workflow has only two daily schedules:

| Trigger | Time | Executions per day |
|---|---|---|
| Mulai 00:01 (AI Agent, processes queued commands) | once a day | 1 |
| Mulai 07:00 (GM and GN scheduler) | once a day | 1 |
| **Total** | | **2 per day (~60 per month)** |

- Tiny, so it fits self-hosted n8n on Railway and n8n Cloud quotas alike.
- The scheduler execution looks "running" for hours because it waits for the GN time (19:00). This is normal.
- Keep the database small with `EXECUTIONS_DATA_PRUNE=true` (template default).

More: [`docs/01-railway-n8n.md`](docs/01-railway-n8n.md) (Indonesian).

## 🔑 Credentials setup

The workflow uses four credential types:

<div align="center">
<img src="assets/credentials-map.svg" alt="Credential to node map" width="860"/>
</div>

Creating a credential in n8n (same for all): left menu **Overview** (or **Credentials**) → **Create** → **Create Credential** → search the type → fill fields → **Save**. Use the exact names below so they are easy to pick in nodes.

### 1. Google Service Account (access to Google Sheets)

**A. Create the Service Account**

1. Open [console.cloud.google.com](https://console.cloud.google.com) → select or create a **project**.
2. **APIs & Services → Library** → search **Google Sheets API** → **Enable**.
3. **APIs & Services → Credentials → Create credentials → Service account**. Name it → **Create and continue** → skip roles → **Done**.
4. Open the new service account → **Keys → Add key → Create new key → JSON → Create**. A `.json` file downloads. **Keep it out of the repo and never share it.**
5. Open the JSON in a text editor; you need `client_email` and `private_key`.

**B. Share the sheet with the Service Account**

Google Sheet → **Share** → paste `client_email` → role **Editor** → **Send**. Repeat for any new copy of the sheet.

**C. Fill the credential in n8n**

| Field | Value |
|---|---|
| Type | **Google Service Account API** |
| Name | `Google Service Account (GM/GN)` |
| Region | Global |
| Service Account Email | the `client_email` value |
| Private Key | the `private_key` value, whole block from `-----BEGIN PRIVATE KEY-----` to `-----END PRIVATE KEY-----` |
| Impersonate a User, Set up for use in HTTP Request node | leave off |

The green *Connection tested successfully* banner only proves the key is valid. Access to a given sheet is proven when a node actually reads it.

### 2. Discord (Header Auth)

| Field | Value |
|---|---|
| Type | **Header Auth** |
| Name | `Discord User Token` (or `Discord Bot Token` for an official bot) |
| Header name | `Authorization` |
| Value | see the options below |

**Option A: official bot (recommended, ToS-compliant)**

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications) → **New Application**.
2. **Bot** → **Reset Token** → copy it (shown once).
3. Still on **Bot**, enable **Message Content Intent**; otherwise `!ai` message content is empty.
4. **OAuth2 → URL Generator**: scope `bot`; permissions **View Channels**, **Send Messages**, **Read Message History**. Open the generated URL to invite the bot.
5. Set **Value** to `Bot <token>`.
6. A bot can only post where it is invited. If your target channels are in servers that do not allow bots, Option A will not work.

**Option B: user account token (violates Discord ToS, ban risk)**

Use the same token as `DISCORD_USER_TOKEN` in the old bot, **without** the `Bot` prefix. Prefer a spare account and never share the token.

### 3. AI model

**Gemini (default)**

1. [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → **Create API key**.
2. n8n: type **Google Gemini(PaLM) Api** → **API Key**, leave **Host** default → Save.
3. In **Google Gemini Chat Model** pick the credential and a model from the dropdown. The workflow uses `models/gemini-3.5-flash-lite`. On `404 ... model is no longer available`, choose the newest Flash/Flash-Lite model listed.

**Groq (alternative)**

1. [console.groq.com/keys](https://console.groq.com/keys) → **Create API Key**.
2. n8n: type **Groq** → **API Key** → Save.
3. Delete **Google Gemini Chat Model**; click **+** on the **Chat Model** port of **AI Agent GM/GN** → **Groq Chat Model** → pick a tool-calling model (Llama 70B family).

### 4. Attach credentials to nodes after import

1. After [importing the workflow](docs/05-import-workflow.md), nodes that need credentials show a warning.
2. Double-click a node → **Credential to connect with** → pick the matching one (see the map).
3. Do the same for each tool under **AI Agent GM/GN** (7 Sheets tools and 3 HTTP tools).
4. Click **Execute step** on one Google Sheets node (e.g. *Get Config*). If data appears, the credential and sheet permissions are right.

## 💬 Commands

Type these in the **monitor channel**, always prefixed with `!ai`. Only messages from `admin_user_id` are processed.

> [!NOTE]
> Commands are **not answered instantly**. Everything you type during the day is processed together at **00:01** and replies appear after that. GM (07:00) and GN (19:00) sends run separately on schedule. To test right now, run the **Tes Manual Perintah** trigger in n8n.

```text
!ai lihat daftar channel                      # list channels
!ai tambah channel 123456789012345678 gm jam 07:00 gn jam 21:30   # add a channel
!ai ubah jam gm channel 123456789012345678 jadi 06:45             # change GM time
!ai stop channel 123456789012345678           # disable (never deletes rows)
!ai tambah pesan gm "gm legends" bobot 8      # add a custom message
!ai kirim gm sekarang ke 123456789012345678   # send GM now
!ai tampilkan bukti pengiriman terakhir       # show latest proof
```

Commands are interpreted in natural Indonesian. Full list: [`docs/06-perintah.md`](docs/06-perintah.md).

## 📊 Data (Google Sheets)

| Sheet | Columns | Purpose |
|---|---|---|
| `Config` | `key`, `value`, `keterangan` | `monitor_channel_id`, `admin_user_id`, `monitor_webhook_url` (optional), `timezone`, `gn_time`, `min_delay_sec`, `max_delay_sec`, `last_message_id` |
| `Channels` | `channel_id`, `aktif`, `gm_time`, `gn_time` | Target channels. The daily scheduler uses `Config.gn_time`; the per-channel time columns are stored for reference |
| `Messages` | `tipe`, `teks`, `bobot` | `gm` / `gn` messages; higher weight = more frequent |
| `Logs` | `waktu`, `server`, `nama_channel`, `channel_id`, `tipe`, `pesan`, `message_id`, `status`, `error` | Delivery proof, filled automatically |

> [!IMPORTANT]
> ID and time columns **must be Plain Text**, or 18-19 digit Discord IDs will be rounded. After importing the template, use **File > Save as Google Sheets**; n8n cannot read files that are still in Excel format.

## 🔒 Security and disclaimer

- **Never** put tokens, API keys, or private keys in the repo, a sheet, or a chat. Secrets live only in n8n *Credentials*.
- Only messages from `admin_user_id` starting with `!ai` are processed; system replies start with 🤖 so they are never re-read as commands. The agent has no delete tool.
- Use a spare account for testing, keep random delays reasonable, and respect each server's rules.
- Not affiliated with Discord, n8n, Google, or Railway. Provided as is, without warranty.

Vulnerability reporting: [`SECURITY.md`](SECURITY.md).

## 🔐 Privacy and data

| Data | Stored in | Notes |
|---|---|---|
| Channel IDs, times, messages, send logs | Your own Google Sheet | No third-party server operated by this project |
| Discord token, model API key, Service Account key | n8n *Credentials* (encrypted by `N8N_ENCRYPTION_KEY`) | Never in sheets, chat, or the repo |
| `!ai` command text and relevant sheet data | Sent to the AI provider you choose | Review the provider's data policy; free tiers of some providers may use inputs to improve products |
| Execution history | Your n8n Postgres | Pruned automatically |

No telemetry. The workflow in this repo is sanitized: no spreadsheet ID, credential IDs, tokens, or personal Discord IDs.

## ❓ FAQ

<details>
<summary><b>"The document must not be an Office file"</b></summary>

The sheet is still in Excel format. Open it in Google Sheets, choose *File > Save as Google Sheets*, use the new file's ID, and share it with the Service Account again.
</details>

<details>
<summary><b>"Forbidden / The caller does not have permission"</b></summary>

The sheet is not shared with the Service Account email as **Editor**, or the spreadsheet ID in the workflow is not the shared file.
</details>

<details>
<summary><b>The schedule does not fire</b></summary>

Make sure the workflow is **Published/Active**, `GENERIC_TIMEZONE` and `TZ` are set, and `Config.gn_time` is plain-text `HH:mm`. The scheduler runs once a day at 07:00; if n8n is down at that moment, that day is skipped. Use the **Tes Manual** trigger to verify sending and logging.
</details>

More: [`docs/08-pemecahan-masalah.md`](docs/08-pemecahan-masalah.md).

## 🤝 Contributing

Pull requests are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and run `python scripts/validate_workflow.py` before opening a PR.

## 📄 License

[MIT](LICENSE) © 2026 akndrn000

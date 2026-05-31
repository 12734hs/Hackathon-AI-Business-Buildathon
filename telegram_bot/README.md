# 🤖 Telegram Bot — PeerMatch AI

A lightweight Telegram bot that acts as a support bridge between users and the PeerMatch AI team. Users can submit applications directly through Telegram, which are forwarded to a private team channel.

---

## 📁 Folder Structure

```
telegram_bot/
  bot.py          # Main bot file — all handlers and logic
  .env            # Environment variables (do not commit to git!)
```

---

## 📄 File Description

### `bot.py`

The single file that contains the entire bot. Built with `pyTelegramBotAPI` (telebot).

| Handler | Trigger | Description |
|---|---|---|
| `/start` | Command | Greets the user by name and starts the application flow |
| `get_subject` | Next step | Waits for the user to enter the subject of their application |
| `get_main_text` | Next step | Waits for the main text, then formats and sends it to the team channel |
| `/new` | Command | Starts a fresh application without restarting the bot |

### Application Flow

```
User sends /start
        ↓
Bot greets user by Telegram username
        ↓
Bot asks for the subject of the application
        ↓
Bot asks for the main text of the application
        ↓
Bot formats the message with user info + unique Application ID
        ↓
Message is forwarded to the private team Telegram channel
        ↓
User receives a confirmation message
        ↓
User can start a new application with /new
```

### Forwarded Message Format

Each application sent to the team channel looks like this:

```
New application

From: @username
Application ID: f47ac10b-58cc-4372-a567-0e02b2c3d479

Subject:
Bug report — profile not saving

Text:
When I click Save on the profile page, nothing happens...
```

---

## 🔑 Environment Variables

Create a `.env` file in the `telegram_bot/` folder:

```env
TELEGRAM_BOT_TOKEN=your-bot-token
CHANNEL_ID=your-channel-id
```

### How to get these values

**`TELEGRAM_BOT_TOKEN`**
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Copy the token BotFather gives you

**`CHANNEL_ID`**
1. Create a private Telegram channel
2. Add your bot as an **admin** of the channel
3. Forward any message from the channel to `@userinfobot` to get the channel ID
4. The ID usually looks like `-100xxxxxxxxxx`

> ⚠️ The bot must be an admin of the channel, otherwise it cannot send messages there.

---

## 🚀 Running the Bot

### Step 1 — Navigate to the bot folder

```bash
cd telegram_bot
```

### Step 2 — Install dependencies

```bash
pip install pyTelegramBotAPI python-dotenv
```

Or if a `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

### Step 3 — Set up environment variables

```bash
touch .env
```

Add to `.env`:

```env
TELEGRAM_BOT_TOKEN=your-bot-token
CHANNEL_ID=your-channel-id
```

### Step 4 — Run the bot

```bash
python bot.py
```

The bot will start polling and print received application subjects and texts to the console.

> ✅ Once running, open Telegram, find your bot, and send `/start` to test it.

---

## 🧪 Testing the Bot

1. Open your bot in Telegram
2. Send `/start`
3. Enter a subject (e.g. `Test application`)
4. Enter a body (e.g. `This is a test message`)
5. Check your team channel — the formatted application should appear there
6. Send `/new` to submit another application

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| pyTelegramBotAPI (telebot) | Telegram Bot API wrapper |
| python-dotenv | Load variables from `.env` |
| uuid | Generate unique application IDs |

---

## 📝 Notes

- The bot uses `register_next_step_handler` for a step-by-step conversation flow — no complex state management needed
- Each application gets a unique UUID so the support team can reference it
- If `TELEGRAM_BOT_TOKEN` or `CHANNEL_ID` are not set, the bot raises a `RuntimeError` immediately on startup
- The bot runs with `infinity_polling()` — it stays alive and reconnects automatically if the connection drops
- `.env` must never be committed to git (add it to `.gitignore`)

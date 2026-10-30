# eSIM Store (@esimtoolstorebot)

A complete educational Telegram bot with **exactly 3 main functions**:

1. **Learn eSIM Basics:** Explanation and a working knowledge quiz.
2. **Check Device Requirements:** Interactive iPhone/Android guidance and compatibility checks.
3. **Installation Guide:** Platform-specific installation steps and safety guidance.

The bot is informational only: it does not sell, provision, activate or deliver eSIM plans. Its bot name reflects the owner's selected brand, not a functioning checkout. Ads must not imply that this bot sells plans.

## Setup
1. Create or confirm the bot's BotFather username is `@esimtoolstorebot`.
2. Set the `BOT_TOKEN` environment variable to that bot's token. Never commit it.
3. Deploy as a **single** Render Background Worker using the Dockerfile (render.yaml is an optional blueprint; verify plan availability/costs).
4. Bot name, About, description and commands are automatically synchronized on startup. Add a clear eSIM-themed profile picture manually with BotFather `/setuserpic`.
5. Open https://t.me/esimtoolstorebot and test `/start`, `/help`, all three tools and their sub-buttons on mobile and desktop. Keep the worker running and check for errors before submitting ads.

## Sample Telegram ad
Text: `Learn eSIM basics, explore phone compatibility tips and read installation guides with eSIM Store on Telegram.`
Destination URL: `t.me/esimtoolstorebot`

Telegram reviews ads case by case. No implementation guarantees approval. See https://ads.telegram.org/guidelines.

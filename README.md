# ShlinkTelegramBot

ShlinkTelegramBot is a Telegram bot that provides a convenient way to shorten URLs right within your Telegram chat. Send a long URL and receive a shortened version in seconds.

## Getting Started

To use ShlinkTelegramBot, you need to run it as a service, which you can easily set up using Docker and `docker-compose`.

### Prerequisites

- Docker
- Docker Compose
- [Shlink](https://github.com/shlinkio/shlink)

### Configuration

To set up the ShlinkTelegramBot service, you need to create a `docker-compose.yml` file using the template below. Be sure to replace the placeholder values with your actual configuration details.

    version: '3.8'
    services:
      ShlinkTelegramBot:
        image: isrofilov/shlink-telegram-bot:latest
        environment:
          TELEGRAM_BOT_TOKEN: your_telegram_bot_token_here
          SHLINK_API_TOKEN: your_shlink_api_token_here
          SHLINK_SERVER_URL: your_shlink_server_url_here
          ALLOWED_TELEGRAM_IDS: "123456789,987654321"



Here's what you need to replace:

- `your_telegram_bot_token_here`: Replace this with your actual Telegram bot token.
- `your_shlink_api_token_here`: Replace this with your Shlink API token.
- `your_shlink_server_url_here`: Replace this with the full URL of your Shlink server, including `https://`. For example, `https://example.com`.
- `ALLOWED_TELEGRAM_IDS`: These are the Telegram user IDs that are allowed to interact with the bot. You can list multiple IDs separated by commas.

Make sure to use the correct URL format and include `https://` to ensure secure communication with the Shlink server.

### Running the Bot

To start the ShlinkTelegramBot, navigate to the directory containing your `docker-compose.yml` and run:

    docker-compose up -d

Your bot is now running and ready to shorten URLs!

## Usage

To shorten a URL, send it to the bot in a Telegram chat. The bot will process it and respond with a shortened link.

## Support

For support, feature requests, or bug reporting, please open an issue on the GitHub repository.
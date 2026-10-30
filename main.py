"""eSIM Store: simple, working eSIM education bot for Telegram."""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand, CallbackQuery, InlineKeyboardButton,
    InlineKeyboardMarkup, Message,
)

BOT_NAME = "eSIM Store"
BOT_USERNAME = "esimtoolstorebot"
ABOUT = "Learn about eSIM technology, phone compatibility, and safe installation."
DESCRIPTION = (
    "Welcome to eSIM Store, an educational guide to digital SIM technology. "
    "Explore three interactive tools: eSIM basics with a short quiz, "
    "device compatibility guidance, and a step-by-step installation guide. "
    "Information only: no plans are sold or activated in this bot."
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
dp = Dispatcher()


def buttons(rows):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=key) for label, key in row]
        for row in rows
    ])


def menu():
    return buttons([
        [("Learn eSIM Basics", "basics")],
        [("Check Device Requirements", "device")],
        [("Installation Guide", "install")],
    ])


def back():
    return buttons([[("Main menu", "home")]])


WELCOME = (
    "Welcome to eSIM Store!\n\n"
    "This bot teaches the basics of eSIM technology through three free tools. "
    "You can learn how an eSIM works, check common phone requirements, "
    "and read installation instructions.\n\n"
    "Education only. This bot does not sell eSIM plans, "
    "issue QR codes, or activate mobile service."
)


@dp.message(CommandStart())
@dp.message(Command("menu"))
async def start(message: Message):
    await message.answer(WELCOME, reply_markup=menu())


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Select one of three tools from /start.\n"
        "1. Learn eSIM Basics: explanation and quiz.\n"
        "2. Check Device Requirements: guided checklist.\n"
        "3. Installation Guide: step-by-step iPhone or Android tips.\n\n"
        "This educational bot does not verify your specific phone or sell plans.",
        reply_markup=menu(),
    )


@dp.callback_query(F.data == "home")
async def home(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME, reply_markup=menu())
    await callback.answer()


@dp.callback_query(F.data == "basics")
async def basics(callback: CallbackQuery):
    await callback.message.edit_text(
        "eSIM Basics\n\n"
        "An eSIM is a digital SIM built into supported devices. "
        "Instead of inserting a removable plastic SIM, you download "
        "a compatible mobile plan using instructions from a provider.\n\n"
        "An eSIM still needs a supported cellular network and an active plan. "
        "Not every phone or regional model supports eSIM.\n\n"
        "Quick question: Does an eSIM give free mobile data?",
        reply_markup=buttons([
            [("Yes", "quiz_yes"), ("No", "quiz_no")],
            [("Main menu", "home")],
        ]),
    )
    await callback.answer()


@dp.callback_query(F.data.in_({"quiz_yes", "quiz_no"}))
async def quiz(callback: CallbackQuery):
    correct = callback.data == "quiz_no"
    await callback.message.edit_text(
        ("Correct! " if correct else "Not quite. ")
        + "An eSIM is a way to store a cellular subscription digitally. "
        "Mobile data still requires an active plan and network coverage.",
        reply_markup=buttons([
            [("Repeat lesson", "basics")],
            [("Main menu", "home")],
        ]),
    )
    await callback.answer()


@dp.callback_query(F.data == "device")
async def device(callback: CallbackQuery):
    await callback.message.edit_text(
        "Device Requirements\n\n"
        "Check these before trying to install an eSIM:\n"
        "1. Your exact phone model and regional variant support eSIM.\n"
        "2. Your phone is not locked to an incompatible carrier.\n"
        "3. Your provider supports eSIM on that device.\n\n"
        "Which phone family do you use? This tool gives general guidance only.",
        reply_markup=buttons([
            [("iPhone", "device_iphone"), ("Android", "device_android")],
            [("Main menu", "home")],
        ]),
    )
    await callback.answer()


@dp.callback_query(F.data.in_({"device_iphone", "device_android"}))
async def device_result(callback: CallbackQuery):
    iphone = callback.data == "device_iphone"
    tips = (
        "On many supported iPhones, open Settings > Cellular/Mobile Data "
        "and look for Add eSIM. Some country-specific models differ."
        if iphone else
        "On many Android phones, open Settings > Network & Internet or "
        "Connections > SIM Manager and look for Add eSIM. Menus vary by brand."
    )
    await callback.message.edit_text(
        ("iPhone" if iphone else "Android") + " compatibility guidance\n\n"
        + tips + "\n\n"
        "An Add eSIM option does not guarantee support for every carrier. "
        "Confirm the exact model and carrier restrictions with the manufacturer.",
        reply_markup=buttons([
            [("Check another device", "device")],
            [("Main menu", "home")],
        ]),
    )
    await callback.answer()


@dp.callback_query(F.data == "install")
async def installation(callback: CallbackQuery):
    await callback.message.edit_text(
        "Installation Guide\n\n"
        "Before starting, obtain a legitimate eSIM plan and QR code or "
        "activation instructions from your chosen provider. "
        "Connect to reliable Wi-Fi and keep the QR code private.\n\n"
        "Choose your platform for the next steps:",
        reply_markup=buttons([
            [("iPhone steps", "install_iphone"), ("Android steps", "install_android")],
            [("Main menu", "home")],
        ]),
    )
    await callback.answer()


@dp.callback_query(F.data.in_({"install_iphone", "install_android"}))
async def install_steps(callback: CallbackQuery):
    iphone = callback.data == "install_iphone"
    first = (
        "1. Open Settings > Cellular/Mobile Data > Add eSIM."
        if iphone else
        "1. Open Settings > Connections/SIM Manager or Network & Internet > Add eSIM."
    )
    await callback.message.edit_text(
        ("iPhone" if iphone else "Android") + " installation steps\n\n"
        + first + "\n"
        "2. Follow the provider's QR code or manual setup instructions.\n"
        "3. Label your plan and choose when to use it for mobile data.\n"
        "4. Enable data roaming only if your provider requires it.\n"
        "5. Check network access and review the provider's activation terms.\n\n"
        "Menu labels vary by model. Some plans begin validity at installation; "
        "follow the provider's instructions before activating.",
        reply_markup=buttons([
            [("Choose another platform", "install")],
            [("Main menu", "home")],
        ]),
    )
    await callback.answer()


@dp.message()
async def fallback(message: Message):
    await message.answer(
        "Choose a lesson below. This bot does not accept payments or activation codes.",
        reply_markup=menu(),
    )


async def main():
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Set BOT_TOKEN in your environment before running.")
    bot = Bot(token=token)
    try:
        identity = await bot.get_me()
        if identity.username.lower() != BOT_USERNAME.lower():
            raise RuntimeError(
                f"BOT_TOKEN belongs to @{identity.username}, not @{BOT_USERNAME}. "
                "Check the token before deploying."
            )
        await bot.set_my_name(name=BOT_NAME)
        await bot.set_my_short_description(short_description=ABOUT)
        await bot.set_my_description(description=DESCRIPTION)
        await bot.set_my_commands([
            BotCommand(command="start", description="Open the three eSIM tools"),
            BotCommand(command="menu", description="Show the main menu"),
            BotCommand(command="help", description="Read bot instructions"),
        ])
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Bot profile synced. Starting polling for @%s", identity.username)
        await dp.start_polling(bot, polling_timeout=30)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

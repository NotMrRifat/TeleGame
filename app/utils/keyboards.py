"""Inline Keyboard Builder for dynamic interactive menus."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config.settings import settings
from app.i18n.engine import i18n


def get_main_menu_keyboard(lang: str = "bn") -> InlineKeyboardMarkup:
    """Constructs main menu inline keyboard with icons."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=i18n.get("btn_games", lang), callback_data="menu_games"),
                InlineKeyboardButton(
                    text=i18n.get("btn_profile", lang), callback_data="menu_profile"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=i18n.get("btn_leaderboard", lang), callback_data="menu_leaderboard"
                ),
                InlineKeyboardButton(
                    text=i18n.get("btn_rewards", lang), callback_data="menu_rewards"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=i18n.get("btn_quests", lang), callback_data="menu_quests"
                ),
                InlineKeyboardButton(text=i18n.get("btn_shop", lang), callback_data="menu_shop"),
            ],
            [
                InlineKeyboardButton(
                    text=i18n.get("btn_inventory", lang), callback_data="menu_inventory"
                ),
                InlineKeyboardButton(
                    text=i18n.get("btn_friends", lang), callback_data="menu_friends"
                ),
            ],
            [
                InlineKeyboardButton(text=i18n.get("btn_clan", lang), callback_data="menu_clan"),
                InlineKeyboardButton(
                    text=i18n.get("btn_settings", lang), callback_data="menu_settings"
                ),
            ],
            [
                InlineKeyboardButton(text=i18n.get("btn_help", lang), callback_data="menu_help"),
            ],
        ]
    )
    return keyboard


def get_back_to_menu_keyboard(lang: str = "bn") -> InlineKeyboardMarkup:
    """Simple back to main menu keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="menu_main")]
        ]
    )


def get_games_selection_keyboard() -> InlineKeyboardMarkup:
    """Constructs dynamic game selection inline keyboard."""
    games = [
        ("❌⭕ Tic-Tac-Toe", "select_game_tic_tac_toe"),
        ("✊✌✋ RPS", "select_game_rock_paper_scissors"),
        ("🔴🟡 Connect Four", "select_game_connect_four"),
        ("🔤 Hangman", "select_game_hangman"),
        ("📝 Word Chain", "select_game_word_chain"),
        ("🧠 Trivia Battle", "select_game_trivia"),
        ("🕵️ Mafia", "select_game_mafia"),
        ("🎴 UNO", "select_game_uno"),
        ("♟️ Chess", "select_game_chess"),
        ("🎲 Ludo", "select_game_ludo"),
    ]

    buttons = []
    for i in range(0, len(games), 2):
        row = [InlineKeyboardButton(text=games[i][0], callback_data=games[i][1])]
        if i + 1 < len(games):
            row.append(InlineKeyboardButton(text=games[i + 1][0], callback_data=games[i + 1][1]))
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="menu_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_game_details_keyboard(game_slug: str) -> InlineKeyboardMarkup:
    """Inline keyboard for individual game detail page."""
    bot_username = settings.BOT_USERNAME or "TeleGameMasterBot"
    start_group_url = f"https://t.me/{bot_username}?startgroup={game_slug}"

    buttons = [
        [InlineKeyboardButton(text="➕ Add to Group Chat to Play", url=start_group_url)],
        [InlineKeyboardButton(text="🔙 Back to Games", callback_data="menu_games")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_tic_tac_toe_keyboard(board: list[str]) -> InlineKeyboardMarkup:
    """Renders interactive 3x3 Tic-Tac-Toe grid keyboard."""
    buttons = []
    for r in range(3):
        row = []
        for c in range(3):
            idx = r * 3 + c
            val = board[idx] if board[idx] != " " else "⬜"
            row.append(InlineKeyboardButton(text=val, callback_data=f"ttt_move_{idx}"))
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_rps_keyboard() -> InlineKeyboardMarkup:
    """Renders interactive Rock Paper Scissors choice keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🪨 Rock", callback_data="rps_move_rock"),
                InlineKeyboardButton(text="📄 Paper", callback_data="rps_move_paper"),
                InlineKeyboardButton(text="✂️ Scissors", callback_data="rps_move_scissors"),
            ]
        ]
    )


def get_connect_four_keyboard(board: list[list[str]] | None = None) -> InlineKeyboardMarkup:
    """Renders interactive 7-column Connect Four drop keyboard."""
    buttons = []

    # Column selectors 1 to 7
    col_row = []
    for col in range(7):
        col_row.append(InlineKeyboardButton(text=f"{col + 1}️⃣", callback_data=f"c4_drop_{col}"))
    buttons.append(col_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

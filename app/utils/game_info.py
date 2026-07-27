"""Game rules, descriptions, and instructions repository."""

GAME_DETAILS = {
    "tic_tac_toe": {
        "title": "❌⭕ Tic-Tac-Toe",
        "category": "Board / Strategy",
        "min_players": 2,
        "max_players": 2,
        "description": "Classic 3x3 grid strategy game.",
        "rules": (
            "1️⃣ Players take turns placing ❌ and ⭕ on the 3x3 grid using inline buttons.\n"
            "2️⃣ Align 3 of your symbols in a row (horizontal, vertical, or diagonal) to win!\n"
            "3️⃣ If all 9 cells are filled with no 3-in-a-row, the game ends in a draw."
        ),
    },
    "rock_paper_scissors": {
        "title": "✊✌✋ Rock Paper Scissors",
        "category": "Casual / Quick",
        "min_players": 2,
        "max_players": 2,
        "description": "Simultaneous hand-gesture battle.",
        "rules": (
            "1️⃣ Both players select their choice simultaneously using the buttons: 🪨 Rock, 📄 Paper, or ✂️ Scissors.\n"
            "2️⃣ 🪨 Rock beats ✂️ Scissors.\n"
            "3️⃣ ✂️ Scissors beats 📄 Paper.\n"
            "4️⃣ 📄 Paper beats 🪨 Rock.\n"
            "5️⃣ If both pick the same choice, it's a draw!"
        ),
    },
    "connect_four": {
        "title": "🔴🟡 Connect Four",
        "category": "Strategy / Grid",
        "min_players": 2,
        "max_players": 2,
        "description": "Drop discs to connect 4 in a row.",
        "rules": (
            "1️⃣ Players take turns dropping colored discs (🔴 or 🟡) into 1 of 7 columns.\n"
            "2️⃣ Discs fall to the lowest available space in the chosen column.\n"
            "3️⃣ Connect 4 discs vertically, horizontally, or diagonally to win!"
        ),
    },
    "hangman": {
        "title": "🔤 Hangman",
        "category": "Word / Quiz",
        "min_players": 1,
        "max_players": 8,
        "description": "Guess the hidden word before running out of attempts.",
        "rules": (
            "1️⃣ A hidden word is chosen by the engine.\n"
            "2️⃣ Players guess letters by typing them in the chat.\n"
            "3️⃣ Correct guesses reveal letters; wrong guesses draw parts of the hangman!\n"
            "4️⃣ Guess the full word before 6 wrong attempts to win!"
        ),
    },
    "word_chain": {
        "title": "📝 Word Chain",
        "category": "Word / Party",
        "min_players": 2,
        "max_players": 10,
        "description": "Chain words using the last letter of the previous word.",
        "rules": (
            "1️⃣ The first player types a starting word.\n"
            "2️⃣ Next player must type a valid word starting with the LAST letter of the previous word.\n"
            "3️⃣ No repeating words! Players get eliminated if they run out of time or type invalid words."
        ),
    },
    "trivia": {
        "title": "🧠 Trivia Battle",
        "category": "Quiz / General Knowledge",
        "min_players": 1,
        "max_players": 20,
        "description": "Real-time quiz competition.",
        "rules": (
            "1️⃣ Questions are presented with multiple choice options.\n"
            "2️⃣ Tap the correct answer as fast as possible using the buttons.\n"
            "3️⃣ Player with the highest correct answers wins!"
        ),
    },
    "mafia": {
        "title": "🕵️ Mafia",
        "category": "Social Deduction / Party",
        "min_players": 4,
        "max_players": 16,
        "description": "Multi-role social deduction mystery match.",
        "rules": (
            "1️⃣ Roles are secret: Mafia, Detective, Doctor, and Villagers.\n"
            "2️⃣ Night phase: Mafia selects a target; Doctor protects; Detective investigates.\n"
            "3️⃣ Day phase: Town discusses and votes to eliminate suspect Mafia members!\n"
            "4️⃣ Villagers win by eliminating all Mafia; Mafia wins by equaling town numbers."
        ),
    },
    "uno": {
        "title": "🎴 UNO",
        "category": "Cards / Party",
        "min_players": 2,
        "max_players": 8,
        "description": "Classic color and number matching card game.",
        "rules": (
            "1️⃣ Match top card by color, number, or symbol.\n"
            "2️⃣ Play Action Cards (+2, Skip, Reverse, Wild) to throw off opponents.\n"
            "3️⃣ First player to clear all cards from hand wins!"
        ),
    },
    "chess": {
        "title": "♟️ Chess",
        "category": "Grand Strategy",
        "min_players": 2,
        "max_players": 2,
        "description": "Grand strategy board game.",
        "rules": (
            "1️⃣ Standard 8x8 chess rules.\n"
            "2️⃣ Move pieces (Pawns, Rooks, Knights, Bishops, Queen, King).\n"
            "3️⃣ Checkmate your opponent's King to claim victory!"
        ),
    },
    "ludo": {
        "title": "🎲 Ludo",
        "category": "Board / Luck & Strategy",
        "min_players": 2,
        "max_players": 4,
        "description": "Dice rolling board game.",
        "rules": (
            "1️⃣ Roll dice to unlock tokens and navigate around the track.\n"
            "2️⃣ Capture opponent tokens by landing on their square.\n"
            "3️⃣ Get all 4 tokens safely into the home triangle to win!"
        ),
    },
}

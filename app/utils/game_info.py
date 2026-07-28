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
        "how_to_play": (
            "🎮 *How to Play — Tic-Tac-Toe*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Be the first to get 3 of your symbols in a line!\n\n"
            "📋 *The Board:*\n"
            "The board has 9 squares arranged in 3 rows and 3 columns:\n"
            "```\n"
            "⬜ | ⬜ | ⬜\n"
            "⬜ | ⬜ | ⬜\n"
            "⬜ | ⬜ | ⬜\n"
            "```\n\n"
            "🕹️ *How to Move:*\n"
            "→ Tap any empty square button (⬜) to place your symbol there.\n"
            "→ Player 1 plays ❌, Player 2 plays ⭕\n"
            "→ You can only move on YOUR turn!\n\n"
            "💡 *Example Round:*\n"
            "Player ❌ taps center → board becomes:\n"
            "```\n"
            "⬜ | ⬜ | ⬜\n"
            "⬜ | ❌ | ⬜\n"
            "⬜ | ⬜ | ⬜\n"
            "```\n"
            "Player ⭕ taps top-left → board becomes:\n"
            "```\n"
            "⭕ | ⬜ | ⬜\n"
            "⬜ | ❌ | ⬜\n"
            "⬜ | ⬜ | ⬜\n"
            "```\n\n"
            "🏆 *Win Condition:* Fill a full row, column, or diagonal:\n"
            "```\n"
            "❌ | ❌ | ❌  ← ROW WIN!\n"
            "⭕ | ⭕ | ⬜\n"
            "⬜ | ⬜ | ⬜\n"
            "```"
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
        "how_to_play": (
            "🎮 *How to Play — Rock Paper Scissors*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Pick the gesture that beats your opponent!\n\n"
            "🕹️ *How to Make Your Move:*\n"
            "→ Tap one of the 3 buttons that appear:\n"
            "   🪨 Rock — crushes Scissors\n"
            "   📄 Paper — covers Rock\n"
            "   ✂️ Scissors — cuts Paper\n"
            "→ Both players choose at the same time (secretly!)\n"
            "→ Once BOTH players pick, the result is revealed!\n\n"
            "💡 *Example Round:*\n"
            "Player 1 taps 🪨 Rock\n"
            "Player 2 taps ✂️ Scissors\n"
            "→ 🏆 Player 1 WINS! (Rock crushes Scissors)\n\n"
            "💡 *Another Example:*\n"
            "Player 1 taps 📄 Paper\n"
            "Player 2 taps 📄 Paper\n"
            "→ 🤝 It's a DRAW! (Same choice)\n\n"
            "⚡ *Quick Cheat Sheet:*\n"
            "🪨 > ✂️ | ✂️ > 📄 | 📄 > 🪨"
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
        "how_to_play": (
            "🎮 *How to Play — Connect Four*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Be the first to connect 4 of your discs in a line!\n\n"
            "📋 *The Board:* 6 rows × 7 columns\n"
            "Discs fall DOWN to the lowest empty space.\n\n"
            "🕹️ *How to Move:*\n"
            "→ Tap a column number button (1️⃣ to 7️⃣) to drop your disc there.\n"
            "→ Player 1 uses 🔴, Player 2 uses 🟡\n"
            "→ The disc fills the BOTTOM-MOST empty row of that column!\n\n"
            "💡 *Example:*\n"
            "```\n"
            "⚪⚪⚪⚪⚪⚪⚪\n"
            "⚪⚪⚪⚪⚪⚪⚪\n"
            "⚪⚪⚪⚪⚪⚪⚪\n"
            "⚪⚪⚪🟡⚪⚪⚪\n"
            "⚪⚪🟡🔴⚪⚪⚪\n"
            "🔴🔴🟡🔴🟡⚪⚪\n"
            "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣\n"
            "```\n"
            "🔴 drops in Column 1 → disc lands at bottom.\n\n"
            "🏆 *Win:* Connect any 4 discs horizontally, vertically, or diagonally!\n"
            "```\n"
            "⚪⚪⚪⚪⚪⚪⚪\n"
            "⚪⚪⚪⚪⚪⚪⚪\n"
            "⚪⚪⚪🔴⚪⚪⚪\n"
            "⚪⚪⚪🔴⚪⚪⚪\n"
            "⚪⚪🟡🔴🟡⚪⚪\n"
            "⚪🟡🟡🔴🟡⚪⚪\n"
            "```\n"
            "↑ 🔴 wins with 4 in column 4!"
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
        "how_to_play": (
            "🎮 *How to Play — Hangman*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Guess the hidden word before the hangman is drawn!\n\n"
            "🕹️ *How to Play:*\n"
            "→ A secret word is shown as blanks: `_ _ _ _ _`\n"
            "→ Type a single letter in the chat to guess it.\n"
            "→ Correct letter → it appears in the word! ✅\n"
            "→ Wrong letter → part of hangman is drawn! ❌\n"
            "→ You have 6 wrong guesses before game over!\n\n"
            "💡 *Example:*\n"
            "Secret word: `T E L E G R A M`\n"
            "You type `E` → `_ E _ E _ _ _ _` ✅\n"
            "You type `Z` → Wrong! 1/6 ❌\n"
            "You type `T` → `T E _ E _ _ _ _` ✅\n\n"
            "⚠️ *Tips:*\n"
            "→ Start with common letters: E, A, R, S, T\n"
            "→ You can guess the full word by typing it!"
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
        "how_to_play": (
            "🎮 *How to Play — Word Chain*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Keep the chain going! Last player standing wins!\n\n"
            "🕹️ *How to Play:*\n"
            "→ On your turn, type a word that starts with the LAST LETTER of the previous word.\n"
            "→ Words must be valid and cannot be repeated!\n\n"
            "💡 *Example Chain:*\n"
            "Player 1: `APPLE` 🍎\n"
            "Player 2: `ELEPHANT` 🐘  (starts with E — last letter of APPLE)\n"
            "Player 3: `TIGER` 🐯  (starts with T — last letter of ELEPHANT)\n"
            "Player 4: `RABBIT` 🐰  (starts with R — last letter of TIGER)\n\n"
            "❌ *You are eliminated if:*\n"
            "→ You repeat a word already used\n"
            "→ Your word doesn't start with the right letter\n"
            "→ You run out of time on your turn\n\n"
            "⚡ *Action:* Just type your word in the chat on your turn!"
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
        "how_to_play": (
            "🎮 *How to Play — Trivia Battle*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Answer the most questions correctly!\n\n"
            "🕹️ *How to Play:*\n"
            "→ A question appears with 4 answer options (A, B, C, D).\n"
            "→ Tap the button with the CORRECT answer!\n"
            "→ Speed matters — faster answers earn bonus points! ⚡\n\n"
            "💡 *Example Question:*\n"
            "❓ What is the capital of France?\n"
            "🅰️ London  🅱️ Berlin\n"
            "🅲 Paris   🅳 Madrid\n"
            "→ Tap 🅲 Paris to win the point! ✅\n\n"
            "🏆 *Scoring:*\n"
            "→ Correct answer = +1 point\n"
            "→ Wrong answer = 0 points\n"
            "→ Most points at the end = WINNER!"
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
        "how_to_play": (
            "🎮 *How to Play — Mafia*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Villagers eliminate all Mafia; Mafia outnumber the town!\n\n"
            "🎭 *Your Secret Role (sent privately):*\n"
            "🔫 Mafia — eliminate a villager each night\n"
            "🕵️ Detective — investigate one player per night\n"
            "💊 Doctor — protect one player per night\n"
            "👨‍🌾 Villager — vote to eliminate suspects each day\n\n"
            "🌙 *Night Phase:*\n"
            "→ Mafia: Send /kill @username (secretly)\n"
            "→ Doctor: Send /save @username\n"
            "→ Detective: Send /investigate @username\n\n"
            "☀️ *Day Phase:*\n"
            "→ Discussion: Debate who the Mafia might be!\n"
            "→ Vote: Send /vote @username to eliminate a suspect\n"
            "→ Most votes = player is eliminated!\n\n"
            "💡 *Example:*\n"
            "Night 1: Mafia eliminates Player A\n"
            "Day 1: Town votes and eliminates Player B (suspected Mafia)\n"
            "Continue until one team wins!"
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
        "how_to_play": (
            "🎮 *How to Play — UNO*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Be the first to play ALL your cards!\n\n"
            "🕹️ *How to Play:*\n"
            "→ On your turn, tap a card from your hand to play it.\n"
            "→ The card must MATCH the top card by color OR number!\n\n"
            "💡 *Example:*\n"
            "Top card: 🔴 7\n"
            "You can play: Any 🔴 card OR any 7 card OR a Wild card!\n\n"
            "🃏 *Special Cards:*\n"
            "⬛ Wild — choose any color\n"
            "+4 Wild — next player draws 4 cards & loses turn\n"
            "+2 — next player draws 2 cards\n"
            "⛔ Skip — next player loses their turn\n"
            "🔄 Reverse — reverses the play order\n\n"
            "📢 *Important:* When you have 1 card left, tap UNO! button or you draw 2 penalty cards!\n\n"
            "🏆 Play all your cards first to WIN!"
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
        "how_to_play": (
            "🎮 *How to Play — Chess*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Checkmate your opponent's King!\n\n"
            "🕹️ *How to Move:*\n"
            "→ Type your move in standard chess notation.\n"
            "→ Format: `[piece][from][to]` or just `[from][to]`\n\n"
            "💡 *Example Moves:*\n"
            "`e2e4` — Move pawn from e2 to e4\n"
            "`d1h5` — Move Queen from d1 to h5\n"
            "`g1f3` — Move Knight from g1 to f3\n\n"
            "♟️ *Piece Movement:*\n"
            "♟ Pawn — moves forward 1 (or 2 on first move)\n"
            "♜ Rook — moves any number of squares straight\n"
            "♞ Knight — moves in L-shape (2+1 squares)\n"
            "♝ Bishop — moves diagonally any distance\n"
            "♛ Queen — moves any direction, any distance\n"
            "♚ King — moves 1 square in any direction\n\n"
            "⚠️ *Check:* Your King is under attack — you MUST escape it!\n"
            "🏆 *Checkmate:* King cannot escape → you WIN!"
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
        "how_to_play": (
            "🎮 *How to Play — Ludo*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🎯 *Goal:* Move all 4 of your tokens to the HOME zone!\n\n"
            "🕹️ *How to Play:*\n"
            "→ On your turn, tap the 🎲 Roll Dice button!\n"
            "→ Your dice number appears (1-6)\n"
            "→ Then tap which token you want to move\n\n"
            "💡 *Example Turn:*\n"
            "Your turn → Tap 🎲 Roll → You roll 🎲 4\n"
            "→ Tap Token 1 → it moves 4 spaces forward!\n\n"
            "📋 *Rules:*\n"
            "→ Roll a 6️⃣ to unlock a token from home base\n"
            "→ Land on an opponent's token → send them back home! 😈\n"
            "→ Safe squares (marked ⭐) cannot be captured\n"
            "→ Roll 6️⃣ = bonus roll! 🎉\n\n"
            "🏆 Get ALL 4 tokens to your home triangle first to WIN!"
        ),
    },
}

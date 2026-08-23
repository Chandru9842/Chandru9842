#!/usr/bin/env python3
"""
GitHub Profile Community Interactive Chess Engine & SVG Renderer for @Chandru9842.
- Handles game state persistence (FEN, PGN, turns, move history).
- Renders high-definition SVG chessboard with piece vectors and move highlights.
- Generates interactive GitHub Issue links for community turns.
- Auto-updates README.md with live board and legal move options.
"""

import os
import sys
import json
import urllib.parse
import chess
import chess.svg

DATA_FILE = "data/chess_game.json"
README_FILE = "README.md"
CHESS_SVG_DARK = "assets/chess-board-dark.svg"
CHESS_SVG_LIGHT = "assets/chess-board-light.svg"
CHESS_SVG_MAIN = "assets/chess-board.svg"
REPO_OWNER = "Chandru9842"
REPO_NAME = "Chandru9842"

DEFAULT_GAME_STATE = {
    "fen": chess.STARTING_FEN,
    "turn": "white",
    "move_count": 0,
    "last_move": "Game Start",
    "last_player": f"@{REPO_OWNER}",
    "status": "In Progress",
    "history": [],
}

def load_game_state():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return dict(DEFAULT_GAME_STATE)

def save_game_state(state):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def generate_board_svg(board, last_move_uci=None, theme="dark"):
    """
    Renders a custom SVG chessboard.
    """
    is_dark = (theme == "dark")
    light_square = "#EBECD0" if not is_dark else "#334155"
    dark_square = "#779952" if not is_dark else "#1E293B"
    bg_color = "#FFFFFF" if not is_dark else "#0B1120"
    border_color = "rgba(0,0,0,0.1)" if not is_dark else "rgba(255,255,255,0.1)"
    text_color = "#0F172A" if not is_dark else "#F8FAFC"
    highlight_color = "#FCD34D" if not is_dark else "#38BDF8"

    last_move = None
    if last_move_uci:
        try:
            last_move = chess.Move.from_uci(last_move_uci)
        except Exception:
            pass

    svg = chess.svg.board(
        board,
        lastmove=last_move,
        colors={
            "square light": light_square,
            "square dark": dark_square,
            "margin": bg_color,
            "coord": text_color,
            "square light lastmove": highlight_color,
            "square dark lastmove": highlight_color,
        },
        size=440,
    )
    return svg

def render_all_svgs(board, last_move_uci=None):
    os.makedirs("assets", exist_ok=True)
    dark_svg = generate_board_svg(board, last_move_uci, theme="dark")
    light_svg = generate_board_svg(board, last_move_uci, theme="light")

    with open(CHESS_SVG_DARK, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(CHESS_SVG_LIGHT, "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open(CHESS_SVG_MAIN, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print("Generated chessboard SVGs successfully!")

def build_issue_link(move_san):
    title = f"Chess: Move {move_san}"
    body = f"Click 'Submit new issue' to play the move **{move_san}** against the community! ♟️"
    params = urllib.parse.urlencode({"title": title, "body": body})
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new?{params}"

def build_new_game_link():
    title = "Chess: New Game"
    body = "Click 'Submit new issue' to reset the board and start a new game of Chess! ♟️"
    params = urllib.parse.urlencode({"title": title, "body": body})
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/new?{params}"

def generate_markdown_content(state, board):
    turn_str = "⚪ **White to move**" if board.turn == chess.WHITE else "⚫ **Black to move**"
    last_move_str = state.get("last_move", "Game Start")
    last_player_str = state.get("last_player", f"@{REPO_OWNER}")
    move_count = state.get("move_count", 0)
    
    # Check status
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        status_banner = f"🏆 **Checkmate! {winner} wins!**"
    elif board.is_stalemate():
        status_banner = "🤝 **Stalemate! The game is a draw!**"
    elif board.is_check():
        status_banner = f"⚠️ **Check!** {turn_str}"
    else:
        status_banner = f"⚔️ {turn_str}"

    # Group legal moves into neat clickable pills/table
    legal_moves = list(board.legal_moves)
    legal_sans = [board.san(m) for m in legal_moves]
    legal_sans.sort()

    moves_table_rows = []
    chunk_size = 6
    for i in range(0, len(legal_sans), chunk_size):
        chunk = legal_sans[i:i+chunk_size]
        row_cells = [f"[`{san}`]({build_issue_link(san)})" for san in chunk]
        moves_table_rows.append(" | ".join(row_cells))

    moves_table = ""
    if moves_table_rows:
        header = " | ".join(["Move"] * min(chunk_size, len(legal_sans)))
        sep = " | ".join([":---:"] * min(chunk_size, len(legal_sans)))
        moves_table = f"| {header} |\n| {sep} |\n"
        for r in moves_table_rows:
            moves_table += f"| {r} |\n"
    else:
        moves_table = f"No legal moves available. [**Click here to start a New Game**]({build_new_game_link()})\n"

    new_game_btn = f"[🔄 **Start New Game**]({build_new_game_link()})"

    md = f"""<!-- CHESS:START -->
<div align="center">

### {status_banner}

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/assets/chess-board-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/assets/chess-board-light.svg" />
    <img src="https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/assets/chess-board.svg" alt="Community Interactive Chessboard" width="440px" />
  </picture>
</p>

**Move #{move_count}** • Last move: **`{last_move_str}`** by {last_player_str} • {new_game_btn}

<br/>

<details>
<summary><b>🎯 Click here to choose your move ({len(legal_sans)} legal moves available)</b></summary>

<br/>

{moves_table}

> **How to Play**: Click any move above to open a pre-filled GitHub Issue and click **Submit new issue**. GitHub Actions will validate your move, update the board live, and close the issue automatically!

</details>

</div>
<!-- CHESS:END -->"""
    return md

def update_readme(state, board):
    if not os.path.exists(README_FILE):
        return
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    chess_md = generate_markdown_content(state, board)

    start_tag = "<!-- CHESS:START -->"
    end_tag = "<!-- CHESS:END -->"

    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = before + chess_md + after
    else:
        # If not present yet, replace Conway's Game of Life or append
        if "## 🧬 &nbsp;Conway's Game of Life Heatmap" in content:
            # Replace game of life section
            p1 = content.split("## 🧬 &nbsp;Conway's Game of Life Heatmap")[0]
            # Find next header
            after_section = content.split("## 🧬 &nbsp;Conway's Game of Life Heatmap")[1]
            if "## 🏆" in after_section:
                p2 = "## 🏆" + after_section.split("## 🏆")[1]
            else:
                p2 = after_section
            new_content = p1 + "## ♟️ &nbsp;Community Interactive Chess Game\n\n" + chess_md + "\n\n<br/>\n\n" + p2
        else:
            new_content = content + "\n\n## ♟️ &nbsp;Community Interactive Chess Game\n\n" + chess_md

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated README.md with live chess board!")

def make_move(move_str, player_handle=f"@{REPO_OWNER}"):
    state = load_game_state()
    board = chess.Board(state["fen"])

    # Clean input
    clean_move = move_str.strip()
    
    # Try SAN first (e.g. e4, Nf3, O-O)
    move = None
    try:
        move = board.parse_san(clean_move)
    except Exception:
        try:
            move = board.parse_uci(clean_move)
        except Exception:
            pass

    if not move or move not in board.legal_moves:
        return False, f"Invalid or illegal move: `{clean_move}`"

    san = board.san(move)
    uci = move.uci()
    board.push(move)

    state["fen"] = board.fen()
    state["turn"] = "black" if board.turn == chess.BLACK else "white"
    state["move_count"] += 1
    state["last_move"] = san
    state["last_player"] = player_handle
    state["history"].append({
        "move": san,
        "uci": uci,
        "player": player_handle,
        "fen": board.fen()
    })

    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        state["status"] = f"Checkmate ({winner} wins)"
    elif board.is_stalemate():
        state["status"] = "Stalemate (Draw)"
    else:
        state["status"] = "In Progress"

    save_game_state(state)
    render_all_svgs(board, last_move_uci=uci)
    update_readme(state, board)

    return True, f"Move `{san}` played successfully by {player_handle}!"

def reset_game():
    state = dict(DEFAULT_GAME_STATE)
    board = chess.Board()
    save_game_state(state)
    render_all_svgs(board)
    update_readme(state, board)
    return True, "Chess game reset to starting position!"

def main():
    if len(sys.argv) < 2:
        # Default initialization / re-render
        state = load_game_state()
        board = chess.Board(state["fen"])
        last_uci = state["history"][-1]["uci"] if state["history"] else None
        render_all_svgs(board, last_move_uci=last_uci)
        update_readme(state, board)
        return

    cmd = sys.argv[1].lower()
    if cmd == "new_game" or cmd == "reset":
        success, msg = reset_game()
        print(msg)
    elif cmd == "move" and len(sys.argv) >= 3:
        move_str = sys.argv[2]
        player = sys.argv[3] if len(sys.argv) >= 4 else f"@{REPO_OWNER}"
        success, msg = make_move(move_str, player)
        print(msg)
        if not success:
            sys.exit(1)
    elif cmd == "render":
        state = load_game_state()
        board = chess.Board(state["fen"])
        last_uci = state["history"][-1]["uci"] if state["history"] else None
        render_all_svgs(board, last_move_uci=last_uci)
        update_readme(state, board)

if __name__ == "__main__":
    main()

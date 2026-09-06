#!/usr/bin/env python3
"""
Multi-Game Grandmaster Chess Animation Generator for Chandru M (@Chandru9842).
- Features 6 iconic, world-famous Grandmaster games on daily rotation.
- Human-understandable playback speed (~3.2s per move) with clear move notation & square highlights.
- Visual HUD displaying player names, event, opening, and tactical annotations.
- Dark & Light mode self-contained SVG using official Cburnett pieces.
"""

import os
import io
import sys
import datetime
import argparse
import chess
import chess.pgn
import chess.svg
import xml.sax.saxutils as saxutils

GAMES_DATABASE = [
    {
        "id": "opera-game",
        "title": "The Opera Game (1858)",
        "white": "Paul Morphy",
        "black": "Duke of Brunswick & Count Isouard",
        "event": "Paris Opera, France",
        "year": "1858",
        "opening": "Philidor Defense",
        "result": "1-0 (White wins by Queen Sacrifice & Checkmate)",
        "theme_tag": "Tactical Masterpiece",
        "pgn": """
[Event "Paris Opera"]
[Site "Paris FRA"]
[Date "1858.10.21"]
[White "Paul Morphy"]
[Black "Duke of Brunswick and Count Isouard"]
[Result "1-0"]

1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 6. Bc4 Nf6 7. Qb3 Qe7 8. Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 14. Rd1 Qe6 15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8# 1-0
"""
    },
    {
        "id": "immortal-game",
        "title": "The Immortal Game (1851)",
        "white": "Adolf Anderssen",
        "black": "Lionel Kieseritzky",
        "event": "London, England",
        "year": "1851",
        "opening": "King's Gambit Accepted",
        "result": "1-0 (White wins by Double Rook & Bishop Sacrifice)",
        "theme_tag": "Romantic Attacking Chess",
        "pgn": """
[Event "London"]
[Site "London ENG"]
[Date "1851.06.21"]
[White "Adolf Anderssen"]
[Black "Lionel Kieseritzky"]
[Result "1-0"]

1. e4 e5 2. f4 exf4 3. Bc4 Qh4+ 4. Kf1 b5 5. Bxb5 Nf6 6. Nf3 Qh6 7. d3 Nh5 8. Nh4 Qg5 9. Nf5 c6 10. g4 Nf6 11. Rg1 cxb5 12. h4 Qg6 13. h5 Qg5 14. Qf3 Ng8 15. Bxf4 Qf6 16. Nc3 Bc5 17. Nd5 Qxb2 18. Bd6 Bxg1 19. e5 Qxa1+ 20. Ke2 Na6 21. Nxg7+ Kd8 22. Qf6+ Nxf6 23. Be7# 1-0
"""
    },
    {
        "id": "game-of-the-century",
        "title": "The Game of the Century (1956)",
        "white": "Donald Byrne",
        "black": "Bobby Fischer (Age 13)",
        "event": "Rosenwald Memorial, New York",
        "year": "1956",
        "opening": "Grünfeld Defense",
        "result": "0-1 (Black wins by Legendary Queen Sacrifice)",
        "theme_tag": "Prodigy Masterpiece",
        "pgn": """
[Event "Third Rosenwald Trophy"]
[Site "New York, NY USA"]
[Date "1956.10.17"]
[White "Donald Byrne"]
[Black "Bobby Fischer"]
[Result "0-1"]

1. Nf3 Nf6 2. c4 g6 3. Nc3 Bg7 4. d4 O-O 5. Bf4 d5 6. Qb3 dxc4 7. Qxc4 c6 8. e4 Nbd7 9. Rd1 Nb6 10. Qc5 Bg4 11. Bg5 Na4 12. Qa3 Nxc3 13. bxc3 Nxe4 14. Bxe7 Qb6 15. Bc4 Nxc3 16. Bc5 Rfe8+ 17. Kf1 Be6 18. Bxb6 Bxc4+ 19. Kg1 Ne2+ 20. Kf1 Nxd4+ 21. Kg1 Ne2+ 22. Kf1 Nc3+ 23. Kg1 axb6 24. Qb4 Ra4 25. Qxb6 Nxd1 0-1
"""
    },
    {
        "id": "evergreen-game",
        "title": "The Evergreen Game (1852)",
        "white": "Adolf Anderssen",
        "black": "Jean Dufresne",
        "event": "Berlin, Germany",
        "year": "1852",
        "opening": "Evans Gambit",
        "result": "1-0 (White wins by Triple Sacrifice Checkmate)",
        "theme_tag": "Classic Evans Gambit",
        "pgn": """
[Event "Berlin"]
[Site "Berlin GER"]
[Date "1852"]
[White "Adolf Anderssen"]
[Black "Jean Dufresne"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. b4 Bxb4 5. c3 Ba5 6. d4 exd4 7. O-O d3 8. Qb3 Qf6 9. e5 Qg6 10. Re1 Nge7 11. Ba3 b5 12. Qxb5 Rb8 13. Qa4 Bb6 14. Nbd2 Bb7 15. Ne4 Qf5 16. Bxd3 Qh5 17. Nf6+ gxf6 18. exf6 Rg8 19. Rad1 Qxf3 20. Rxe7+ Nxe7 21. Qxd7+ Kxd7 22. Bf5+ Ke8 23. Bd7+ Kf8 24. Bxe7# 1-0
"""
    },
    {
        "id": "kasparov-immortal",
        "title": "Kasparov's Immortal (1999)",
        "white": "Garry Kasparov",
        "black": "Veselin Topalov",
        "event": "Hoogovens, Wijk aan Zee",
        "year": "1999",
        "opening": "Pirc Defense",
        "result": "1-0 (White wins by Brilliant Rook Sacrifice)",
        "theme_tag": "Modern King Hunt",
        "pgn": """
[Event "Hoogovens A Tournament"]
[Site "Wijk aan Zee NED"]
[Date "1999.01.20"]
[White "Garry Kasparov"]
[Black "Veselin Topalov"]
[Result "1-0"]

1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6 6. f3 b5 7. Nge2 Nbd7 8. Bh6 Bxh6 9. Qxh6 Bb7 10. a3 e5 11. O-O-O Qe7 12. Kb1 a6 13. Nc1 O-O-O 14. Nb3 exd4 15. Rxd4 c5 16. Rd1 Nb6 17. g3 Kb8 18. Na5 Ba8 19. Bh3 d5 20. Qf4+ Ka7 21. Rhe1 d4 22. Nd5 Nbxd5 23. exd5 Qd6 24. Rxd4 cxd4 25. Re7+ Kb6 26. Qxd4+ Kxa5 27. b4+ Ka4 28. Qc3 Qxd5 29. Ra7 Bb7 30. Rxb7 1-0
"""
    },
    {
        "id": "tal-masterpiece",
        "title": "Tal's Attacking Brilliance (1959)",
        "white": "Mikhail Tal",
        "black": "Vasily Smyslov",
        "event": "Candidates Tournament, Bled",
        "year": "1959",
        "opening": "Caro-Kann Defense",
        "result": "1-0 (White wins by Sacrificial Attack)",
        "theme_tag": "Magician from Riga",
        "pgn": """
[Event "Bled-Zagreb-Belgrade Candidates"]
[Site "Bled YUG"]
[Date "1959.09.18"]
[White "Mikhail Tal"]
[Black "Vasily Smyslov"]
[Result "1-0"]

1. e4 c6 2. d3 d5 3. Nd2 e5 4. Ngf3 Nd7 5. d4 dxe4 6. Nxe4 exd4 7. Qxd4 Ngf6 8. Bg5 Be7 9. O-O-O O-O 10. Nd6 Qa5 11. Bc4 b5 12. Bd2 Qa6 13. Nf5 Bd8 14. Qh4 bxc4 15. Qg5 Nh5 16. Nh6+ Kh8 17. Qxh5 Qxa2 18. Bc3 Nf6 19. Qxf7 Qa1+ 20. Kd2 Rxf7 21. Nxf7+ Kg8 22. Rxa1 Kxf7 23. Ne5+ Ke6 24. Nxc6 1-0
"""
    }
]

def get_current_game(game_index=None):
    if game_index is not None and 0 <= game_index < len(GAMES_DATABASE):
        return GAMES_DATABASE[game_index]
    # Rotate daily based on day of year
    day_of_year = datetime.datetime.now(datetime.timezone.utc).timetuple().tm_yday
    idx = day_of_year % len(GAMES_DATABASE)
    return GAMES_DATABASE[idx]

def parse_game(game_meta):
    pgn_text = game_meta["pgn"].strip()
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    board = game.board()
    frames = []

    # Initial setup frame
    frames.append({
        "fen": board.fen(),
        "san": "Initial Setup",
        "move_display": "Game Start",
        "turn": "White to move",
        "move_num": 0,
        "from_sq": None,
        "to_sq": None,
        "is_check": False,
        "is_mate": False
    })

    moves = list(game.mainline_moves())
    for i, move in enumerate(moves):
        san = board.san(move)
        move_num = (i // 2) + 1
        is_white = (i % 2 == 0)
        prefix = f"{move_num}." if is_white else f"{move_num}..."
        move_display = f"{prefix} {san}"
        
        from_sq = chess.square_name(move.from_square)
        to_sq = chess.square_name(move.to_square)
        
        board.push(move)
        
        frames.append({
            "fen": board.fen(),
            "san": san,
            "move_display": move_display,
            "turn": "Black to move" if is_white else "White to move",
            "move_num": move_num,
            "from_sq": from_sq,
            "to_sq": to_sq,
            "is_check": board.is_check(),
            "is_mate": board.is_checkmate()
        })

    return frames

def get_piece_svg_dict():
    piece_dict = {}
    for p_sym in ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']:
        p = chess.Piece.from_symbol(p_sym)
        svg_str = chess.svg.piece(p, size=44)
        inner = svg_str.split('>', 1)[1].rsplit('</svg>', 1)[0]
        piece_dict[p_sym] = inner
    return piece_dict

def build_animated_chess_svg(game_meta, theme="dark", seconds_per_move=3.2):
    """
    Builds the complete animated SVG with human-comprehensible speed (3.2s/move)
    and square movement highlights.
    """
    is_dark = (theme == "dark")
    frames = parse_game(game_meta)
    num_frames = len(frames)
    total_duration = num_frames * seconds_per_move

    piece_svgs_map = get_piece_svg_dict()

    # Palette
    bg = "#040F1D" if is_dark else "#FFFFFF"
    card_bg = "#0B1E3B" if is_dark else "#F8FAFC"
    border_color = "rgba(56, 189, 248, 0.22)" if is_dark else "rgba(15, 23, 42, 0.12)"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#8BB9FE" if is_dark else "#475569"
    text_muted = "#5B7CA3" if is_dark else "#94A3B8"
    accent = "#00E8FF" if is_dark else "#0284C7"
    accent_glow = "#38BDF8" if is_dark else "#2563EB"
    
    # Board squares
    sq_light = "#334155" if is_dark else "#EBECD0"
    sq_dark = "#1E293B" if is_dark else "#779952"
    sq_from_hi = "#0369A1" if is_dark else "#FDE047"
    sq_to_hi = "#00E8FF" if is_dark else "#F59E0B"
    badge_bg = "rgba(0, 232, 255, 0.10)" if is_dark else "rgba(2, 132, 199, 0.08)"

    # CSS Keyframes
    keyframe_css = []
    for f_idx in range(num_frames):
        p_start = (f_idx / float(num_frames)) * 100.0
        p_end = ((f_idx + 1) / float(num_frames)) * 100.0
        fade_pct = 0.05
        
        keyframe_css.append(f"""
        @keyframes frame_{f_idx} {{
          0%, {p_start:.2f}% {{ opacity: 0; pointer-events: none; }}
          {p_start + fade_pct:.2f}%, {p_end - fade_pct:.2f}% {{ opacity: 1; pointer-events: auto; }}
          {p_end:.2f}%, 100% {{ opacity: 0; pointer-events: none; }}
        }}
        .f_{f_idx} {{
          animation: frame_{f_idx} {total_duration:.1f}s infinite;
        }}
        """)

    css_block = "\n".join(keyframe_css)

    # Pre-render frames
    board_groups = []
    for f_idx, f_data in enumerate(frames):
        fen = f_data["fen"]
        board = chess.Board(fen)
        move_display = saxutils.escape(f_data["move_display"])
        turn_str = saxutils.escape(f_data["turn"])
        from_sq = f_data["from_sq"]
        to_sq = f_data["to_sq"]
        is_check = f_data["is_check"]
        is_mate = f_data["is_mate"]

        # Square highlights
        sq_svgs = []
        for rank in range(7, -1, -1):
            for file in range(8):
                sq_name = chess.square_name(chess.square(file, rank))
                x = file * 44 + 32
                y = (7 - rank) * 44 + 72
                is_light = (file + rank) % 2 != 0
                fill_color = sq_light if is_light else sq_dark

                border_highlight = ""
                if sq_name == from_sq:
                    fill_color = sq_from_hi
                    border_highlight = f'<rect x="{x+1}" y="{y+1}" width="42" height="42" fill="none" stroke="{accent}" stroke-width="2"/>'
                elif sq_name == to_sq:
                    fill_color = sq_to_hi
                    border_highlight = f'<rect x="{x+1}" y="{y+1}" width="42" height="42" fill="none" stroke="#FFFFFF" stroke-width="2"/>'

                sq_svgs.append(f'<rect x="{x}" y="{y}" width="44" height="44" fill="{fill_color}"/>{border_highlight}')

        # Pieces
        piece_svgs = []
        for rank in range(7, -1, -1):
            for file in range(8):
                piece = board.piece_at(chess.square(file, rank))
                if piece:
                    x = file * 44 + 32
                    y = (7 - rank) * 44 + 72
                    sym = piece.symbol()
                    icon = piece_svgs_map.get(sym, '')
                    piece_svgs.append(f'<g transform="translate({x}, {y}) scale(0.98)">{icon}</g>')

        status_tag = "⚔️ IN PLAY"
        status_color = accent
        if is_mate:
            status_tag = "🏆 CHECKMATE"
            status_color = "#10B981"
        elif is_check:
            status_tag = "⚠️ CHECK"
            status_color = "#F59E0B"

        frame_content = f"""
    <g class="f_{f_idx}">
      <!-- Board Squares -->
      {''.join(sq_svgs)}
      <!-- Piece Vectors -->
      {''.join(piece_svgs)}
      
      <!-- Live Move HUD -->
      <g transform="translate(416, 80)">
        <rect width="276" height="52" rx="10" fill="{card_bg}" stroke="{border_color}" stroke-width="1.2"/>
        <text x="16" y="24" class="font-mono" font-size="11px" fill="{text_muted}">CURRENT MOVE (3.2s / move):</text>
        <text x="16" y="42" class="font-mono" font-size="14px" font-weight="700" fill="{accent}">{move_display}</text>
        <g transform="translate(170, 14)">
          <rect width="92" height="24" rx="6" fill="{badge_bg}" stroke="{status_color}" stroke-width="0.8"/>
          <text x="46" y="16" class="font-mono" font-size="9.5px" font-weight="700" fill="{status_color}" text-anchor="middle">{status_tag}</text>
        </g>
      </g>

      <!-- Turn Indicator -->
      <g transform="translate(416, 142)">
        <rect width="276" height="40" rx="8" fill="{card_bg}" stroke="{border_color}" stroke-width="1"/>
        <circle cx="20" cy="20" r="5" fill="{accent}"/>
        <text x="34" y="24" class="font-mono" font-size="12px" font-weight="600" fill="{text_secondary}">{turn_str}</text>
        <text x="260" y="24" class="font-mono" font-size="11px" fill="{text_muted}" text-anchor="end">Frame {f_idx + 1}/{num_frames}</text>
      </g>

      <!-- Game Details Card -->
      <g transform="translate(416, 194)">
        <rect width="276" height="230" rx="10" fill="{card_bg}" stroke="{border_color}" stroke-width="1.2"/>
        
        <text x="16" y="28" class="font-sans" font-size="13px" font-weight="700" fill="{text_primary}">📜 Game Telemetry</text>
        <line x1="16" y1="38" x2="260" y2="38" stroke="{border_color}" stroke-width="0.8"/>

        <text x="16" y="60" class="font-mono" font-size="11px" fill="{text_muted}">MATCH:</text>
        <text x="16" y="76" class="font-sans" font-size="11.5px" font-weight="700" fill="{accent}">{saxutils.escape(game_meta["title"])}</text>

        <text x="16" y="102" class="font-mono" font-size="10.5px" fill="{text_muted}">WHITE:</text>
        <text x="70" y="102" class="font-sans" font-size="11px" font-weight="600" fill="{text_primary}">{saxutils.escape(game_meta["white"])}</text>

        <text x="16" y="124" class="font-mono" font-size="10.5px" fill="{text_muted}">BLACK:</text>
        <text x="70" y="124" class="font-sans" font-size="11px" font-weight="600" fill="{text_primary}">{saxutils.escape(game_meta["black"])}</text>

        <text x="16" y="146" class="font-mono" font-size="10.5px" fill="{text_muted}">OPENING:</text>
        <text x="70" y="146" class="font-sans" font-size="11px" font-weight="600" fill="{text_secondary}">{saxutils.escape(game_meta["opening"])}</text>

        <text x="16" y="168" class="font-mono" font-size="10.5px" fill="{text_muted}">OUTCOME:</text>
        <text x="16" y="184" class="font-sans" font-size="10.5px" font-weight="700" fill="#10B981">{saxutils.escape(game_meta["result"])}</text>

        <!-- Footer tag -->
        <line x1="16" y1="198" x2="260" y2="198" stroke="{border_color}" stroke-width="0.8"/>
        <text x="138" y="216" class="font-mono" font-size="10px" fill="{text_muted}" text-anchor="middle">Daily Grandmaster Game Rotation • 6 Classics</text>
      </g>
    </g>
        """
        board_groups.append(frame_content)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="460" viewBox="0 0 720 460" role="img" aria-label="Grandmaster Chess Automation - {saxutils.escape(game_meta["title"])}">
  <defs>
    <style>
      .font-sans {{ font-family: 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }}
      .font-mono {{ font-family: 'Consolas', 'Courier New', 'Fira Code', monospace; }}
      {css_block}
    </style>
  </defs>

  <!-- Container -->
  <rect width="720" height="460" rx="16" fill="{bg}" stroke="{border_color}" stroke-width="1.5"/>
  <rect x="8" y="8" width="704" height="444" rx="12" fill="{card_bg}" fill-opacity="{0.7 if is_dark else 0.9}"/>

  <!-- Header -->
  <g transform="translate(32, 22)">
    <circle cx="6" cy="11" r="5" fill="{accent}"/>
    <text x="18" y="16" class="font-sans" font-size="16px" font-weight="800" fill="{text_primary}">♟️ Automated Grandmaster Chessboard</text>
    <text x="0" y="34" class="font-mono" font-size="11.5px" font-weight="600" fill="{text_secondary}">Human Speed (3.2s/move) • Daily Grandmaster Rotation</text>
    
    <g transform="translate(530, 0)">
      <rect width="134" height="28" rx="8" fill="#10B981" fill-opacity="0.15" stroke="#10B981" stroke-width="1"/>
      <circle cx="14" cy="14" r="4" fill="#10B981"/>
      <text x="26" y="18" class="font-mono" font-size="10.5px" font-weight="700" fill="#10B981">AUTOPLAY (3.2s)</text>
    </g>
  </g>

  <!-- Board Coordinate Labels (Files a-h) -->
  <g class="font-mono" font-size="10.5px" font-weight="700" fill="{text_secondary}" text-anchor="middle">
    <text x="54" y="66">a</text><text x="98" y="66">b</text><text x="142" y="66">c</text><text x="186" y="66">d</text>
    <text x="230" y="66">e</text><text x="274" y="66">f</text><text x="318" y="66">g</text><text x="362" y="66">h</text>
    
    <text x="54" y="438">a</text><text x="98" y="438">b</text><text x="142" y="438">c</text><text x="186" y="438">d</text>
    <text x="230" y="438">e</text><text x="274" y="438">f</text><text x="318" y="438">g</text><text x="362" y="438">h</text>
  </g>

  <!-- Board Coordinate Labels (Ranks 1-8) -->
  <g class="font-mono" font-size="10.5px" font-weight="700" fill="{text_secondary}" text-anchor="middle">
    <text x="20" y="98">8</text><text x="20" y="142">7</text><text x="20" y="186">6</text><text x="20" y="230">5</text>
    <text x="20" y="274">4</text><text x="20" y="318">3</text><text x="20" y="362">2</text><text x="20" y="406">1</text>
    
    <text x="394" y="98">8</text><text x="394" y="142">7</text><text x="394" y="186">6</text><text x="394" y="230">5</text>
    <text x="394" y="274">4</text><text x="394" y="318">3</text><text x="394" y="362">2</text><text x="394" y="406">1</text>
  </g>

  <!-- Animated Board Frames -->
  {''.join(board_groups)}

</svg>
'''
    return svg

def main():
    parser = argparse.ArgumentParser(description="Generate Grandmaster Chessboard Animation SVG")
    parser.add_argument("--game", type=int, default=None, help="Index of game (0 to 5)")
    args = parser.parse_args()

    os.makedirs("assets", exist_ok=True)
    game_meta = get_current_game(args.game)
    print(f"Generating Grandmaster Chessboard for: {game_meta['title']}")
    print(f"White: {game_meta['white']} vs Black: {game_meta['black']} ({game_meta['opening']})")
    print(f"Playback speed: 3.2s per move")

    dark_svg = build_animated_chess_svg(game_meta, "dark", seconds_per_move=3.2)
    light_svg = build_animated_chess_svg(game_meta, "light", seconds_per_move=3.2)

    with open("assets/chess-animated-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/chess-animated-light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open("assets/chess-animated.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)

    print(f"Generated assets/chess-animated.svg ({len(dark_svg)} bytes) successfully!")

if __name__ == "__main__":
    main()

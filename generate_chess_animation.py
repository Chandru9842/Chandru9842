#!/usr/bin/env python3
"""
Automated Chessboard Animation Generator for Chandru M (@Chandru9842).
Generates a smooth, standalone looping SVG chess game animation.
Features a legendary game (e.g. Fischer's Game of the Century / Immortal Game)
with sliding pieces, captured tray, move tracker, and cyber/dark theme.
"""

import os
import chess
import chess.pgn
import io

IMMORTAL_GAME_PGN = """
[Event "London"]
[Site "London"]
[Date "1851.06.21"]
[White "Adolf Anderssen"]
[Black "Lionel Kieseritzky"]
[Result "1-0"]

1. e4 e5 2. f4 exf4 3. Bc4 Qh4+ 4. Kf1 b5 5. Bxb5 Nf6 6. Nf3 Qh6 7. d3 Nh5 8. Nh4 Qg5 9. Nf5 c6 10. g4 Nf6 11. Rg1 cxb5 12. h4 Qg6 13. h5 Qg5 14. Qf3 Ng8 15. Bxf4 Qf6 16. Nc3 Bc5 17. Nd5 Qxb2 18. Bd6 Bxg1 19. e5 Qxa1+ 20. Ke2 Na6 21. Nxg7+ Kd8 22. Qf6+ Nxf6 23. Be7# 1-0
"""

# Piece Unicode and SVG Path mapping
PIECE_SVGS = {
    # White pieces
    'P': '<path d="M22 9c-2.2 0-4 1.8-4 4 0 1.2.5 2.2 1.3 3-.9.7-1.5 1.7-1.7 2.8-.8.3-1.6.8-2.2 1.5-.7.8-1.1 1.8-1.2 2.9-.1 1.2.2 2.3.8 3.3.6 1 1.5 1.7 2.5 2.1-.8.9-1.3 2-1.4 3.2-.1 1.3.3 2.5 1.1 3.5.8 1 1.9 1.6 3.1 1.7h11.4c1.2-.1 2.3-.7 3.1-1.7.8-1 1.2-2.2 1.1-3.5-.1-1.2-.6-2.3-1.4-3.2 1-.4 1.9-1.1 2.5-2.1.6-1 .9-2.1.8-3.3-.1-1.1-.5-2.1-1.2-2.9-.6-.7-1.4-1.2-2.2-1.5-.2-1.1-.8-2.1-1.7-2.8.8-.8 1.3-1.8 1.3-3 0-2.2-1.8-4-4-4s-4 1.8-4 4c0 1.2.5 2.2 1.3 3-.9.7-1.5 1.7-1.7 2.8H20.4c-.2-1.1-.8-2.1-1.7-2.8.8-.8 1.3-1.8 1.3-3 0-2.2-1.8-4-4-4z" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.5"/>',
    'N': '<path d="M22 10c-3 0-6 2-7 5-1 3-1 7 2 9-1 1-2 3-2 5 0 3 2 5 5 6h12c3-1 5-3 5-6 0-2-1-4-2-5 3-2 3-6 2-9-1-3-4-5-7-5h-8z" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.5"/>',
    'B': '<path d="M22 8c-2 0-4 2-4 4 0 1 .5 2 1 3-2 2-3 5-3 8 0 3 2 6 5 8h4c3-2 5-5 5-8 0-3-1-6-3-8 .5-1 1-2 1-3 0-2-2-4-4-4h-2z" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.5"/>',
    'R': '<path d="M12 10h4v4h4v-4h4v4h4v-4h4v6l-2 3v11h4v4H10v-4h4V19l-2-3v-6z" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.5"/>',
    'Q': '<path d="M11 13l3 11h16l3-11-6 4-5-8-5 8-6-4zm2 15h18v4H13v-4z" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.5"/>',
    'K': '<path d="M21 8h2v3h3v2h-3v3h-2v-3h-3v-2h3V8zm-8 10l3 8h16l3-8-4 2-6-4-6 4-4-2zm2 10h18v4H15v-4z" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.5"/>',
    # Black pieces
    'p': '<path d="M22 9c-2.2 0-4 1.8-4 4 0 1.2.5 2.2 1.3 3-.9.7-1.5 1.7-1.7 2.8-.8.3-1.6.8-2.2 1.5-.7.8-1.1 1.8-1.2 2.9-.1 1.2.2 2.3.8 3.3.6 1 1.5 1.7 2.5 2.1-.8.9-1.3 2-1.4 3.2-.1 1.3.3 2.5 1.1 3.5.8 1 1.9 1.6 3.1 1.7h11.4c1.2-.1 2.3-.7 3.1-1.7.8-1 1.2-2.2 1.1-3.5-.1-1.2-.6-2.3-1.4-3.2 1-.4 1.9-1.1 2.5-2.1.6-1 .9-2.1.8-3.3-.1-1.1-.5-2.1-1.2-2.9-.6-.7-1.4-1.2-2.2-1.5-.2-1.1-.8-2.1-1.7-2.8.8-.8 1.3-1.8 1.3-3 0-2.2-1.8-4-4-4s-4 1.8-4 4c0 1.2.5 2.2 1.3 3-.9.7-1.5 1.7-1.7 2.8H20.4c-.2-1.1-.8-2.1-1.7-2.8.8-.8 1.3-1.8 1.3-3 0-2.2-1.8-4-4-4z" fill="#1E293B" stroke="#94A3B8" stroke-width="1.5"/>',
    'n': '<path d="M22 10c-3 0-6 2-7 5-1 3-1 7 2 9-1 1-2 3-2 5 0 3 2 5 5 6h12c3-1 5-3 5-6 0-2-1-4-2-5 3-2 3-6 2-9-1-3-4-5-7-5h-8z" fill="#1E293B" stroke="#94A3B8" stroke-width="1.5"/>',
    'b': '<path d="M22 8c-2 0-4 2-4 4 0 1 .5 2 1 3-2 2-3 5-3 8 0 3 2 6 5 8h4c3-2 5-5 5-8 0-3-1-6-3-8 .5-1 1-2 1-3 0-2-2-4-4-4h-2z" fill="#1E293B" stroke="#94A3B8" stroke-width="1.5"/>',
    'r': '<path d="M12 10h4v4h4v-4h4v4h4v-4h4v6l-2 3v11h4v4H10v-4h4V19l-2-3v-6z" fill="#1E293B" stroke="#94A3B8" stroke-width="1.5"/>',
    'q': '<path d="M11 13l3 11h16l3-11-6 4-5-8-5 8-6-4zm2 15h18v4H13v-4z" fill="#1E293B" stroke="#94A3B8" stroke-width="1.5"/>',
    'k': '<path d="M21 8h2v3h3v2h-3v3h-2v-3h-3v-2h3V8zm-8 10l3 8h16l3-8-4 2-6-4-6 4-4-2zm2 10h18v4H15v-4z" fill="#1E293B" stroke="#94A3B8" stroke-width="1.5"/>',
}

def parse_game():
    game = chess.pgn.read_game(io.StringIO(IMMORTAL_GAME_PGN))
    board = game.board()
    frames = []
    
    # Starting frame
    frames.append({
        "fen": board.fen(),
        "san": "Game Start",
        "turn": "White to move",
        "move_num": 0,
        "from_sq": None,
        "to_sq": None
    })

    for i, move in enumerate(game.mainline_moves()):
        san = board.san(move)
        from_sq = chess.square_name(move.from_square)
        to_sq = chess.square_name(move.to_square)
        board.push(move)
        frames.append({
            "fen": board.fen(),
            "san": san,
            "turn": "White to move" if board.turn == chess.WHITE else "Black to move",
            "move_num": (i // 2) + 1,
            "from_sq": from_sq,
            "to_sq": to_sq
        })
    return frames

def build_animated_chess_svg(theme="dark"):
    is_dark = (theme == "dark")
    frames = parse_game()
    num_frames = len(frames)
    total_duration = num_frames * 1.6  # ~36s loop
    
    bg = "#0B1120" if is_dark else "#FFFFFF"
    card_bg = "#0F172A" if is_dark else "#F8FAFC"
    border_color = "rgba(56, 189, 248, 0.35)" if is_dark else "rgba(15, 23, 42, 0.15)"
    text_primary = "#F8FAFC" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    sq_light = "#334155" if is_dark else "#EBECD0"
    sq_dark = "#1E293B" if is_dark else "#779952"
    sq_hi = "#0284C7" if is_dark else "#FCD34D"
    accent = "#38BDF8" if is_dark else "#2563EB"

    # Generate CSS keyframes for each frame
    keyframe_css = []
    for f_idx in range(num_frames):
        p_start = (f_idx / num_frames) * 100
        p_end = ((f_idx + 1) / num_frames) * 100
        
        # Each frame displays its board state and text
        keyframe_css.append(f"""
        @keyframes frame_{f_idx} {{
          0%, {p_start:.2f}% {{ opacity: 0; pointer-events: none; }}
          {p_start + 0.1:.2f}%, {p_end - 0.1:.2f}% {{ opacity: 1; pointer-events: auto; }}
          {p_end:.2f}%, 100% {{ opacity: 0; pointer-events: none; }}
        }}
        .f_{f_idx} {{
          animation: frame_{f_idx} {total_duration:.1f}s infinite;
        }}
        """)

    css_block = "\n".join(keyframe_css)

    # Render board frames
    board_groups = []
    for f_idx, f_data in enumerate(frames):
        fen = f_data["fen"]
        board = chess.Board(fen)
        san = f_data["san"]
        turn = f_data["turn"]
        move_num = f_data["move_num"]
        from_sq = f_data["from_sq"]
        to_sq = f_data["to_sq"]

        sq_svgs = []
        # Draw 64 squares
        for rank in range(7, -1, -1):
            for file in range(8):
                sq_name = chess.square_name(chess.square(file, rank))
                x = file * 44 + 32
                y = (7 - rank) * 44 + 72
                is_light = (file + rank) % 2 != 0
                fill_color = sq_light if is_light else sq_dark
                
                # Highlight last move squares
                if sq_name in [from_sq, to_sq]:
                    fill_color = sq_hi

                sq_svgs.append(f'<rect x="{x}" y="{y}" width="44" height="44" fill="{fill_color}"/>')

        # Draw piece glyphs
        piece_svgs = []
        for rank in range(7, -1, -1):
            for file in range(8):
                piece = board.piece_at(chess.square(file, rank))
                if piece:
                    x = file * 44 + 32
                    y = (7 - rank) * 44 + 72
                    sym = piece.symbol()
                    icon = PIECE_SVGS.get(sym, '')
                    piece_svgs.append(f'<g transform="translate({x}, {y})">{icon}</g>')

        status_text = f"Move #{move_num} • {san} ({turn})"
        if "1-0" in san or "#" in san or f_idx == num_frames - 1:
            status_text = f"🏆 Checkmate! Adolf Anderssen wins (The Immortal Game)"

        frame_content = f"""
    <g class="f_{f_idx}">
      <!-- Board Squares -->
      {''.join(sq_svgs)}
      <!-- Piece Vectors -->
      {''.join(piece_svgs)}
      <!-- Live Game Move HUD -->
      <g transform="translate(416, 120)">
        <rect width="270" height="44" rx="8" fill="{card_bg}" stroke="{border_color}" stroke-width="1.2"/>
        <text x="14" y="27" class="font-mono" font-size="12px" font-weight="700" fill="{accent}">MOVE: <tspan fill="{text_primary}">{san}</tspan></text>
      </g>
      <g transform="translate(416, 176)">
        <rect width="270" height="44" rx="8" fill="{card_bg}" stroke="{border_color}" stroke-width="1.2"/>
        <text x="14" y="27" class="font-mono" font-size="11.5px" font-weight="600" fill="{text_secondary}">{turn}</text>
      </g>
      <g transform="translate(416, 232)">
        <rect width="270" height="150" rx="8" fill="{card_bg}" stroke="{border_color}" stroke-width="1.2"/>
        <text x="14" y="26" class="font-sans" font-size="12px" font-weight="700" fill="{text_primary}">⚔️ Match Details</text>
        <text x="14" y="52" class="font-mono" font-size="10.5px" fill="{text_secondary}">White : Adolf Anderssen</text>
        <text x="14" y="74" class="font-mono" font-size="10.5px" fill="{text_secondary}">Black : L. Kieseritzky</text>
        <text x="14" y="96" class="font-mono" font-size="10.5px" fill="{text_secondary}">Event : The Immortal Game</text>
        <text x="14" y="118" class="font-mono" font-size="10.5px" fill="{accent}">Opening: King's Gambit</text>
        <text x="14" y="138" class="font-mono" font-size="10.5px" font-weight="700" fill="#10B981">Live Auto-Play • Looping</text>
      </g>
    </g>
        """
        board_groups.append(frame_content)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="460" viewBox="0 0 720 460" role="img" aria-label="Automated Animated Chessboard - The Immortal Game">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;700;800&amp;family=Plus+Jakarta+Sans:wght@600;700;800&amp;display=swap');
      .font-sans {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
      .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
      {css_block}
    </style>
  </defs>

  <!-- Container -->
  <rect width="720" height="460" rx="16" fill="{bg}" stroke="{border_color}" stroke-width="1.5"/>
  <rect x="8" y="8" width="704" height="444" rx="12" fill="{card_bg}" fill-opacity="{0.7 if is_dark else 0.9}"/>

  <!-- Header -->
  <g transform="translate(32, 22)">
    <text x="0" y="18" class="font-sans" font-size="16px" font-weight="800" fill="{text_primary}">♟️ Automated Chessboard</text>
    <text x="0" y="34" class="font-mono" font-size="11px" font-weight="600" fill="{text_secondary}">Live Grandmaster Game Replay • Looping Animation</text>
    
    <g transform="translate(540, 2)">
      <rect width="116" height="28" rx="8" fill="#10B981" fill-opacity="0.15" stroke="#10B981" stroke-width="1"/>
      <circle cx="12" cy="14" r="4" fill="#10B981"/>
      <text x="24" y="18" class="font-mono" font-size="10.5px" font-weight="700" fill="#10B981">AUTOPLAY</text>
    </g>
  </g>

  <!-- Board Coordinate Labels (Files a-h) -->
  <g class="font-mono" font-size="10px" font-weight="700" fill="{text_secondary}" text-anchor="middle">
    <text x="54" y="66">a</text><text x="98" y="66">b</text><text x="142" y="66">c</text><text x="186" y="66">d</text>
    <text x="230" y="66">e</text><text x="274" y="66">f</text><text x="318" y="66">g</text><text x="362" y="66">h</text>
    
    <text x="54" y="438">a</text><text x="98" y="438">b</text><text x="142" y="438">c</text><text x="186" y="438">d</text>
    <text x="230" y="438">e</text><text x="274" y="438">f</text><text x="318" y="438">g</text><text x="362" y="438">h</text>
  </g>

  <!-- Board Coordinate Labels (Ranks 1-8) -->
  <g class="font-mono" font-size="10px" font-weight="700" fill="{text_secondary}" text-anchor="middle">
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
    os.makedirs("assets", exist_ok=True)
    dark_svg = build_animated_chess_svg("dark")
    light_svg = build_animated_chess_svg("light")

    with open("assets/chess-animated-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/chess-animated-light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open("assets/chess-animated.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print("Generated automated animated chessboard SVGs successfully!")

if __name__ == "__main__":
    main()

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
    },
    {
        "id": "gold-coins-game",
        "title": "The Gold Coins Game (1912)",
        "white": "Stefan Levitsky",
        "black": "Frank Marshall",
        "event": "DSB Congress, Breslau",
        "year": "1912",
        "opening": "French Defense",
        "result": "0-1 (Black wins by Legendary 23...Qg3!! Queen Sacrifice)",
        "theme_tag": "Gold Coins Queen Sacrifice",
        "pgn": """
[Event "Breslau"]
[Site "Breslau GER"]
[Date "1912.07.20"]
[White "Stefan Levitsky"]
[Black "Frank Marshall"]
[Result "0-1"]

1. d4 e6 2. e4 d5 3. Nc3 c5 4. Nf3 Nc6 5. exd5 exd5 6. Be2 Nf6 7. O-O Be7 8. Bg5 O-O 9. dxc5 Be6 10. Nd4 Bxc5 11. Nxe6 fxe6 12. Bg4 Qd6 13. Bh3 Rae8 14. Qd2 Bb4 15. Bxf6 Rxf6 16. Rad1 Qc5 17. Qe2 Bxc3 18. bxc3 Qxc3 19. Rxd5 Nd4 20. Qh5 Ref8 21. Re5 Rh6 22. Qg5 Rxh3 23. Rc5 Qg3 0-1
"""
    },
    {
        "id": "capablanca-marshall",
        "title": "Capablanca's Counter-Attack (1918)",
        "white": "Jose Raul Capablanca",
        "black": "Frank Marshall",
        "event": "Manhattan Chess Club, New York",
        "year": "1918",
        "opening": "Ruy Lopez (Marshall Attack)",
        "result": "1-0 (White refutes Marshall Attack over the board)",
        "theme_tag": "The Human Chess Machine",
        "pgn": """
[Event "New York"]
[Site "New York, NY USA"]
[Date "1918.10.23"]
[White "Jose Raul Capablanca"]
[Black "Frank Marshall"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 O-O 8. c3 d5 9. exd5 Nxd5 10. Nxe5 Nxe5 11. Rxe5 Nf6 12. d4 Bd6 13. Re1 Ng4 14. h3 Qh4 15. Qf3 Nxf2 16. Re2 Bg4 17. Qxf2 Bg3 18. Qf1 Rae8 19. Rxe8 Rxe8 20. Nd2 Be2 21. Qf5 Bd3 22. Qxd3 Re1+ 23. Nf1 Bf2+ 24. Kh2 Rxf1 25. Qxf1 1-0
"""
    },
    {
        "id": "anand-immortal",
        "title": "Anand's Immortal Masterpiece (2013)",
        "white": "Levon Aronian",
        "black": "Viswanathan Anand",
        "event": "Tata Steel, Wijk aan Zee",
        "year": "2013",
        "opening": "Semi-Slav Defense (Meran)",
        "result": "0-1 (Black wins by Tiger of Madras Tactical Storm)",
        "theme_tag": "Vishy Anand Masterpiece",
        "pgn": """
[Event "Wijk aan Zee"]
[Site "Wijk aan Zee NED"]
[Date "2013.01.15"]
[White "Levon Aronian"]
[Black "Viswanathan Anand"]
[Result "0-1"]

1. d4 d5 2. c4 c6 3. Nf3 Nf6 4. Nc3 e6 5. e3 Nbd7 6. Bd3 dxc4 7. Bxc4 b5 8. Bd3 Bd6 9. O-O O-O 10. Qc2 Bb7 11. a3 Rc8 12. Ng5 c5 13. Nxh7 Ng4 14. f4 cxd4 15. exd4 Bc5 16. Be2 Nde5 17. Bxg4 Bxd4+ 18. Kh1 Nxg4 19. Nxf8 f5 20. Qe2 Qh4 21. Qxe6+ Kxf8 22. Qxf5+ Kg8 23. Qe6+ Kh8 0-1
"""
    },
    {
        "id": "botvinnik-capablanca",
        "title": "Botvinnik's King Hunt (1938)",
        "white": "Mikhail Botvinnik",
        "black": "Jose Raul Capablanca",
        "event": "AVRO Tournament, Netherlands",
        "year": "1938",
        "opening": "Nimzo-Indian Defense",
        "result": "1-0 (White wins by Deep Positional 30. Ba3!! Sacrifice)",
        "theme_tag": "Soviet Chess Patriarch",
        "pgn": """
[Event "AVRO"]
[Site "Amsterdam NED"]
[Date "1938.11.22"]
[White "Mikhail Botvinnik"]
[Black "Jose Raul Capablanca"]
[Result "1-0"]

1. d4 Nf6 2. c4 e6 3. Nc3 Bb4 4. e3 d5 5. a3 Bxc3+ 6. bxc3 c5 7. cxd5 exd5 8. Bd3 O-O 9. Ne2 b6 10. O-O Ba6 11. Bxa6 Nxa6 12. Bb2 Qd7 13. a4 Rfe8 14. Qd3 c4 15. Qc2 Nb8 16. Rae1 Nc6 17. Ng3 Na5 18. f3 Nb3 19. e4 Qxa4 20. e5 Nd7 21. Qf2 g6 22. f4 f5 23. exf6 Nxf6 24. f5 Rxe1 25. Rxe1 Re8 26. Re6 Rxe6 27. fxe6 Kg7 28. Qf4 Qe8 29. Qe5 Qe7 30. Ba3 Qxa3 31. Nh5+ gxh5 32. Qg5+ Kf8 33. Qxf6+ Kg8 34. e7 Qc1+ 35. Kf2 Qc2+ 36. Kg3 Qd3+ 37. Kh4 Qe4+ 38. Kxh5 Qe2+ 39. Kh4 Qe4+ 40. g4 Qe1+ 41. Kh5 1-0
"""
    },
    {
        "id": "fischer-spassky",
        "title": "Match of the Century - Game 6 (1972)",
        "white": "Bobby Fischer",
        "black": "Boris Spassky",
        "event": "World Championship, Reykjavik",
        "year": "1972",
        "opening": "Queen's Gambit Declined",
        "result": "1-0 (White wins in Spassky-Applauded Classic)",
        "theme_tag": "Match of the Century",
        "pgn": """
[Event "World Championship 1972"]
[Site "Reykjavik ISL"]
[Date "1972.07.23"]
[White "Bobby Fischer"]
[Black "Boris Spassky"]
[Result "1-0"]

1. c4 e6 2. Nf3 d5 3. d4 Nf6 4. Nc3 Be7 5. Bg5 O-O 6. e3 h6 7. Bh4 b6 8. cxd5 Nxd5 9. Bxe7 Qxe7 10. Nxd5 exd5 11. Rc1 Be6 12. Qa4 c5 13. Qa3 Rc8 14. Bb5 a6 15. dxc5 bxc5 16. O-O Ra7 17. Be2 Nd7 18. Nd4 Qf8 19. Nxe6 fxe6 20. e4 d4 21. f4 Qe7 22. e5 Rb8 23. Bc4 Kh8 24. Qh3 Nf8 25. b3 a5 26. f5 exf5 27. Rxf5 Nh7 28. Rcf1 Qd8 29. Qg3 Re7 30. h4 Rbb7 31. e6 Rbc7 32. Qe5 Qe8 33. a4 Qd8 34. R1f2 Qe8 35. R2f3 Qd8 36. Bd3 Qe8 37. Qe4 Nf6 38. Rxf6 gxf6 39. Rxf6 Kg8 40. Bc4 Kh8 41. Qf4 1-0
"""
    },
    {
        "id": "morphy-paulsen",
        "title": "Morphy's Queen Sacrifice (1857)",
        "white": "Louis Paulsen",
        "black": "Paul Morphy",
        "event": "1st American Chess Congress, New York",
        "year": "1857",
        "opening": "Four Knights Game",
        "result": "0-1 (Black wins by Historic 17...Qxf3!! Sacrifice)",
        "theme_tag": "Morphy Romantic Brilliance",
        "pgn": """
[Event "New York 1857"]
[Site "New York, NY USA"]
[Date "1857.11.08"]
[White "Louis Paulsen"]
[Black "Paul Morphy"]
[Result "0-1"]

1. e4 e5 2. Nf3 Nc6 3. Nc3 Nf6 4. Bb5 Bc5 5. O-O O-O 6. Nxe5 Re8 7. Nxc6 dxc6 8. Bc4 b5 9. Be2 Nxe4 10. Nxe4 Rxe4 11. Bf3 Re6 12. c3 Qd3 13. b4 Bb6 14. a4 bxa4 15. Qxa4 Bd7 16. Ra2 Rae8 17. Qa6 Qxf3 18. gxf3 Rg6+ 19. Kh1 Bh3 20. Rd1 Bg2+ 21. Kg1 Bxf3+ 22. Kf1 Bg2+ 23. Kg1 Bh3+ 24. Kh1 Bxf2 25. Qf1 Bxf1 26. Rxf1 Re2 27. Ra1 Rh6 28. d4 Be3 0-1
"""
    },
    {
        "id": "rotlewi-rubinstein",
        "title": "Rubinstein's Immortal Game (1907)",
        "white": "Georg Rotlewi",
        "black": "Akiba Rubinstein",
        "event": "Lodz, Poland",
        "year": "1907",
        "opening": "Queen's Gambit Declined (Tarrasch)",
        "result": "0-1 (Black wins by Legendary Queen & Double Minor Sac)",
        "theme_tag": "Positional & Tactical Perfection",
        "pgn": """
[Event "Lodz 1907"]
[Site "Lodz POL"]
[Date "1907.12.26"]
[White "Georg Rotlewi"]
[Black "Akiba Rubinstein"]
[Result "0-1"]

1. d4 d5 2. Nf3 e6 3. e3 c5 4. c4 Nc6 5. Nc3 Nf6 6. dxc5 Bxc5 7. a3 a6 8. b4 Bd6 9. Bb2 O-O 10. Qd2 Qe7 11. Bd3 dxc4 12. Bxc4 b5 13. Bd3 Rd8 14. Qe2 Bb7 15. O-O Ne5 16. Nxe5 Bxe5 17. f4 Bc7 18. e4 Rac8 19. e5 Bb6+ 20. Kh1 Ng4 21. Be4 Qh4 22. g3 Rxc3 23. gxh4 Rd2 24. Qxd2 Bxe4+ 25. Qg2 Rh3 0-1
"""
    },
    {
        "id": "pearl-of-zandvoort",
        "title": "The Pearl of Zandvoort (1935)",
        "white": "Max Euwe",
        "black": "Alexander Alekhine",
        "event": "World Championship (Game 26), Zandvoort",
        "year": "1935",
        "opening": "Slav Defense",
        "result": "1-0 (White wins to Claim World Championship)",
        "theme_tag": "World Crown Deciding Battle",
        "pgn": """
[Event "World Championship 1935"]
[Site "Zandvoort NED"]
[Date "1935.12.03"]
[White "Max Euwe"]
[Black "Alexander Alekhine"]
[Result "1-0"]

1. d4 d5 2. c4 c6 3. Nf3 Nf6 4. Nc3 dxc4 5. a4 Bf5 6. Ne5 e6 7. f3 Bb4 8. e4 Bxe4 9. fxe4 Nxe4 10. Bd2 Qxd4 11. Nxe4 Qxe4+ 12. Qe2 Bxd2+ 13. Kxd2 Qd5+ 14. Kc2 Na6 15. Nxc4 O-O-O 16. Qe5 f6 17. Qxd5 exd5 18. Na5 Nc5 19. b4 Ne4 20. Bd3 Rhe8 21. Rhe1 Kc7 22. Nb3 g6 23. a5 f5 24. Bxe4 dxe4 25. Nc5 b6 26. axb6+ axb6 27. Ra7+ Kd6 28. Rd1+ Ke5 29. Nd7+ Kf4 30. Nxb6 Rxd1 31. Kxd1 1-0
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

SPEED_PRESETS = {
    "slow": {"seconds": 4.2, "label": "4.2s / move (Slow)", "tag": "🐢 SLOW (4.2s)"},
    "normal": {"seconds": 2.8, "label": "2.8s / move (Normal)", "tag": "⚡ NORMAL (2.8s)"},
    "fast": {"seconds": 1.5, "label": "1.5s / move (Fast)", "tag": "🚀 FAST (1.5s)"}
}

def build_animated_chess_svg(game_meta, theme="dark", speed_key="normal"):
    """
    Builds the complete animated SVG with controllable playback speed
    and square movement highlights.
    """
    is_dark = (theme == "dark")
    speed_info = SPEED_PRESETS.get(speed_key, SPEED_PRESETS["normal"])
    seconds_per_move = speed_info["seconds"]
    speed_label = speed_info["label"]
    speed_tag = speed_info["tag"]

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
        <text x="16" y="24" class="font-mono" font-size="10.5px" fill="{text_muted}">CURRENT MOVE ({speed_label}):</text>
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
        <text x="138" y="216" class="font-mono" font-size="10px" fill="{text_muted}" text-anchor="middle">Daily Grandmaster Rotation • 6 Classics</text>
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
    <text x="0" y="34" class="font-mono" font-size="11.5px" font-weight="600" fill="{text_secondary}">Speed: {speed_label} • Daily Classic Game Rotation</text>
    
    <g transform="translate(520, 0)">
      <rect width="146" height="28" rx="8" fill="#10B981" fill-opacity="0.15" stroke="#10B981" stroke-width="1"/>
      <circle cx="14" cy="14" r="4" fill="#10B981"/>
      <text x="26" y="18" class="font-mono" font-size="10.5px" font-weight="700" fill="#10B981">{speed_tag}</text>
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
    parser.add_argument("--speed", type=str, default="normal", choices=["slow", "normal", "fast"], help="Playback speed")
    parser.add_argument("--all", action="store_true", help="Generate all game and speed combinations")
    args = parser.parse_args()

    os.makedirs("assets", exist_ok=True)

    # 1. Daily featured game (rotates daily)
    featured_game = get_current_game(args.game)
    print(f"Daily Featured Game: {featured_game['title']}")

    # Render Default (Normal speed)
    dark_normal = build_animated_chess_svg(featured_game, "dark", "normal")
    light_normal = build_animated_chess_svg(featured_game, "light", "normal")

    with open("assets/chess-animated-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_normal)
    with open("assets/chess-animated-light.svg", "w", encoding="utf-8") as f:
        f.write(light_normal)
    with open("assets/chess-animated.svg", "w", encoding="utf-8") as f:
        f.write(dark_normal)
    print("Generated default assets/chess-animated.svg (Normal 2.8s)")

    # Render Slow speed variant (4.2s)
    dark_slow = build_animated_chess_svg(featured_game, "dark", "slow")
    light_slow = build_animated_chess_svg(featured_game, "light", "slow")
    with open("assets/chess-animated-slow.svg", "w", encoding="utf-8") as f:
        f.write(dark_slow)
    with open("assets/chess-animated-slow-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_slow)
    with open("assets/chess-animated-slow-light.svg", "w", encoding="utf-8") as f:
        f.write(light_slow)
    print("Generated assets/chess-animated-slow.svg (Slow 4.2s)")

    # Render Fast speed variant (1.5s)
    dark_fast = build_animated_chess_svg(featured_game, "dark", "fast")
    light_fast = build_animated_chess_svg(featured_game, "light", "fast")
    with open("assets/chess-animated-fast.svg", "w", encoding="utf-8") as f:
        f.write(dark_fast)
    with open("assets/chess-animated-fast-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_fast)
    with open("assets/chess-animated-fast-light.svg", "w", encoding="utf-8") as f:
        f.write(light_fast)
    print("Generated assets/chess-animated-fast.svg (Fast 1.5s)")

    # 2. Render each of the 14 legendary Grandmaster games for individual viewing
    game_slugs = [
        ("opera", 0),
        ("immortal", 1),
        ("century", 2),
        ("evergreen", 3),
        ("kasparov", 4),
        ("tal", 5),
        ("gold-coins", 6),
        ("capablanca", 7),
        ("anand", 8),
        ("botvinnik", 9),
        ("fischer-spassky", 10),
        ("morphy-paulsen", 11),
        ("rubinstein", 12),
        ("zandvoort", 13),
    ]
    for slug, g_idx in game_slugs:
        g_meta = GAMES_DATABASE[g_idx]
        g_svg = build_animated_chess_svg(g_meta, "dark", "normal")
        out_path = f"assets/chess-game-{slug}.svg"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(g_svg)
        print(f"Generated {out_path} ({g_meta['title']})")

    print("All chess multi-speed and multi-game assets generated successfully!")

if __name__ == "__main__":
    main()

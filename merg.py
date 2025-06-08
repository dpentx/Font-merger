import argparse
from fontTools.ttLib import TTFont

def merge_fonts(text_font_path, emoji_font_path, output_path):
    print(f"Merging fonts:\n- Text Font: {text_font_path}\n- Emoji Font: {emoji_font_path}\n- Output: {output_path}")
    
    text_font = TTFont(text_font_path)
    emoji_font = TTFont(emoji_font_path)

    allowed_glyphs = set(text_font.getGlyphOrder())

    # Merge CBDT
    if 'CBDT' in emoji_font:
        print(f" - Merging table: CBDT (safe mode)")
        text_font['CBDT'] = emoji_font['CBDT']

    # Merge CBLC güvenli şekilde
    if 'CBLC' in emoji_font:
        print(f" - Merging table: CBLC (safe mode)")
        emoji_cblc = emoji_font['CBLC']
        new_cblc = emoji_cblc.__class__()
        new_cblc.version = emoji_cblc.version
        new_cblc.strikes = []

        for strike in emoji_cblc.strikes:
            try:
                # Bazı glifleri at
                valid_subtables = []
                for sub in strike.indexSubTables:
                    if hasattr(sub, 'glyphArray'):
                        sub.glyphArray = [g for g in sub.glyphArray if g in allowed_glyphs]
                        if sub.glyphArray:
                            valid_subtables.append(sub)
                    elif hasattr(sub, 'imageSize') and hasattr(sub, 'names'):
                        sub.names = [n for n in sub.names if n in allowed_glyphs]
                        if sub.names:
                            valid_subtables.append(sub)
                if valid_subtables:
                    strike.indexSubTables = valid_subtables
                    new_cblc.strikes.append(strike)
            except Exception as e:
                print(f" ⚠️ CBLC strike atlandı: {e}")

        text_font['CBLC'] = new_cblc
    else:
        print("⚠️ CBLC tablosu bulunamadı!")

    # Son olarak kaydet
    text_font.save(output_path)
    print("🎉 Font başarıyla birleştirildi!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge emoji font into text font (CBLC+CBDT safe)")
    parser.add_argument("--text", required=True, help="Text font path")
    parser.add_argument("--emoji", required=True, help="Emoji font path")
    parser.add_argument("--output", required=True, help="Output merged font path")
    args = parser.parse_args()

    merge_fonts(args.text, args.emoji, args.output)


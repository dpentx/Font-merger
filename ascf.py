from fontTools.ttLib import TTFont, newTable

def add_secf_table(font_path, output_path):
    font = TTFont(font_path)
    
    if "SECF" in font:
        print("Fontta zaten SECF tablosu var.")
    else:
        secf = newTable("SECF")
        # En basit haliyle boş ama var olması lazım
        secf.data = b"\x00\x00\x00\x00"  # minimal placeholder
        font["SECF"] = secf
        print("SECF tablosu eklendi.")
        
    font.save(output_path)
    print(f"Yeni font kaydedildi: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add_secf.py input.ttf output.ttf")
    else:
        add_secf_table(sys.argv[1], sys.argv[2])


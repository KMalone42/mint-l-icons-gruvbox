{ stdenv }:

stdenv.mkDerivation {
  pname = "mint-l-icons-gruvbox-dark";
  version = "1.0";

  src = ./.;

  installPhase = ''
    mkdir -p $out/share/icons
    # copy every Mint-L* theme dir
    for d in mint-l-icons-gruvbox-dark/Mint-L*; do
      [ -d "$d" ] || continue
      tname="$(basename "$d")"
      mkdir -p "$out/share/icons/$tname"
      cp -a "$d"/. "$out/share/icons/$tname/"
    done
  '';

  meta = {
    description = "Mint-L Gruvbox icon themes (multiple color variants)";
    license = stdenv.lib.licenses.gpl3Plus;
    platforms = stdenv.lib.platforms.linux;
  };
}


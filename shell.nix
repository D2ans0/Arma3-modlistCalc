with import <nixpkgs> {};

let
  pinned_hash = "f70001bf2db0d2f8b8072282685a0df2f5660ed7";
  pinned_version = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/${pinned_hash}.tar.gz") { };
in
pkgs.mkShell {
  buildInputs = with pinned_version; [
    python312
    python312Packages.beautifulsoup4
    python312Packages.requests
    python312Packages.grequests
 ];
}

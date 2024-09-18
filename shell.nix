# Consider using mach-nix to generate these in the future: https://github.com/DavHau/mach-nix
# An example: https://discourse.nixos.org/t/how-to-convert-a-python-requirements-txt-file-into-a-nix-script/12426/2
let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (python-pkgs: [
      python-pkgs.pandas
      python-pkgs.streamlit
      python-pkgs.pyyaml
    ]))
  ];
}

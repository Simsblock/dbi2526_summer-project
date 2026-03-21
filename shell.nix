{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311                
    pkgs.python311Packages.pip    
  ];

  shellHook = ''
    echo "--- Python environment loaded ---"
    python --version
    pip --version
  '';
}
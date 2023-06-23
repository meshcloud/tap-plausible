{ pkgs ? import <nixpkgs> { } }:
let
  unstable = import <nixpkgs-unstable> { }; 
  my-python = pkgs.python310; 
  python-with-my-packages =
    my-python.withPackages (p: with p; [ tox ]);

in
pkgs.mkShell {
  NIX_SHELL = "tap-plausible";
  buildInputs = [
    pkgs.poetry
    python-with-my-packages
  ];
  shellHook = ''
    PYTHONPATH=${python-with-my-packages}/${python-with-my-packages.sitePackages}

    echo "Welcome to tap-plausible"
  '';
}

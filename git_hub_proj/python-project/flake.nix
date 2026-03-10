# nix develop 
# Env Managment using NixOS (Package Manager)
{
  description = "Python development setup with Nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }:
    {
      devShells.x86_64-linux =
      let
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in
      {
        default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            python3Packages.matplotlib
            python3Packages.tkinter
            python3Packages.pyinstaller
          ];
        };
      };
    };
}

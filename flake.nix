{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-26.05";
    };
  };

  outputs =
    {
      nixpkgs,
      ...
    }:
    let
      system = "x86_64-linux";

      lib = nixpkgs.lib;
      pkgs = import nixpkgs {
        inherit system;
        config = {
          allowUnfreePredicate =
            pkg:
            builtins.elem (lib.getName pkg) [
              "vagrant"
            ];
        };
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        shellHook = ''
          ln -s $PWD/.config/pulumi $HOME/.pulumi || true
        '';

        packages = with pkgs; [
          uv
          nickel
          jq

          pulumi-bin
          talosctl
          kubectl
          kubernetes-helm
          kustomize
          cilium-cli

          just

          vagrant
          swtpm
          rubocop
          wlvncc
        ];
      };
    };
}

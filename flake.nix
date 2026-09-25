{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
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
        packages = with pkgs; [
          pulumi
          uv
          nickel
          nls
          jq

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

{
  description = "Meetings summary, ,,, , ,";

  outputs = {
    self,
    nixpkgs-unstable,
  }: let
    lib = nixpkgs-unstable.lib;
    forAllSystems = genExpr: lib.genAttrs lib.systems.flakeExposed genExpr;
    nixpkgsFor = forAllSystems (system: import nixpkgs-unstable {inherit system;});
  in {
    formatter = forAllSystems (system: nixpkgsFor.${system}.alejandra);
    packages = forAllSystems (system: let
      pkgs = nixpkgsFor.${system};
    in {
      default = pkgs.callPackage ({
        stdenvNoCC,
        python3,
      }:
        stdenvNoCC.mkDerivation {
          name = "virgule";
          buildInputs = [(python3.withPackages (p: [p.faster-whisper]))];
        }) {};
    });
  };
}

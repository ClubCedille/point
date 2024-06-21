{
  description = "Meetings transcripts....";

  inputs.nixpkgs-unstable.url = "nixpkgs-unstable";

  outputs = {
    self,
    nixpkgs-unstable,
  }: let
    lib = nixpkgs-unstable.lib;
    forAllSystems = genExpr: lib.genAttrs lib.systems.flakeExposed genExpr;
    nixpkgsFor = forAllSystems (system: import nixpkgs-unstable {inherit system;});
    version = lib.substring 0 8 self.lastModifiedDate;
  in {
    formatter = forAllSystems (system: nixpkgsFor.${system}.alejandra);
    packages = forAllSystems (system: let
      pkgs = nixpkgsFor.${system};
      point = pkgs.callPackage ({
        stdenvNoCC,
        python3,
      }:
        stdenvNoCC.mkDerivation {
          name = "point";
          buildInputs = [(python3.withPackages (p: [p.faster-whisper p.flask]))];
        }) {};
    in {
      inherit point;
      default = point;
      point-docker = pkgs.dockerTools.buildLayeredImage {
        name = "point";
        tag = "latest";
        created = version;
        contents = [point];
        # TODO
        config = {
          # Cmd = ["${}"];
        };
      };
    });
  };
}

{ pkgs ? import <nixpkgs> {}}:
with pkgs;
mkShell {
  buildInputs = [
    google-cloud-sdk
    crane
    python310Packages.autopep8
    scorecard
  ];
}

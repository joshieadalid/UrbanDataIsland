[weewx@nixos:~]$ cat /etc/nixos/weewx.nix
# toolz.nix
{ lib
, buildPythonPackage
, fetchPypi
, setuptools
, wheel
}:

with import <nixpkgs> {};
#with pkgs.python312Packages;

buildPythonPackage rec {
  pname = "weewx";
  version = "5.1.0";
  format = "wheel";
  src = python312Packages.fetchPypi rec {
    inherit pname version format;
    sha256 = "13817ba9874c5c60a656a8e28cd1fbcd40b2a31eed262557bc58fc71f6bf15ef";
    dist = python;
    python = "py3";
  };
  propagatedBuildInputs = [
    python312Packages.configobj
    python312Packages.cheetah3
    python312Packages.pyserial
    python312Packages.paho-mqtt
    python312Packages.requests
    python312Packages.pyusb];
}
{ config, pkgs, ... }:
{
  systemd.services.weewxd = {
    enable = true;
    after = [ "network.target" ];
    wantedBy = [ "multi-user.target" ];

    description = "WeeWX Service";
    serviceConfig = {
      Type = "simple";
      ExecStart = "/run/current-system/sw/bin/weewxd --config /home/weewx/weewx-data/weewx.conf";
      Restart = "always";
      RestartSec = 5;
    };

    # Define el usuario si es necesario
#    user = "weewx";
#    group = "weewx";
  };
}
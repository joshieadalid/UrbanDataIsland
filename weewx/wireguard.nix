{ config, pkgs, lib, ... }:{
  networking.firewall.allowedUDPPorts = [51820];

  networking.wg-quick.interfaces = let
  publicKey = "JfnFFnXz+vBltwXmehAIlv7Sa9CdW8qs3SZb7EEXFxA=";
  in {
    wg0 = {
      listenPort = 51820;
      address = [ "10.100.0.6/24" ];
      dns = [ "192.168.10.51" ];
      privateKeyFile = "/root/wireguard-keys/privatekey";
      postUp = ["wg set wg0 peer ${publicKey} persistent-keepalive 1"];

      peers = [{
        inherit publicKey;
#        presharedKey = "QQKHkNQ9NvqR79Yz3l76vNEznF5jVKlSmdRlKN2XeH8";
       presharedKeyFile = "/root/wireguard-keys/presharedkey";
        allowedIPs = [ "0.0.0.0/0" "::/0" ];
        endpoint = "148.204.58.178:51820";
      }];
    };
  };
}
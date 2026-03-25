# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do | config|
  config.vm.box = "debian/bullseye64"
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "private_network", ip: "192.168.56.9"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
  SHELL

end

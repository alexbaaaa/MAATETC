# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/bullseye64"
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"

  # Flask dev server (flask run) and Nginx
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "private_network", ip: "192.168.56.9"

  # Full production-like stack: Nginx -> Gunicorn (systemd) -> Flask
  config.vm.provision "shell", path: "files/conf/deploy.sh", args: ["/vagrant"]
end

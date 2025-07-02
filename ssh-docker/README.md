# Install SSH
```shell
docker run -d -it --name dev-ssh -p 2220:20 -p 2221:21 -p 2222:22 --gpus=all --mount type=bind,source="$(pwd)",target=/test/ ubuntu:22.04

apt update && apt install -y openssh-server
mkdir /var/run/sshd
```

# SSH with Public Key Only (No Password)
```shell
docker exec -it dev-ssh bash
# enable public key authentication
sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^PubkeyAuthentication no/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# disable password authentication
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# set priviliage for 'root'
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin without-password/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin yes/PermitRootLogin without-password/' /etc/ssh/sshd_config

# start SSH service
service ssh status
service ssh restart
/usr/sbin/sshd

# set authroized keys
cd ~ && mkdir .ssh
vim .ssh/authorized_keys
```
# Public Key + Password (Both Allowed)
```shell
docker exec -it dev-ssh bash
# set password for 'root'
passwd root # xxx@xxx
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# start SSH service
/usr/sbin/sshd
```
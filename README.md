# pymongotut
A PyMongo tutorial with MongoDB running on a Raspberry Pi 2

Raspberry Pi 2 Setup:

1. Enable Static IP
2. Enable SSH from raspi-config tool
3. Update and upgrade
    * sudo apt-get update
    * sudo apt-get upgrade

For installing MongoDB on a Raspberry Pi 2, we need to use a special port available on Github (thanks to skrabban):

[skrabban/mongo-nonx86](https://github.com/skrabban/mongo-nonx86)

To install MongoDB on the Rapberry Pi 2, follow the instruction by Hardware Hacks :

[Raspberry Pi MongoDB Installation - The working guide!](http://c-mobberley.com/wordpress/2013/10/14/raspberry-pi-mongodb-installation-the-working-guide/)
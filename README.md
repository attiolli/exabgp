Exabgp config example that monitors two local service IPs (binded to loopback) and based on reply, announces/withdraws them via BGP. A convenient way to add more resilence for eg. an anycasted DNS service that needs to be highly available. Another usecase would be to help migrating a service between two datacenters. This can be done by building another server with identical service & same loopback ip and starting to announcing the IP with BGP. Then when you want to migrate, just withdraw the route from the first server.

<img width="962" alt="image" src="https://github.com/attiolli/exabgp/assets/5729471/89e5d000-75b4-4fcd-a52e-36c56a59dde3">


Because Exabgp has been coded with python and therefore relays on the libraries of the host system, a containerized installation seems a bit more reliable way to go.

Some notes when using this:

* When building from exabgp repo Dockerfile the default user seems to be "exa" and uid 999. Be sure to adjust exabgp dir file permissions according to this on the host machine.

* Also create a "log" directory under the exabgp dir on the host and verify that the "exa" user can write to it.

* After building the docker image, run like this for eg. : ```docker run --restart unless-stopped -e TZ=Europe/Helsinki -d --network host -v /etc/exabgp:/etc/exabgp --name exabgp -it exabgp -v /etc/exabgp/exabgp.conf```

* Tested with Edgerouter ER-X and seems to work as expected

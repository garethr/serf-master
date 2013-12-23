# Serf Master

[Serf](http://www.serfdom.io/) is a very nice service discovery and
orchestration framework which allows you to write scripts to react to
different events across your infrastructure. However most of the
examples are simple shell scripts with lots of logic embedded in them.
Combine that with per host configuration around registering event
handlers and it's easy to build a fiddly, hard to reason about
enviroment. It doesn't have to be that way.

Serf is the framework, what you built on top of it matters. I wanted
something with the following properties:

* Testable. I should be able to unit test the entire configuration.
* Single package. All hosts should get the same code, with the code
  deciding what runs where.
* Single event handler. I'd rather deal with logic about user events or
  roles within my code, rather than parameters to serf.


Serf Master tries to do this, presented as a very small Python framework
with no dependencies. Here's an example:

## An example

Imagine a cluster with a number of database servers and web servers. The
database servers have the Serf role of `db` and the web servers the Serf
role of `web`. We want the web servers to react whenever a new server is
added to the cluster (maybe to tell a load balancer to reload?) and we
want to be able to trigger a deploy. For the database servers we want to
be able to trigger a backup custom event.


    from serf_handler import SerfHandler, SerfHandlerProxy

    class WedHandler(SerfHandler):
        def deploy(self):
          # run commands here to do with deployment

        def member_join(self):
          # maybe rebalance the load balancer
    

    class DatabaseHandler(SerfHandler):
        def backup(self):
          # run commands here to do with backups


    if __name__ == '__main__':
        handler = SerfHandlerProxy()
        handler.register('web', WebHandler())
        handler.register('db', DatabaseHandler())
        handler.run()


The important parts are:

    handler.register('web', WebHandler())

This says if the Serf role is `web` then use the `WebHandler` class for
any events.

    def member_join(self):

This says for the `member-join` serf event we should execute the code
we write here.

See the unit tests for examples of now this can be tested.


## Installation

Serf Master is available on
[PyPi](https://pypi.python.org/pypi/serf_master) and can be installed
with:

    pip install serf_master

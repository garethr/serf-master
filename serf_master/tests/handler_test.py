#!/usr/bin/env python

import os

from mock import MagicMock

from serf_master import SerfHandler, SerfHandlerProxy


class TestSerfHandler:
    def setup(self):
        os.environ = {
            'SERF_SELF_NAME': 'local',
            'SERF_SELF_ROLE': 'web',
            'SERF_EVENT': 'member-join',
            'SERF_USER_EVENT': 'deploy',
            'SERF_QUERY_NAME': 'question',
        }
        self.load_handler()

    def load_handler(self):
        self.handler = SerfHandler()

    def test_name_set_from_env(self):
        assert self.handler.name == 'local'

    def test_role_set_from_env(self):
        assert self.handler.role == 'web'

    def test_event_set_from_env(self):
        assert self.handler.event == 'member_join'

    def test_custom_event(self):
        os.environ['SERF_EVENT'] = 'user'
        self.load_handler()
        assert self.handler.event == 'deploy'

    def test_query(self):
        os.environ['SERF_EVENT'] = 'query'
        self.load_handler()
        assert self.handler.event == 'question'




class TestSerfHandlerTags:

    def setup(self):
        os.environ = {
            'SERF_SELF_NAME': 'null',
            'SERF_TAG_ROLE': 'bob',
            'SERF_EVENT': 'null',
        }
        self.handler = SerfHandlerProxy()
        self.handler.log = MagicMock(return_value=True)
        assert len(self.handler.handlers) == 0

    def test_role_set_from_env(self):
        assert self.handler.role == 'bob'


class TestSerfHandlerRoleOverloading:

    def setup(self):
        os.environ = {
            'SERF_SELF_NAME': 'null',
            'SERF_SELF_ROLE': 'jim',
            'SERF_TAG_ROLE': 'bob',
            'SERF_EVENT': 'null',
        }
        self.handler = SerfHandlerProxy()
        self.handler.log = MagicMock(return_value=True)
        assert len(self.handler.handlers) == 0

    def test_role_set_from_env(self):
        assert self.handler.role == 'bob'


class TestSerfHandlerNegativeCases:

    def setup(self):
        os.environ = {
            'SERF_SELF_NAME': 'null',
            'SERF_SELF_ROLE': 'null',
            'SERF_EVENT': 'member-join',
        }
        self.handler = SerfHandlerProxy()
        self.handler.log = MagicMock(return_value=True)
        assert len(self.handler.handlers) == 0

    def test_no_handler(self):
        self.handler.run()
        self.handler.log.assert_called_with("no handler for role")

    def test_no_method_implemented(self):
        self.handler.register('default', SerfHandler())
        assert len(self.handler.handlers) == 1
        self.handler.run()
        self.handler.log.assert_called_with("event not implemented by class")


class TestSerfHandlerProxyCustomEvent:

    def test_method_implemented(self):
        os.environ = {
            'SERF_SELF_NAME': 'null',
            'SERF_SELF_ROLE': 'null',
            'SERF_EVENT': 'user',
            'SERF_USER_EVENT': 'implemented',
        }
        handler = SerfHandlerProxy()
        sample = SerfHandler()
        sample.implemented = MagicMock(return_value=True)
        assert len(handler.handlers) == 0
        handler.register('default', sample)
        assert len(handler.handlers) == 1
        handler.run()
        sample.implemented.assert_called_with()


class TestSerfHandlerProxyStandardEvent:
    def setup(self):
        os.environ = {
            'SERF_SELF_NAME': 'null',
            'SERF_SELF_ROLE': 'web',
            'SERF_EVENT': 'member-join',
        }
        self.handler = SerfHandlerProxy()
        self.sample = SerfHandler()
        self.sample.member_join = MagicMock(return_value=True)

    def test_standard_events_called(self):
        self.handler.register('default', self.sample)
        assert len(self.handler.handlers) == 1
        assert 'default' in self.handler.handlers
        self.handler.run()
        self.sample.member_join.assert_called_with()

    def test_role_registration(self):
        self.handler.register('web', self.sample)
        assert len(self.handler.handlers) == 1
        assert 'web' in self.handler.handlers
        self.handler.run()
        self.sample.member_join.assert_called_with()

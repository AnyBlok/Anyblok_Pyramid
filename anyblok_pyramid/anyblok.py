# -*- coding: utf-8 -*-
# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from zope.sqlalchemy import ZopeTransactionExtension
from zope.sqlalchemy.datamanager import (
    _SESSION_STATE, STATUS_ACTIVE, STATUS_READONLY, STATUS_CHANGED,
    STATUS_INVALIDATED, NO_SAVEPOINT_SUPPORT, _retryable_errors)
import transaction as zope_transaction
from transaction._transaction import Status as ZopeStatus


from zope.interface import implementer
from transaction.interfaces import IDataManagerSavepoint
from anyblok.environment import EnvironmentManager
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.exc import ConcurrentModificationError
from sqlalchemy.exc import DBAPIError


class AnyBlokSessionDataManager:

    def __init__(self, session, status, transaction_manager,
                 keep_session=False):
        self.transaction_manager = transaction_manager
        self.registry = session._query_cls.registry
        self.transaction = self.registry.session.transaction
        transaction_manager.get().join(self)
        _SESSION_STATE[id(session)] = status
        self.state = 'init'
        self.keep_session = keep_session

    def _finish(self, final_state):
        assert self.transaction is not None
        del _SESSION_STATE[id(self.registry.session)]
        registry = self.registry
        self.transaction = self.registry = None
        self.state = final_state
        if not self.keep_session:
            registry.session.close()
        else:
            registry.session.expire_all()

        EnvironmentManager.set('_precommit_hook', [])

    def abort(self, trans):
        if self.transaction is not None:
            self._finish('aborted')

    def tpc_begin(self, trans):
        self.registry.session.flush()

    def commit(self, trans):
        status = _SESSION_STATE[id(self.registry.session)]
        if status is not STATUS_INVALIDATED:
            if self.registry.session.expire_on_commit:
                self.registry.session.expire_all()
            self._finish('no work')

    def tpc_vote(self, trans):
        if self.transaction is not None:
            self.registry.commit()
            self._finish('committed')

    def tpc_finish(self, trans):
        pass

    def tpc_abort(self, trans):
        assert self.state is not 'committed'

    def sortKey(self):
        return "~AnyBlok:%d" % id(self.transaction)

    @property
    def savepoint(self):
        if set(engine.url.drivername
               for engine in self.transaction._connections.keys()
               if isinstance(engine, Engine)
               ).intersection(NO_SAVEPOINT_SUPPORT):
            raise AttributeError('savepoint')
        return self._savepoint

    def _savepoint(self):
        return AnyBlokSessionSavepoint(self.registry)

    def should_retry(self, error):
        if isinstance(error, ConcurrentModificationError):
            return True
        if isinstance(error, DBAPIError):
            orig = error.orig
            for error_type, test in _retryable_errors:
                if isinstance(orig, error_type):
                    if test is None:
                        return True
                    if test(orig):
                        return True


class AnyBlokTwoPhaseSessionDataManager(AnyBlokSessionDataManager):

    def tpc_vote(self, trans):
        if self.transaction is not None:
            self.transaction.prepare()
            self.state = 'voted'

    def tpc_finish(self, trans):
        if self.transaction is not None:
            self.registry.commit()
            self._finish('committed')

    def tpc_abort(self, trans):
        if self.transaction is not None:
            self.registry.rollback()
            self._finish('aborted commit')

    def sortKey(self):
        # Sort normally
        return "AnyBlok.twophase:%d" % id(self.transaction)


@implementer(IDataManagerSavepoint)
class AnyBlokSessionSavepoint:

    def __init__(self, registry):
        self.registry = registry
        self.transaction = self.registry.session.begin_nested()

    def rollback(self):
        self.transaction.rollback()


def join_transaction(session, initial_state=STATUS_ACTIVE,
                     transaction_manager=zope_transaction.manager,
                     keep_session=False):
    if _SESSION_STATE.get(id(session), None) is None:
        if session.twophase:
            DataManager = AnyBlokTwoPhaseSessionDataManager
        else:
            DataManager = AnyBlokSessionDataManager
        DataManager(session, initial_state, transaction_manager,
                    keep_session=keep_session)


def mark_changed(session, transaction_manager=zope_transaction.manager,
                 keep_session=False):
    session_id = id(session)
    assert _SESSION_STATE.get(session_id, None) is not STATUS_READONLY, (
        "Session already registered as read only")
    join_transaction(session, STATUS_CHANGED, transaction_manager, keep_session)
    _SESSION_STATE[session_id] = STATUS_CHANGED


class AnyBlokZopeTransactionExtension(ZopeTransactionExtension):

    def after_begin(self, session, transaction, connection):
        join_transaction(session, self.initial_state, self.transaction_manager,
                         self.keep_session)

    def after_attach(self, session, instance):
        join_transaction(session, self.initial_state, self.transaction_manager,
                         self.keep_session)

    def after_flush(self, session, flush_context):
        mark_changed(session, self.transaction_manager, self.keep_session)

    def after_bulk_update(self, session, query, query_context, result):
        mark_changed(session, self.transaction_manager, self.keep_session)

    def after_bulk_delete(self, session, query, query_context, result):
        mark_changed(session, self.transaction_manager, self.keep_session)

    def before_commit(self, session):
        assert (session.transaction.nested or  # noqa
                self.transaction_manager.get().status == ZopeStatus.COMMITTING,
                "Transaction must be committed using the transaction manager")

# -*- coding: utf-8 -*-
# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.environment import EnvironmentManager
from zope.sqlalchemy import ZopeTransactionExtension
from zope.sqlalchemy.datamanager import (
    SessionDataManager, TwoPhaseSessionDataManager, _SESSION_STATE,
    STATUS_ACTIVE, STATUS_READONLY, STATUS_CHANGED)
import transaction as zope_transaction
from transaction._transaction import Status as ZopeStatus


class AnyBlokMixinSessionDataManager:
    def _finish(self, final_state):
        super(AnyBlokMixinSessionDataManager, self)._finish(final_state)
        EnvironmentManager.set('_precommit_hook', [])


class AnyBlokSessionDataManager(AnyBlokMixinSessionDataManager,
                                SessionDataManager):
    def tpc_vote(self, trans):
        if self.tx is not None:  # there may have been no work to do
            # FIXME replace by anyblok.registry.commit
            self.session._query_cls.registry.apply_precommit_hook()
            self.tx.commit()
            self._finish('committed')


class AnyBlokTwoPhaseSessionDataManager(AnyBlokMixinSessionDataManager,
                                        TwoPhaseSessionDataManager):
    pass


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
    assert (_SESSION_STATE.get(session_id, None) is not STATUS_READONLY,
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
        assert (session.transaction.nested or
                self.transaction_manager.get().status == ZopeStatus.COMMITTING,
                "Transaction must be committed using the transaction manager")

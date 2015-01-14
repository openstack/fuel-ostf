#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from contextlib import contextmanager
from sqlalchemy import create_engine, orm


LOG = logging.getLogger(__name__)


@contextmanager
def contexted_session(dbpath):
    '''Allows to handle session via context manager
    '''
    LOG.debug('Starting session with dbpath={0}'.format(dbpath))
    engine = create_engine(dbpath)
    session = orm.Session(bind=engine)
    try:
        LOG.debug('Before yielding session.')
        yield session
        session.commit()
    except Exception:
        LOG.exception('Raised error in contexted session.')
        session.rollback()
        raise
    finally:
        session.close()


def get_session(dbpath):
    """Returns SQLAlchemy scoped session for given DB configuration string."""
    engine = create_engine(dbpath)
    session = orm.scoped_session(orm.sessionmaker())
    session.configure(bind=engine)
    return session

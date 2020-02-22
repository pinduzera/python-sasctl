#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2019, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os

import pytest
import six


@pytest.fixture
def change_dir():
    """Change working directory for the duration of the test."""
    old_dir = os.path.abspath(os.curdir)

    def change(new_dir):
        os.chdir(new_dir)

    yield change
    os.chdir(old_dir)


def test_astore_model(session, cas_session, change_dir):
    """Ensure the astore_model.py example executes successfully."""

    # Mock up Session() to return the Betamax-recorded session
    def Session(*args, **kwargs):
        return session

    change_dir('examples')
    with open('astore_model.py') as f:
        # Remove Session import and set CAS session to Betamax-recorded CAS
        # session
        code = f.read().replace('from sasctl import Session', '')
        code = code.replace("s = swat.CAS('hostname', 5570, 'username', 'password')",
                            's = cas_session')
        # Exec the script.
        six.exec_(code)


def test_sklearn_model(session, change_dir):
    """Ensure the sklearn_model.py example executes successfully."""

    # Mock up Session() to return the Betamax-recorded session
    def Session(*args, **kwargs):
        return session

    change_dir('examples')
    with open('sklearn_model.py') as f:
        # Remove import of Session to ensure mock function will be used
        # instead.
        code = f.read().replace('from sasctl import Session, register_model',
                                'from sasctl import register_model')
        six.exec_(code)


def test_full_lifecycle(session, change_dir):
    """Ensure the sklearn_model.py example executes successfully."""

    pytest.skip("Fix/re-implement.  Performance upload creates unrecorded CAS "
                "session that can't be replayed.")

    # Mock up Session() to return the Betamax-recorded session
    def Session(*args, **kwargs):
        return session

    change_dir('examples')
    with open('full_lifecycle.py') as f:
        # Remove import of Session to ensure mock function will be used
        # instead.
        code = f.read().replace('from sasctl import Session', '')

        six.exec_(code)

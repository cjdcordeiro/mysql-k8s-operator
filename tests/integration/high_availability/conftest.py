#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

import pytest
from integration.high_availability.high_availability_helpers import (
    deploy_chaos_mesh,
    destroy_chaos_mesh,
    get_application_name,
)
from pytest_operator.plugin import OpsTest


@pytest.fixture()
async def continuous_writes(ops_test: OpsTest) -> None:
    """Starts continuous writes to the MySQL cluster for a test and clear the writes at the end."""
    application_name = await get_application_name(ops_test, "application")

    application_unit = ops_test.model.applications[application_name].units[0]

    clear_writes_action = await application_unit.run_action("clear-continuous-writes")
    await clear_writes_action.wait()

    start_writes_action = await application_unit.run_action("start-continuous-writes")
    await start_writes_action.wait()

    yield

    clear_writes_action = await application_unit.run_action("clear-continuous-writes")
    await clear_writes_action.wait()


@pytest.fixture()
async def chaos_mesh(ops_test: OpsTest) -> None:
    """Deploys choas mesh to the namespace and uninstalls it at the end."""
    deploy_chaos_mesh(ops_test.model.info.name)

    yield

    destroy_chaos_mesh(ops_test.model.info.name)

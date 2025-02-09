import random

import pytest
import pytest_asyncio
from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet

from tests.integration.helpers.helpers import int_to_uint256


@pytest_asyncio.fixture(scope="module")
async def datacopy(
    starknet: Starknet, blockhashes: dict, blockhash_registry: StarknetContract
):
    return await starknet.deploy(
        source="./tests/unit/src/kakarot/precompiles/test_datacopy.cairo",
        cairo_path=["src"],
        disable_hint_validation=True,
    )


@pytest.mark.asyncio
class TestDataCopy:
    @pytest.mark.parametrize(
        "calldata_len",
        [32],
        ids=["calldata_len32"],
    )
    async def test_datacopy(self, datacopy, calldata_len):
        random.seed(0)
        calldata = [random.randint(0, 255) for _ in range(calldata_len)]

        await datacopy.test__datacopy_impl(calldata=calldata).call()
        await datacopy.test__datacopy_via_staticcall().call()

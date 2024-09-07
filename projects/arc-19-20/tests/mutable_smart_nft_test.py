from collections.abc import Generator

import pytest
from algopy_testing import AlgopyTestContext, algopy_testing_context

from smart_contracts.mutable_smart_nft.contract import MutableSmartNft


@pytest.fixture()
def context() -> Generator[AlgopyTestContext, None, None]:
    with algopy_testing_context() as ctx:
        yield ctx
        ctx.reset()


def test_apply_for_nft(context: AlgopyTestContext) -> None:
    # Arrange
    name = context.any_string()
    counter = 0
    contract = MutableSmartNft()

    # contract.create_application("Ayushman", 0, [1059])
    # Act

    reserve_address_str = "KBLZ2XFVWSPEZRZXDRTRT6DUUNPIF52I3SGQZZO2SJ2DKK5EJMC4DNCZPE"
    reserve_address = AlgopyTestContext.any_account(self=context)

    url_template = "template-ipfs://{ipfscid:0:dag-pb:reserve:sha2-256}"

    metahash = str.encode(reserve_address_str)

    # output = contract.apply_for_nft(
    #     reserve_address=reserve_address,
    #     url_template=url_template,
    #     metadata_hash=metahash,
    #     asset_name="Ayushman",
    #     unit_name="ayush",
    # )

    # Assert
    # assert output == f"Hello, {dummy_input}"

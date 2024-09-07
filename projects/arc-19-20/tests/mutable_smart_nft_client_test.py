import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.beta.account_manager import AddressAndSigner
from algokit_utils.beta.algorand_client import AlgorandClient, PayParams
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.mutable_smart_nft.mutable_smart_nft_client import (
    MutableSmartNftClient,
)


@pytest.fixture(scope="session")
def mutable_smart_nft_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> MutableSmartNftClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = MutableSmartNftClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.create_create_application(
        name="Ayushman", counter=1, criterias=[10, 59, 112]
    )

    # client.deploy(
    #     on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    #     on_update=algokit_utils.OnUpdate.AppendApp,
    # )
    return client


@pytest.fixture(scope="session")
def algorand() -> AlgorandClient:
    """Get an AlgorandClient to use throughout the tests"""
    return AlgorandClient.default_local_net()


@pytest.fixture(scope="session")
def dispenser(algorand: AlgorandClient) -> AddressAndSigner:
    """Get the dispenser to fund test addresses"""
    return algorand.account.dispenser()


@pytest.fixture(scope="session")
def creator(algorand: AlgorandClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    acct = algorand.account.random()

    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=100_000_000)
    )

    return acct


def test_says_apply_for_nft(
    mutable_smart_nft_client: MutableSmartNftClient,
    algorand: AlgorandClient,
    creator: AddressAndSigner,
    dispenser: AddressAndSigner,
) -> None:

    algorand.send.payment(
        PayParams(
            sender=dispenser.address,
            receiver=mutable_smart_nft_client.app_address,
            amount=10_000_000,
        )
    )

    print(
        mutable_smart_nft_client.algod_client.account_info(
            mutable_smart_nft_client.app_address
        )
    )

    # assert mbr_pay_txn.fee == 1_000

    reserve_address_str = "KBLZ2XFVWSPEZRZXDRTRT6DUUNPIF52I3SGQZZO2SJ2DKK5EJMC4DNCZPE"
    reserve_address = algorand.account.random()

    url_template = "template-ipfs://{ipfscid:0:dag-pb:reserve:sha2-256}"

    metahash = str.encode(reserve_address_str)
    result = mutable_smart_nft_client.apply_for_nft(
        reserve_address=reserve_address_str,
        url_template=url_template,
        metadata_hash=metahash,
        asset_name="Ayushman1",
        unit_name="ayush1",
    )

    # assert result.return_value == "Hello, World"


# def test_simulate_says_hello_with_correct_budget_consumed(
#     mutable_smart_nft_client: MutableSmartNftClient, algod_client: AlgodClient
# ) -> None:
#     result = (
#         mutable_smart_nft_client.compose()
#         .hello(name="World")
#         .hello(name="Jane")
#         .simulate()
#     )

#     assert result.abi_results[0].return_value == "Hello, World"
#     assert result.abi_results[1].return_value == "Hello, Jane"
#     assert result.simulate_response["txn-groups"][0]["app-budget-consumed"] < 100

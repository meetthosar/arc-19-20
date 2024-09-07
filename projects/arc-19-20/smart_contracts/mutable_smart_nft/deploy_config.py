import logging

import algokit_utils
import algokit_utils.beta
import algokit_utils.beta.account_manager
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.mutable_smart_nft.mutable_smart_nft_client import (
    MutableSmartNftClient,
)

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    pass

    app_client = MutableSmartNftClient(algod_client=algod_client, signer=deployer)

    criterias = [1, 2]

    response = app_client.create_create_application(
        name="Ayushman", counter=1, criterias=criterias
    )

    # print(response.get("address"))

    # application = algod_client.application_info(application_id=application_id)

    # print(application)

    # txn = algosdk.transaction.PaymentTxn(sender=deployer, receiver=response.address)
    # algod_client.send_transaction(txn)

    reserve_address_str = "KBLZ2XFVWSPEZRZXDRTRT6DUUNPIF52I3SGQZZO2SJ2DKK5EJMC4DNCZPE"

    url_template = "template-ipfs://{ipfscid:0:dag-pb:reserve:sha2-256}"

    metahash = str.encode(reserve_address_str)

    # app_client.apply_for_nft(
    #     reserve_address=reserve_address_str,
    #     url_template=url_template,
    #     asset_name="Ayushman",
    #     unit_name="ayush",
    #     metadata_hash=metahash,
    # )

    # app_client.deploy(
    #     on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    #     on_update=algokit_utils.OnUpdate.AppendApp,
    # )
    # name = "world"
    # response = app_client.hello(name=name)
    # logger.info(
    #     f"Called hello on {app_spec.contract.name} ({app_client.app_id}) "
    #     f"with name={name}, received: {response.return_value}"
    # )

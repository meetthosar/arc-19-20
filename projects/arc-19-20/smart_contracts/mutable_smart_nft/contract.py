from algopy import (
    Account,
    ARC4Contract,
    Asset,
    Bytes,
    Global,
    String,
    Txn,
    UInt64,
    gtxn,
    itxn,
    op,
    subroutine,
)
from algopy.arc4 import DynamicArray, UInt32, abimethod
from algopy.arc4 import UInt64 as ARC4UInt64


class ARC20Contract(ARC4Contract):
    @subroutine
    def asset_create(
        self,
        total: UInt64,
        decimals: UInt32,
        default_frozen: bool,
        unit_name: String,
        name: String,
        url: String,
        metadata_hash: Bytes,
        manager_addr: Account,
        reserve_addr: Account,
        freeze_addr: Account,
        clawback_addr: Account,
    ) -> Asset:
        asset = (
            itxn.AssetConfig(
                unit_name=unit_name,
                asset_name=name,
                total=total,
                manager=manager_addr,
                freeze=freeze_addr,
                reserve=reserve_addr,
                clawback=clawback_addr,
                url=url,
                default_frozen=default_frozen,
                fee=Global.min_txn_fee,
            )
            .submit()
            .created_asset
        )

        return asset

    @subroutine
    def asset_config(
        self,
        config_asset: Asset,
        total: UInt64,
        decimals: UInt32,
        default_frozen: bool,
        unit_name: String,
        name: String,
        url: String,
        metadata_hash: Bytes,
        manager_addr: Account,
        reserve_addr: Account,
        freeze_addr: Account,
        clawback_addr: Account,
    ) -> None:

        assert self.is_application_a_asset_creator(config_asset)

        itxn.AssetConfig(
            config_asset=config_asset,
            manager=manager_addr,
            freeze=freeze_addr,
            reserve=reserve_addr,
            clawback=clawback_addr,
        ).submit()

    @subroutine
    def get_asset_config(self, asset: Asset) -> Asset:
        assert self.is_application_a_asset_creator(asset=asset)
        return asset

    @subroutine
    def asset_transfer(
        self,
        xfer_asset: Asset,
        asset_amount: UInt64,
        asset_sender: Account,
        asset_receiver: Account,
    ) -> None:
        assert self.is_application_a_asset_creator(asset=xfer_asset)
        itxn.AssetTransfer(
            xfer_asset=xfer_asset,
            asset_amount=asset_amount,
            asset_sender=asset_sender,
            asset_receiver=asset_receiver,
        ).submit()

    @subroutine
    def asset_freeze(self, freeze_asset: Asset, asset_frozen: bool) -> None:
        assert self.is_application_a_asset_creator(asset=freeze_asset)

        itxn.AssetConfig(
            config_asset=freeze_asset, default_frozen=asset_frozen
        ).submit()

    @subroutine
    def get_asset_is_frozen(self, freeze_asset: Asset) -> bool:
        assert self.is_application_a_asset_creator(asset=freeze_asset)
        return True

    @subroutine
    def get_account_is_frozen(
        self, freeze_asset: Asset, freeze_account: Account
    ) -> bool:
        assert self.is_application_a_asset_creator(asset=freeze_asset)
        return True

    @subroutine
    def asset_destroy(self, destroy_asset: Asset) -> None:
        assert self.is_application_a_asset_creator(asset=destroy_asset)
        # Asset Destroy

    @subroutine
    def get_circulating_supply(self, asset: Asset) -> UInt64:
        return UInt64(1)

    @subroutine
    def is_application_a_asset_creator(self, asset: Asset) -> bool:
        [creator, flag] = op.AssetParamsGet.asset_creator(asset)
        return creator == Global.current_application_address


class MutableSmartNft(ARC20Contract):
    counter: UInt64
    name: String
    criterias: DynamicArray[ARC4UInt64]

    @abimethod(allow_actions=["NoOp"], create="require")
    def create_application(
        self,
        name: String,
        counter: UInt64,
        criterias: DynamicArray[ARC4UInt64],
    ) -> None:
        self.counter = counter
        self.name = name
        self.criterias = criterias.copy()

    @abimethod()
    def create_yojana_token(
        self,
        reserve_address: Account,
        url_template: String,
        asset_name: String,
        unit_name: String,
        metadata_hash: Bytes,
        mbr_pay: gtxn.PaymentTransaction,
    ) -> None:
        assert Txn.sender == mbr_pay.sender
        assert mbr_pay.receiver == Global.current_application_address
        assert self.criterias.length != 0, "Length should not be zero"
        assert self.are_criteria_matching(
            criterias=self.criterias, applicant=Txn.sender
        ), "One the criteria token balance is zero"

        # apps_created = Global.current_application_address.total_assets_created + 1
        # unit_name = unit_name + String.
        token = self.asset_create(
            total=UInt64(1),
            decimals=UInt32(0),
            default_frozen=True,
            unit_name=unit_name,
            name=asset_name,
            url=url_template,
            metadata_hash=metadata_hash,
            manager_addr=Global.current_application_address,
            reserve_addr=reserve_address,
            freeze_addr=Global.current_application_address,
            clawback_addr=Global.current_application_address,
        )

        # self.opt_in_asset(token=token, applicant=applicant)

    @subroutine
    def are_criteria_matching(
        self, criterias: DynamicArray[ARC4UInt64], applicant: Account
    ) -> bool:
        matches_all_criteria = True
        for criteria in criterias:
            [balance, flag] = op.AssetHoldingGet.asset_balance(
                applicant, criteria.native
            )
            if balance == 0:
                return False
        return matches_all_criteria

    @abimethod
    def get_yojana_token(self, mbr_pay: gtxn.PaymentTransaction, token: UInt64) -> None:
        assert mbr_pay.sender == Txn.sender
        assert Txn.sender.is_opted_in(Asset(token))

        self.asset_transfer(
            xfer_asset=Asset(token),
            asset_amount=UInt64(1),
            asset_sender=Global.current_application_address,
            asset_receiver=Txn.sender,
        )

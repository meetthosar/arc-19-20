from algopy import (
    ARC4Contract,
)


class ARC20Contract(ARC4Contract):
    def asser_create(self) -> bool:
        return True

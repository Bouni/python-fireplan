import logging
from fireplan import Fireplan

logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)8s | %(module)20s %(funcName)20s | %(message)s",
)

fp = Fireplan("kQOGjw0SaYC4oLXqmp44ycC664L0ttVbb9c7Ee9Pa3D")
fp.register("Fail")
fp.get_calendar()

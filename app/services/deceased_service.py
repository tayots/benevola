from app.exceptions.deceased import *
from app import db
from app.home.models import Deceased
import logging

log = logging.getLogger(__name__)


def delete_deceased(deceased_id):
    # Prepare Data
    deceased = Deceased.query.get(deceased_id)

    if deceased is None:
        raise DeceasedNotFoundError("Deceased id={0} not found".format(deceased_id))

    db.session.delete(deceased)

    db.session.commit()

    return True

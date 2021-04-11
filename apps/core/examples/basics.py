from datetime import date
from typing import List

from django.db import connection, transaction
from django.db.models import Count, Q
from django.db.models.functions import Length

from apps.core.models import Member, Party


def select_all() -> List[Member]:
    """
    Select all users in table members using model Member
    :return:
    """
    pass


def select_one() -> Member:
    """
    Return exactly one member (if possible) with surname `Poliačik`
    :return:
    """
    pass


def select_first() -> Member:
    """
    Select first record from table parties
    :return:
    """
    pass


def select_youngest() -> Member:
    """
    Select the youngest member of parliament ever
    :return:
    """
    pass


def create_party() -> Party:
    """
    Create party with name: `Friends of Douglas Adams`
    :return:
    """
    pass


def party_exists() -> bool:
    """
    Is there a party with name `Združenie robotníkov Slovenska`?
    :return:
    """
    pass


def longest_party_name() -> str:
    pass


def most_experienced_member() -> Member:
    pass


def communists_or_socialists() -> List[Party]:
    """
    Select all parties where type is SOCIALISTS or LIBERAL
    :return:
    """
    pass


def communists_or_socialists_with_robo() -> List[Party]:
    pass


def best_tourist() -> Member:
    pass


def party_type_for_mazurek() -> str:
    pass


def disco_members() -> List[Member]:
    pass


def select_raw() -> List[dict]:
    query = "SELECT * FROM parties;"

    with connection.cursor() as cursor:
        cursor.execute(str(query))
        columns = [col[0] for col in cursor.description]
        response = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return response


def cleansing():
    with transaction.atomic():
        Member.objects.filter(government_members__party__type=Party.PartyEnum.NAZI).delete()

        raise Exception("We are better than them")

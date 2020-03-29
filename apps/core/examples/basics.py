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

    members = Member.objects.all()
    return members


def select_one() -> Member:
    """
    Return exactly one member (if possible) with surname `Poliačik`
    :return:
    """
    member = Member.objects.get(
        surname="Poliačik"
    )

    return member


def select_first() -> Member:
    """
    Select first record from table parties
    :return:
    """
    party = Party.objects.first()
    return party


def select_youngest() -> Member:
    """
    Select the youngest member of parliament ever
    :return:
    """
    member = Member.objects.order_by('-born_at').first()
    return member


def create_party() -> Party:
    """
    Create party with name: `Friends of Douglas Adams`
    :return:
    """
    party = Party.objects.create(
        name='Friends of Douglas Adams',
        color='darkblue'
    )

    return party


def party_exists() -> bool:
    """
    Is there a party with name `Združenie robotníkov Slovenska`?
    :return:
    """
    return Party.objects.filter(name='Združenie robotníkov Slovenska').exists()


def longest_party_name() -> str:
    party_name = Party.objects.annotate(
        name_length=Length('name')
    ).order_by('-name_length').first().name

    return party_name


def most_experienced_member() -> Member:
    member = Member.objects.annotate(
        experience=Count('government_members__id')
    ).order_by('-experience').first()

    return member


def communists_or_socialists() -> List[Party]:
    """
    Select all parties where type is SOCIALISTS or LIBERAL
    :return:
    """
    parties = Party.objects.filter(
        type__in=[Party.PartyEnum.SOCIALISTS, Party.PartyEnum.COMMUNIST]
    )

    parties = Party.objects.filter(
        Q(type=Party.PartyEnum.SOCIALISTS) | Q(type=Party.PartyEnum.COMMUNIST)
    )

    return parties


def communists_or_socialists_with_robo() -> List[Party]:
    parties = Party.objects.filter(
        (Q(type=Party.PartyEnum.SOCIALISTS) | Q(type=Party.PartyEnum.COMMUNIST)) &
        Q(government_members__member__name='Robert')
    ).distinct('name')

    return parties


def best_tourist() -> Member:
    member = Member.objects.annotate(
        travels=Count('government_members__party_id', distinct=True)
    ).order_by('-travels').first()

    return member


def party_type_for_mazurek() -> str:
    return Party.objects.filter(
        government_members__member__name='Milan',
        government_members__member__surname='Mazurek').values_list('type', flat=True)[0]


def disco_members() -> List[Member]:
    return Member.objects.filter(
        born_at__gte=date(1960, 1, 1),
        born_at__lte=date(1969, 12, 31),
    )


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

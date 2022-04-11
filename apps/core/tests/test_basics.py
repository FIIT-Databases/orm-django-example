from datetime import date

from django.db import connection
from django.db.models import Q, Count
from django.test import TestCase, override_settings

from apps.core.examples import basics
from apps.core.models import Member, Party


class ORMTestCase(TestCase):
    fixtures = ['apps/core/fixtures/initial.json']

    @override_settings(DEBUG=True)
    def test_select_all(self):
        members = Member.objects.all()

        self.assertEqual(list(basics.select_all()), list(members))

    @override_settings(DEBUG=True)
    def test_select_one(self):
        member = Member.objects.get(
            surname="Poliačik"
        )

        self.assertEqual(basics.select_one(), member)

    @override_settings(DEBUG=True)
    def test_select_first(self):
        party = Party.objects.first()

        self.assertEqual(basics.select_first(), party)

    @override_settings(DEBUG=True)
    def test_select_youngest(self):
        member = Member.objects.order_by('-born_at').first()

        self.assertEqual(basics.select_youngest(), member)

    @override_settings(DEBUG=True)
    def test_create_party(self):
        basics.create_party()
        self.assertTrue(Party.objects.filter(name='Friends of Douglas Adams').exists())

    @override_settings(DEBUG=True)
    def test_longest_party_name(self):
        self.assertEqual(
            'Magyar Koalíció – Maďarská koalícia, Magyar Kereszténydemokrata Mozgalom – Maďarské kresťanskodemokra'
            'tické hnutie, Együttélés – Spolužitie, Magyar Polgári Párt – Maďarská občianska strana',
            basics.longest_party_name()
        )

    @override_settings(DEBUG=True)
    def test_most_experienced_member(self):
        self.assertEqual(
            Member.objects.get(name='Robert', surname='Fico'),
            basics.most_experienced_member()
        )

    @override_settings(DEBUG=True)
    def test_communists_or_socialists(self):
        self.assertEqual(
            list(Party.objects.filter(
                type__in=[Party.PartyEnum.SOCIALISTS, Party.PartyEnum.COMMUNIST]
            )),
            list(basics.communists_or_socialists())
        )

    @override_settings(DEBUG=True)
    def test_communists_or_socialists_with_robo(self):
        self.assertEqual(
            list(Party.objects.filter(
                (Q(type=Party.PartyEnum.SOCIALISTS) | Q(type=Party.PartyEnum.COMMUNIST))
                & Q(government_members__member__name='Robert')
            ).distinct('name')),
            list(basics.communists_or_socialists_with_robo())
        )

    @override_settings(DEBUG=True)
    def test_best_tourist(self):
        self.assertEqual(
            Member.objects.annotate(travels=Count('government_members__party_id', distinct=True)).order_by('-travels').first(),
            basics.best_tourist()
        )

    @override_settings(DEBUG=True)
    def test_party_type_for_mazurek(self):
        self.assertEqual(
            Party.PartyEnum.NAZI,
            Party.objects.filter(
                government_members__member__name='Milan',
                government_members__member__surname='Mazurek'
            ).values_list('type', flat=True)[0]
        )

    @override_settings(DEBUG=True)
    def test_disco_members(self):
        self.assertEqual(
            list(Member.objects.filter(
                born_at__gte=date(1960, 1, 1),
                born_at__lte=date(1969, 12, 31),
            )),
            list(basics.disco_members())
        )

    @override_settings(DEBUG=True)
    def test_select_raw(self):
        query = "SELECT * FROM parties;"

        with connection.cursor() as cursor:
            cursor.execute(str(query))
            columns = [col[0] for col in cursor.description]
            response = [dict(zip(columns, row)) for row in cursor.fetchall()]

        self.assertEqual(
            response,
            basics.select_raw()
        )

    @override_settings(DEBUG=True)
    def test_cleansing(self):
        with self.assertRaisesMessage(Exception, "We are better than them"):
            basics.cleansing()

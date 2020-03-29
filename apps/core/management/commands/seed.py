import json
from typing import Dict, List

from django.core.management import BaseCommand
import urllib.request

from django.utils.dateparse import parse_datetime
from django.utils.functional import cached_property

from apps.core.models import Member, Party, Government, GovernmentMember, Role


class Command(BaseCommand):

    @cached_property
    def default_role(self) -> Role:
        default_role, created = Role.objects.get_or_create(name='Poslanec')

        if created:
            self.stdout.write(f"Creating role: {default_role}")

        return default_role

    def handle(self, *args, **options):
        governments = self._download("https://www.nrsr.sk/opendata/1/sk/General/ParliamentaryTerms")

        for government in governments:
            self._process_term(government)

    def _download(self, url: str) -> List[Dict]:
        data = urllib.request.urlopen(url)
        return json.loads(data.read())

    def _process_term(self, data: Dict):
        government, created = Government.objects.get_or_create(
            started_at=parse_datetime(data['dateFrom']).date(),
            end_at=parse_datetime(data['dateTo']).date() if data.get('dateTo') else None,
        )

        if created:
            self.stdout.write(f"Creating government: {government}")

        members = self._download(f'https://www.nrsr.sk/opendata/1/sk/MP/MembersOfParliament?termNr={data["termNr"]}')

        for member in members:
            self._process_member(government, member)

    def _process_member(self, government: Government, data: Dict):
        member, created = Member.objects.get_or_create(
            name=data['firstname'],
            surname=data['lastName'],
            born_at=parse_datetime(data['birthDate']).date()
        )

        if created:
            self.stdout.write(f"Creating member: {member}")

        party, created = Party.objects.get_or_create(
            name=data['partyDepartmentName']
        )

        if created:
            self.stdout.write(f"Creating party: {party}")

        government_member, created = GovernmentMember.objects.get_or_create(
            government=government,
            party=party,
            member=member,
            role=self.default_role
        )

        if created:
            self.stdout.write(str(government_member))

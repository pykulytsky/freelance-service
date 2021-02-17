from typing import Iterable, Optional

from authentication.mailchimp.http import MailchimpHTTP
from authentication.mailchimp.member import MailchimpMember
from authentication.models import User


class AppMailchimp:
    def __init__(self):
        self.http = MailchimpHTTP()

    def subscribe_django_user(self, list_id: str, user: User, tags: Optional[Iterable] = None):
        member = MailchimpMember.from_django_user(user)
        self.mass_subscribe(
            list_id=list_id,
            members=[member],
        )

        if tags is not None:
            self.set_tags(
                list_id=list_id,
                member=member,
                tags=tags,
            )

    def mass_subscribe(self, list_id: str, members: Iterable[MailchimpMember]):

        member_list = list()
        for member in members:
            member_list.append({
                **member.to_mailchimp(),
                'status': 'subscribed',
            })

        return self.http.post(
            url=f'lists/{list_id}',
            payload={
                'members': member_list,
                'update_existing': True,
            },
        )

    def delete_list_member(self, list_id: str, user: User, tags: Optional[Iterable] = None):
        member = MailchimpMember.from_django_user(user)

        if tags is not None:
            self.set_tags(
                list_id=list_id,
                member=member,
                tags=tags,
            )

        return self.http.delete(
            url=f'lists/{list_id}/members/{member.subscriber_hash}',
        )

    def set_tags(self, list_id: str, member: MailchimpMember, tags: Iterable[str]):
        self.http.post(
            url=f'/lists/{list_id}/members/{member.subscriber_hash}/tags',
            payload={
                'tags': [{'name': tag, 'status': 'active'} for tag in tags],
            },
            expected_status_code=204,
        )


__all__ = [
    AppMailchimp,
]

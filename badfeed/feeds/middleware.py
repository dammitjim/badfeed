from django.db.models import Case, Count, IntegerField, Q, When

from badfeed.feeds.models import Feed


class FeedMenuMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.feed_menu = Feed.objects.watched_by(request.user).annotate(
                unread_items=Count(
                    Case(
                        When(
                            Q(
                                entries__states__isnull=False,
                                entries__states__user=request.user,
                            )
                        ),
                        then=0,
                        default=1,
                        output_field=IntegerField(),
                    )
                )
            )

        response = self.get_response(request)
        return response

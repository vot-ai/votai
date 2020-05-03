from celery import shared_task


@shared_task
def auto_deactivate(item_id: int) -> None:
    from .models import Item

    try:
        item: Item = Item.objects.get(id=item_id)
        item.deactivate()
    except Item.DoesNotExist:
        pass

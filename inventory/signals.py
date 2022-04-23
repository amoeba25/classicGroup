from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import RawInventory, UtilityInventory, FinishedInventory, TotalInventory


@receiver(post_save, sender=RawInventory)
def RawMerge(sender, instance, created, **kwargs):
    rawInventory = instance
    if created:
        TotalInventory.objects.create(
            select_branch=rawInventory.select_branch,
            category=rawInventory._meta.db_table,
            unique_name=rawInventory.slug,
            product_name=rawInventory.product_name,
            quantity=rawInventory.quantity,
            reserved_qt=rawInventory.reserved_qt,
            max_quantity=rawInventory.max_quantity,
            available_quantity=rawInventory.available_quantity,
            description=rawInventory.description
        )
        print("Raw Inventory Merged")


@receiver(post_save, sender=RawInventory)
def RawUpdate(sender, instance, **kwargs):
    rawData = instance
    TotalInventory.objects.filter(unique_name=rawData.slug).update(
        product_name=rawData.product_name,
        quantity=rawData.quantity,
        reserved_qt=rawData.reserved_qt,
        max_quantity=rawData.max_quantity,
        available_quantity=rawData.available_quantity,
        description=rawData.description
    )

@receiver(post_delete, sender=RawInventory)
def RawDelete(sender, instance, **kwargs):
    rawData = instance.slug
    TotalInventory.objects.filter(unique_name=rawData).delete()


@receiver(post_save, sender=UtilityInventory)
def UtilityMerge(sender, instance, created, **kwargs):
    utilityInventory = instance
    if created:
        TotalInventory.objects.create(
            select_branch=utilityInventory.select_branch,
            category=utilityInventory._meta.db_table,
            unique_name=utilityInventory.slug,
            product_name=utilityInventory.product_name,
            quantity=utilityInventory.quantity,
            reserved_qt=utilityInventory.reserved_qt,
            max_quantity=utilityInventory.max_quantity,
            available_quantity=utilityInventory.available_quantity,
            description=utilityInventory.description
        )
        print("Utility Inventory Merged")


@receiver(post_save, sender=UtilityInventory)
def UtilityUpdate(sender, instance, **kwargs):
    UtilityData = instance
    TotalInventory.objects.filter(unique_name=UtilityData.slug).update(
        product_name=UtilityData.product_name,
        quantity=UtilityData.quantity,
        reserved_qt=UtilityData.reserved_qt,
        max_quantity=UtilityData.max_quantity,
        available_quantity=UtilityData.available_quantity,
        description=UtilityData.description
    )

@receiver(post_delete, sender=UtilityInventory)
def UtilityDelete(sender, instance, **kwargs):
    utilityData = instance.slug
    TotalInventory.objects.filter(unique_name=utilityData).delete()


@receiver(post_save, sender=FinishedInventory)
def FinishedMerge(sender, instance, created, **kwargs):
    finishedInventory = instance
    if created:
        TotalInventory.objects.create(
            select_branch=finishedInventory.select_branch,
            category=finishedInventory._meta.db_table,
            unique_name=finishedInventory.slug,
            product_name=finishedInventory.product_name,
            quantity=finishedInventory.quantity,
            reserved_qt=finishedInventory.reserved_qt,
            max_quantity=finishedInventory.max_quantity,
            available_quantity=finishedInventory.available_quantity,
            description=finishedInventory.description
        )
        print("Finished Inventory Merged")


@receiver(post_save, sender=FinishedInventory)
def FinishedUpdate(sender, instance, **kwargs):
    FinishedData = instance
    TotalInventory.objects.filter(unique_name=FinishedData.slug).update(
        product_name=FinishedData.product_name,
        quantity=FinishedData.quantity,
        reserved_qt=FinishedData.reserved_qt,
        max_quantity=FinishedData.max_quantity,
        available_quantity=FinishedData.available_quantity,
        description=FinishedData.description
    )

@receiver(post_delete, sender=FinishedInventory)
def FinishedDelete(sender, instance, **kwargs):
    finishedData = instance.slug
    TotalInventory.objects.filter(unique_name=finishedData).delete()

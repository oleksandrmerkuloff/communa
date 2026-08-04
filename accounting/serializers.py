from django.db import transaction
from rest_framework import serializers

from .models import Category, Income, Expense, Budget, AccountingAttachment
from organization.serializers import OrganizationReaderSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id"]


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name",)


class AccountingAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingAttachment
        fields = ("id", "file", "created_at")
        read_only_fields = ["created_at"]


class BudgetWriterSerializer(serializers.ModelSerializer):
    attachments = AccountingAttachmentSerializer(many=True, required=False)

    class Meta:
        model = Budget
        fields = ("organization", "category", "planned_amount", "year", "month", "attachments")

    def create(self, validated_data):
        attachments_data = validated_data.pop("attachments", [])

        with transaction.atomic():
            budget = Budget.objects.create(**validated_data)

            for attachment_data in attachments_data:
                AccountingAttachment.objects.create(content_object=budget, **attachment_data)

        return budget

    def update(self, instance, validated_data):
        attachments_data = validated_data.pop("attachments", [])

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if attachments_data:
                existing_attachments = {att.id: att for att in instance.attachments.all()}
                keep_attachment_ids = []

                for attachment_item in attachments_data:
                    attachment_id = attachment_item.get("id")

                    if attachment_id in existing_attachments:
                        att_instance = existing_attachments[attachment_id]
                        for key, value in attachment_item.items():
                            if key == "id":
                                continue
                            setattr(att_instance, key, value)
                        att_instance.save()
                        keep_attachment_ids.append(att_instance.id)
                    else:
                        new_att = AccountingAttachment.objects.create(content_object=instance, **attachment_item)
                        keep_attachment_ids.append(new_att.id)

                for att_id, att_instance in existing_attachments.items():
                    if att_id not in keep_attachment_ids:
                        att_instance.delete()

        return instance


class BudgetReaderSerializer(serializers.ModelSerializer):
    attachments = AccountingAttachmentSerializer(many=True, read_only=True)
    organization = OrganizationReaderSerializer(read_only=True)
    category = CategoryShortSerializer(read_only=True)

    class Meta:
        model = Budget
        fields = "__all__"


class IncomeWriterSerializer(serializers.ModelSerializer):
    attachments = AccountingAttachmentSerializer(many=True, required=False)

    class Meta:
        model = Income
        fields = ("amount", "date", "description", "organization", "category", "attachments")

    def create(self, validated_data):
            attachments_data = validated_data.pop("attachments", [])
    
            with transaction.atomic():
                income = Income.objects.create(**validated_data)
    
                for attachment_data in attachments_data:
                    AccountingAttachment.objects.create(content_object=income, **attachment_data)
    
            return income
    
    def update(self, instance, validated_data):
        attachments_data = validated_data.pop("attachments", [])

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if attachments_data:
                existing_attachments = {att.id: att for att in instance.attachments.all()}
                keep_attachment_ids = []

                for attachment_item in attachments_data:
                    attachment_id = attachment_item.get("id")

                    if attachment_id in existing_attachments:
                        att_instance = existing_attachments[attachment_id]
                        for key, value in attachment_item.items():
                            if key == "id":
                                continue
                            setattr(att_instance, key, value)
                        att_instance.save()
                        keep_attachment_ids.append(att_instance.id)
                    else:
                        new_att = AccountingAttachment.objects.create(content_object=instance, **attachment_item)
                        keep_attachment_ids.append(new_att.id)

                for att_id, att_instance in existing_attachments.items():
                    if att_id not in keep_attachment_ids:
                        att_instance.delete()

        return instance
    

class IncomeReaderSerializer(serializers.ModelSerializer):
    attachments = AccountingAttachmentSerializer(many=True, read_only=True)
    organization = OrganizationReaderSerializer(read_only=True)
    category = CategoryShortSerializer(read_only=True)

    class Meta:
        model = Income
        fields = "__all__"


class ExpenseWriterSerializer(serializers.ModelSerializer):
    attachments = AccountingAttachmentSerializer(many=True, required=False)

    class Meta:
        model = Expense
        fields = ("amount", "date", "description", "organization", "category", "attachments")

    def create(self, validated_data):
            attachments_data = validated_data.pop("attachments", [])
    
            with transaction.atomic():
                expense = Expense.objects.create(**validated_data)
    
                for attachment_data in attachments_data:
                    AccountingAttachment.objects.create(content_object=expense, **attachment_data)
    
            return expense
    
    def update(self, instance, validated_data):
        attachments_data = validated_data.pop("attachments", [])

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if attachments_data:
                existing_attachments = {att.id: att for att in instance.attachments.all()}
                keep_attachment_ids = []

                for attachment_item in attachments_data:
                    attachment_id = attachment_item.get("id")

                    if attachment_id in existing_attachments:
                        att_instance = existing_attachments[attachment_id]
                        for key, value in attachment_item.items():
                            if key == "id":
                                continue
                            setattr(att_instance, key, value)
                        att_instance.save()
                        keep_attachment_ids.append(att_instance.id)
                    else:
                        new_att = AccountingAttachment.objects.create(content_object=instance, **attachment_item)
                        keep_attachment_ids.append(new_att.id)

                for att_id, att_instance in existing_attachments.items():
                    if att_id not in keep_attachment_ids:
                        att_instance.delete()

        return instance
    

class ExpenseReaderSerializer(serializers.ModelSerializer):
    attachments = AccountingAttachmentSerializer(many=True, read_only=True)
    organization = OrganizationReaderSerializer(read_only=True)
    category = CategoryShortSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"


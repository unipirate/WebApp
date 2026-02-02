from rest_framework import serializers
import os
from .models import FileDocument

class UpLoadFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        required = True,
        help_text = "Upload file with CSV or Excel format",
        write_only = True
    )

    class Meta:
        model = FileDocument
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def validate_file(self, value):
        allowed_types = ['.csv', '.xlsx', '.xls']
        file_extension = os.path.splitext(value.name)[1].lower()

        if file_extension not in allowed_types:
            raise serializers.ValidationError(
                f"Unsupported file type. Allowed types are: {', '.join(allowed_types)}"
            )

        max_file_size = 10 * 1024 * 1024  # 10 MB
        if value.size > max_file_size:
            raise serializers.ValidationError(
                "File size exceeds the maximum limit of 10 MB."
            )
        return value

class ProcessDataSerializer(serializers.Serializer):
    data = serializers.ListField(
        child = serializers.DictField(),
        required = True,
        help_text = "List of data records to be processed"
    )

    natural_language_input = serializers.CharField(
        required = True,
        max_length = 1000,
        help_text = "Complete natural language instruction：'Change the email address in the email column to \"REDACTED\"'"
    )


    def validate_data(self, value):
        if not value:
            raise serializers.ValidationError("Data list cannot be empty.")
        return value
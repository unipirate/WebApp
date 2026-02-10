from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .serializers import UpLoadFileSerializer, ProcessDataSerializer
from utils.file_parser import FileParser
from utils.llm_service import LLMService
from utils.regex_processor import RegexProcessor
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse

@api_view(['POST'])
def UploadFileView(request):
    try:
        serializer = UpLoadFileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Invalid file upload.',
                    'details': serializer.errors
                }, 
                status=400
            )
        
        uploaded_file = serializer.validated_data['file']

        file_data = uploaded_file.read()
        file_name = uploaded_file.name

        FileParser.validate_file(file_data, file_name)

        parsed_data = FileParser.parse_file(file_data, file_name)

        return Response(
            {
                'success': True,
                'file_name': file_name,
                'data': parsed_data['data'][:100],
                'columns': parsed_data['columns'],
                'row_count': parsed_data['row_count'],
                'column_count': parsed_data['column_count'],
            },
            status=200
        )
    except ValidationError as e:
        return Response(
            {
                'error': 'File validation failed.',
                'message': str(e)
            },
            status=400
        )
    except Exception as e:
        return Response(
            {
                'error': 'Server error during file upload.',
                'message': str(e)
            },
            status=500
        )

@api_view(['POST'])
def ProcessDataView(request):
    try:
        serializer = ProcessDataSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Invalid data for processing.',
                    'details': serializer.errors
                },
                status = 400
            )
        
        data = serializer.validated_data['data']
        natural_language_input = serializer.validated_data['natural_language_input']
        
        if not data or len(data) == 0:
            return Response(
                {
                    'error': 'Data list is empty.'
                },
                status = 400
            )
        
        available_columns = list(data[0].keys()) if len(data) > 0 else []
        
        llm_service = LLMService()
        regex_result = llm_service.generate_regex_pattern(
            natural_language_input,
            available_columns = available_columns
        )

        column = regex_result['column_name']
        regex_pattern = regex_result['regex_pattern']
        replacement_value = regex_result['replacement']
        pattern_description = regex_result.get('pattern_description', '') 
        
        if column not in available_columns:
            return Response(
                {'error': f"colum '{column}' does not exist in the data. Available columns: {', '.join(available_columns)}"},
                status = 400
            )

        processor = RegexProcessor()
        
        result = processor.process_data(
            data = data,
            column = column,
            regex_pattern = regex_pattern,
            replacement_value = replacement_value
        )

        return Response(
            {
                'success': True,
                'column_name': column,
                'pattern_description': pattern_description,
                'regex_pattern': regex_pattern,
                'processed_data': result['processed_data'],
                'state': result['state'],
                'replacement': replacement_value,
                'model_used': regex_result.get('model_used', 'unknown')
            },
            status = 200
        )

    except ValueError as e:
        return Response(
            {
                'error': 'Data processing error.',
                'message': str(e)
            },
            status=400
        )
    except Exception as e:
        return Response(
            {
                'error': 'Server error during data processing.',
                'message': str(e)
            },
            status=500
        )

def home(request):
    return HttpResponse("""
        <div style='text-align: center; padding-top: 50px; font-family: sans-serif;'>
            <h1>Backend is Live!</h1>
            <p>Django server is running perfectly on Render.</p>
            <p>Please access the <a href='https://web-app-silk-two.vercel.app/'>Frontend Here</a></p>
        </div>
    """)

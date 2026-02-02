import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Can not import Django."
            """If virtual environment is being used, 
            please activate it first by running: 
            source venv/bin/activate"""
        ) from exc
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

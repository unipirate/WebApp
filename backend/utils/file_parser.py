import pandas as pd
import numpy as np
import io
from typing import Dict, List, Any, Optional

class FileParser:
    SUPPORTED_EXTENSIONS = ['.csv', '.xlsx', '.xls']

    @staticmethod
    def parse_file(file_content: bytes,file_name: str)  -> Dict[str, Any]:
        file_extension = None
        for ext in FileParser.SUPPORTED_EXTENSIONS:
            if file_name.lower().endswith(ext):
                file_extension = ext
                break
        
        if not file_extension:
            raise ValueError("Unsupported file extension.")
        
        try:
            if file_extension == '.csv':
                try:
                    df = pd.read_csv(io.BytesIO(file_content), encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(io.BytesIO(file_content), encoding='latin1')
            else:
                df = pd.read_excel(io.BytesIO(file_content))
                
            ddf = df.replace([np.inf, -np.inf], np.nan)
            df = df.dropna(how='all')
            df = df.astype(object) 
            df = df.where(pd.notnull(df), "")
            
            columns = list(df.columns)
            data = df.to_dict('records')

            return {
                'data': data,
                'columns': columns,
                'row_count': len(df),
                'column_count': len(columns)
            }
        except Exception as e:
            raise ValueError(f"Error parsing file: {str(e)}")

    @staticmethod
    def validate_file(
        file_content: bytes, 
        file_name: str,
        max_size: int = 10 * 1024 * 1024
    ) -> bool:
        if len(file_content) > max_size:
            raise ValueError("File size exceeds the maximum limit.")
        
        file_extension = None
        for ext in FileParser.SUPPORTED_EXTENSIONS:
            if file_name.lower().endswith(ext):
                file_extension = ext
                break
        
        if not file_extension:
            raise ValueError("Unsupported file extension.")
        
        return True

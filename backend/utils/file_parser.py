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
                    df_preview = pd.read_csv(io.BytesIO(file_data), header=None, nrows=20, encoding='utf-8')
                except UnicodeDecodeError:
                    df_preview = pd.read_csv(io.BytesIO(file_data), header=None, nrows=20, encoding='gbk')
            else:
                df_preview = pd.read_excel(io.BytesIO(file_data), header=None, nrows=20)
                
            max_valid_cols = 0
            header_row_index = 0

            for i, row in df_preview.iterrows():
                valid_count = 0
                for cell in row:
                    cell_str = str(cell).strip()
                    if pd.notna(cell) and cell_str and 'unnamed' not in cell_str.lower():
                        valid_count += 1
                
                if valid_count > max_valid_cols:
                    max_valid_cols = valid_count
                    header_row_index = i
            
            columns = list(df.columns)
            data = df.to_dict('records')

            if file_extension == '.csv':
                try:
                    df = pd.read_csv(io.BytesIO(file_data), header=header_row_index, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(io.BytesIO(file_data), header=header_row_index, encoding='gbk')
            else:
                df = pd.read_excel(io.BytesIO(file_data), header=header_row_index)

            df.dropna(how='all', inplace=True)
            df.dropna(axis=1, how='all', inplace=True)
            df = df.fillna("")

            return {
                'data': df.to_dict(orient='records'),
                'columns': list(df.columns),
                'row_count': len(df),
                'column_count': len(df.columns)
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

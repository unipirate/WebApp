import re
from typing import Dict, List, Any

class RegexProcessor:
    @staticmethod
    def process_data(
        data: List[Dict[str, Any]], 
        column: str, 
        regex_pattern: str, 
        replacement_value: str
    ) -> Dict[str, Any]:
        if not data:
            raise ValueError("Data list is empty.")
        
        if column not in data[0]:
            raise ValueError(f"Column '{column}' does not exist in the data.")
        
        try:
            pattern = re.compile(regex_pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {str(e)}")
        
        processed_data = []
        match_count = 0
        replace_count = 0

        for row in data:
            new_row = row.copy()
            original_value = str(new_row.get(column, ""))
            if pattern.search(original_value):
                match_count += 1
                new_value = pattern.sub(replacement_value, original_value)
                new_row[column] = new_value
                if new_value != original_value:
                    replace_count += 1
            
            else:
                new_row[column] = original_value

            processed_data.append(new_row)

        return {
            "processed_data": processed_data,
            "state": {
                "total_rows": len(data),
                "matched_rows": match_count,
                "replaced_rows": replace_count,
                "unmatched_rows": len(data) - match_count
            },
            "regex_pattern": regex_pattern,
            "replacement_value": replacement_value
        }
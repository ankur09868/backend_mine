from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO

def process_subfile(file_path):
    
    print(f'Processing file: {file_path}')
    

    df = pd.read_excel(file_path)
    
    print('Columns in the sub-file:', df.columns.tolist())

    print('DataFrame contents:')
    print(df.to_string(index=False)) 

    return "Processing Complete"

@csrf_exempt
def create_subfile(request):
    if request.method == 'POST':
        input_file = request.FILES.get('input_file')
        columns_text = request.POST.get('columns')
        merge_columns = request.POST.get('merge_columns')  # Optional parameter for merging columns

        if not input_file:
            return JsonResponse({'error': 'Input file must be provided'}, status=400)

        
        # Load the Excel file into a DataFrame
        try:
            df = pd.read_excel(input_file)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        columns_dict = json.loads(columns_text) if columns_text else {}


        # Convert column indices to column names
        def get_column_names(df, indices):
            return [df.columns[i] for i in indices]

        # Merge columns if provided
        if merge_columns:
            try:
                merge_columns_dict = json.loads(merge_columns)  # Parse the JSON string into a dictionary
                print("something: " ,merge_columns_dict)
                for new_col, indices in merge_columns_dict.items():
                    if len(indices) != 2:
                        return JsonResponse({'error': 'Merge columns should be a list of two indices'}, status=400)
                    try:
                        col1, col2 = get_column_names(df, indices)
                        df[new_col] = df[col1].astype(str) +", "+ df[col2].astype(str)
                        df = df.drop([col1, col2], axis=1)  # Drop the original columns if desired
                        # columns_dict[new_col] = new_col
                        print("new col: " ,new_col)
                    except IndexError:
                        return JsonResponse({'error1': 'One or both column indices are out of range'}, status=400)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON format for merge_columns'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        # Apply column renaming if provided
        if columns_text:
            try:
                print("columns dict: " ,columns_dict)
                # Convert column indices to names for renaming
                columns_dict_with_names = {}
                for old_index, new_name in columns_dict.items():
                    try:
                        old_col = df.columns[int(old_index)]
                        columns_dict_with_names[old_col] = new_name
                    except IndexError:
                        return JsonResponse({'error': f'Column index {old_index} is out of range'}, status=400)
                df_sub = df.rename(columns=columns_dict_with_names)
                df_sub = df_sub[list(columns_dict.values()) + list(merge_columns_dict.keys())]

            except KeyError as e:
                return JsonResponse({'error': f'Column {e} not found in the input file'}, status=400)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON format for columns'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            # If no columns_dict provided, use all columns without renaming
            df_sub = df

        # Save the sub DataFrame to a new Excel file
        output_file = BytesIO()
        df_sub.to_excel(output_file, index=False)
        output_file.seek(0)

        processing_result = process_subfile(output_file)

        return JsonResponse({'message': f'Sub-file created and processed: {processing_result}'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

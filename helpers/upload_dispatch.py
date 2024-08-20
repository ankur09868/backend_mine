from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest,JsonResponse
import os, pandas as pd,json
from .vectorize import vectorize
from .table_from_img import data_from_image
from .upload_csv import upload_csv, upload_xls
from io import BytesIO


def create_subfile(df, columns_text, merge_columns):
    
    print("dataframe: " ,df.columns)
    columns_dict = json.loads(columns_text) if columns_text else {}

    def get_column_names(df, indices):
        return [df.columns[i] for i in indices]
    
    if merge_columns:
        try:
            merge_columns_dict = json.loads(merge_columns)  # Parse the JSON string into a dictionary
            print("something: " ,merge_columns_dict)
            for new_col, indices in merge_columns_dict.items():
                if len(indices) < 2:
                    return JsonResponse({'error': 'Merge columns should be a list of atleast two indices'}, status=400)
                try:
                    columns = get_column_names(df, indices)
                    df[new_col] = df[columns].astype(str).agg(', '.join, axis =1)
                    # df = df.drop([col1, col2], axis=1)  
                        
                    # print(f"{new_col}: " ,df[new_col])
                except IndexError:
                    return JsonResponse({'error1': 'One or more column indices are out of range'}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format for merge_columns'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


    if columns_text:
        try:
            print("columns dict: " ,columns_dict)
                
            columns_dict_with_names = {}
            for old_index, new_name in columns_dict.items():
                try:
                    old_col = df.columns[int(old_index)]
                    columns_dict_with_names[old_col] = new_name
                except IndexError:
                    return JsonResponse({'error': f'Column index {old_index} is out of range'}, status=400)
            df_sub = df.rename(columns=columns_dict_with_names)
            df_new = df_sub[list(columns_dict.values()) + list(merge_columns_dict.keys())]

        except KeyError as e:
            return JsonResponse({'error': f'Column {e} not found in the input file'}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format for columns'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        df_new = df
    print("files created")
    return df_new

@csrf_exempt
def dispatcher(request):
    print("rqst rcvsd")
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES.get('file')
        columns_text = request.POST.get('columns')
        merge_columns = request.POST.get('merge_columns')
        print("files rcvd")
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension == '.pdf':
            return vectorize(request)
            
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            return data_from_image(request)
        elif file_extension == '.csv':
            if not uploaded_file:
                return JsonResponse({'error': 'Input file must be provided'}, status=400)

            try:
                df = pd.read_csv(uploaded_file)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
            print("file rcvd")
            new_df = create_subfile(df, columns_text, merge_columns)

            return upload_xls(request, new_df)
        elif file_extension in ['.xls', '.xlsx']:
            if not uploaded_file:
                return JsonResponse({'error': 'Input file must be provided'}, status=400)

            try:
                df = pd.read_excel(uploaded_file)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
            print("file rcvd")
            new_df = create_subfile(df, columns_text, merge_columns)

            return upload_xls(request, new_df)
        else:
            return HttpResponseBadRequest('Unsupported file type.')
    else:
        return HttpResponseBadRequest('No file uploaded.')

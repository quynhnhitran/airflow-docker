import requests
import openpyxl
import pandas as pd
from collections import defaultdict
import re
import json

def read_file_excel(filepath):
    df = pd.read_excel(filepath, header=None, skiprows=1)
    category_dict = defaultdict(list)
    
    target_categories = [
        'Điện Thoại - Máy Tính Bảng', 
        'Thiết Bị Số - Phụ Kiện Số', 
        'Laptop - Máy Vi Tính - Linh kiện', 
        'Máy Ảnh - Máy Quay Phim'
    ]

    for index, row in df.iterrows():
        if row[0] in target_categories:  # Chỉ lấy dữ liệu cho các danh mục mục tiêu
            category_name = row[0]
            if row.dropna().iloc[-1]:  
                category_id = int(row.dropna().iloc[-1])
                category_dict[category_name].append(category_id)

    return category_dict

def get_products_limit_category(category_id):
    all_products = []
    page = 1

    while True:
        try:
            print(f'Get products for category {category_id}, page {page}')
            url = f'https://tiki.vn/api/v2/products?limit=40&category={category_id}&page={page}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
            }
            response = requests.get(url, headers=headers)
            data = response.json().get('data', [])

            if not data:
                break

            all_products.extend(data)
            page += 1

        except Exception as e:
            print(f"Error occurred while getting products for category {category_id}: {str(e)}")
            break

    return all_products

def save_products_to_json(products, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print(f"All Products saved to '{output_file}' successfully.")

def main():
    input_file = 'FullCategory.xlsx'
    category_dict = read_file_excel(input_file)

    for category_name, category_ids in category_dict.items():
        all_products = []
        for category_id in category_ids:
            products = get_products_limit_category(category_id)
            all_products.extend(products)

        clean_category_name = re.sub(r'[^\w\s]', '', category_name)
        output_file = f"{clean_category_name.strip().replace(' ', '_')}.json"
        save_products_to_json({'data': all_products}, output_file)

if __name__ == "__main__":
    main()
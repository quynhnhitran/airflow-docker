import json

def merge_category_files(output_file, categories_with_files):
    all_data = {
        "category": {}  # Khởi tạo trường category
    }

    for category, file in categories_with_files.items():
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data["category"][category] = {
                "products": data.get('data', [])  # Lưu danh sách sản phẩm dưới mỗi danh mục
            }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print(f"All categories merged into '{output_file}' successfully.")

    # Đếm số lượng sản phẩm trong mỗi danh mục
    count_products(all_data)

def count_products(all_data):
    for category, value in all_data["category"].items():
        product_count = 0  # Khởi tạo biến đếm
        for product in value["products"]:  # Duyệt qua từng sản phẩm
            product_count += 1  # Tăng đếm cho mỗi sản phẩm
        print(f"Category '{category}' has {product_count} products.")

if __name__ == "__main__":
    output_file = 'product_all.json'
    categories_with_files = {
        'Điện Thoại - Máy Tính Bảng': 'Điện_Thoại__Máy_Tính_Bảng.json',
        'Thiết Bị Số - Phụ Kiện Số': 'Thiết_Bị_Số__Phụ_Kiện_Số.json',
        'Laptop - Máy Vi Tính - Linh kiện': 'Laptop__Máy_Vi_Tính__Linh_kiện.json',
        'Máy Ảnh - Máy Quay Phim': 'Máy_Ảnh__Máy_Quay_Phim.json'
    }
    merge_category_files(output_file, categories_with_files)

import yaml
import argparse

def generate_aprilgrid_yaml(output_path, tag_rows, tag_cols, tag_size, tag_spacing):
    # 构建 YAML 数据
    config = {
        'target_type': 'aprilgrid',
        'tagCols': tag_cols,
        'tagRows': tag_rows,
        'tagSize': tag_size,
        'tagSpacing': tag_spacing
    }

    # 写入 YAML 文件
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✅ YAML 文件已成功生成：{output_path}")
    print(f"   参数配置：")
    print(f"     tagRows: {tag_rows}")
    print(f"     tagCols: {tag_cols}")
    print(f"     tagSize: {tag_size}")
    print(f"     tagSpacing: {tag_spacing}")

def main():
    parser = argparse.ArgumentParser(description="生成 AprilGrid 标定板的 YAML 配置文件")
    parser.add_argument('--output', '-o', type=str, required=True, help='输出 YAML 文件路径')
    parser.add_argument('--tag-rows', '-r', type=int, default=6, help='AprilGrid 的行数，默认 6')
    parser.add_argument('--tag-cols', '-c', type=int, default=6, help='AprilGrid 的列数，默认 6')
    parser.add_argument('--tag-size', '-s', type=float, default=0.0275, help='标签大小（米），默认 0.0275')
    parser.add_argument('--tag-spacing', '-p', type=float, default=0.3, help='标签间距比例（0~1），默认 0.3')

    args = parser.parse_args()

    generate_aprilgrid_yaml(
        output_path=args.output,
        tag_rows=args.tag_rows,
        tag_cols=args.tag_cols,
        tag_size=args.tag_size,
        tag_spacing=args.tag_spacing
    )

if __name__ == "__main__":
    main()
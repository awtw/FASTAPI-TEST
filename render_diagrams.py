#!/usr/bin/env python3
"""
将 diagrams.md 中的 Mermaid 图表渲染为图片
支持使用 mermaid.ink API 或本地 mermaid-cli
"""

import os
import re
import base64
import json
import urllib.parse
from pathlib import Path
import subprocess
import sys

def extract_mermaid_blocks(markdown_file):
    """从 Markdown 文件中提取所有 Mermaid 代码块"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 ```mermaid ... ``` 代码块
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    # 同时提取标题
    titles = []
    title_pattern = r'##\s+(\d+\.\s+.*?)\n\n```mermaid'
    title_matches = re.findall(title_pattern, content)
    
    diagrams = []
    for i, (title, code) in enumerate(zip(title_matches, matches), 1):
        diagrams.append({
            'index': i,
            'title': title.strip(),
            'code': code.strip()
        })
    
    return diagrams

def render_with_mermaid_ink(diagram_code, output_path):
    """使用 mermaid.ink API 渲染图表"""
    try:
        from urllib.request import urlopen, Request
        from urllib.error import URLError
        
        # 将代码编码为 base64
        encoded = base64.urlsafe_b64encode(diagram_code.encode('utf-8')).decode('utf-8')
        url = f"https://mermaid.ink/img/{encoded}"
        
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urlopen(req, timeout=30) as response:
            if response.status == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.read())
                return True
            else:
                print(f"  ❌ API 返回错误: {response.status}")
                return False
    except URLError as e:
        print(f"  ❌ 网络错误: {e}")
        return False
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def render_with_mmdc(diagram_code, output_path):
    """使用本地 mermaid-cli (mmdc) 渲染图表"""
    try:
        # 创建临时文件
        temp_file = output_path.with_suffix('.mmd')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(diagram_code)
        
        # 运行 mmdc
        result = subprocess.run(
            ['mmdc', '-i', str(temp_file), '-o', str(output_path), '-b', 'transparent'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 清理临时文件
        temp_file.unlink()
        
        if result.returncode == 0:
            return True
        else:
            print(f"  ❌ mmdc 错误: {result.stderr}")
            return False
    except FileNotFoundError:
        return None  # mmdc 未安装
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def render_diagrams(markdown_file, output_dir='docs/images', method='auto'):
    """渲染所有图表"""
    diagrams = extract_mermaid_blocks(markdown_file)
    
    if not diagrams:
        print("❌ 未找到 Mermaid 图表")
        return
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📊 找到 {len(diagrams)} 个图表\n")
    
    # 检查是否可以使用 mmdc
    use_mmdc = False
    if method in ['auto', 'mmdc']:
        try:
            subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
            use_mmdc = True
            print("✅ 检测到 mermaid-cli，将使用本地渲染\n")
        except (FileNotFoundError, subprocess.CalledProcessError):
            if method == 'mmdc':
                print("❌ mermaid-cli 未安装，请安装: npm install -g @mermaid-js/mermaid-cli\n")
                return
            else:
                print("⚠️  未检测到 mermaid-cli，将使用在线 API\n")
    
    success_count = 0
    for diagram in diagrams:
        index = diagram['index']
        title = diagram['title']
        code = diagram['code']
        
        # 生成文件名（使用标题中的数字和清理后的标题）
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        filename = f"{index:02d}-{safe_title}.png"
        output_file = output_path / filename
        
        print(f"[{index}/{len(diagrams)}] 渲染: {title}")
        print(f"  📁 输出: {output_file}")
        
        success = False
        if use_mmdc:
            result = render_with_mmdc(code, output_file)
            if result is True:
                success = True
            elif result is False:
                # mmdc 失败，尝试 API
                print("  ⚠️  mmdc 失败，尝试使用在线 API...")
                success = render_with_mermaid_ink(code, output_file)
        else:
            success = render_with_mermaid_ink(code, output_file)
        
        if success:
            print(f"  ✅ 成功\n")
            success_count += 1
        else:
            print(f"  ❌ 失败\n")
    
    print(f"\n{'='*50}")
    print(f"✅ 成功渲染: {success_count}/{len(diagrams)}")
    print(f"📁 图片保存在: {output_path.absolute()}")
    print(f"{'='*50}")

if __name__ == '__main__':
    markdown_file = Path('docs/diagrams.md')
    
    if not markdown_file.exists():
        print(f"❌ 文件不存在: {markdown_file}")
        sys.exit(1)
    
    # 检查命令行参数
    method = 'auto'
    if len(sys.argv) > 1:
        method = sys.argv[1]
        if method not in ['auto', 'api', 'mmdc']:
            print("用法: python render_diagrams.py [auto|api|mmdc]")
            sys.exit(1)
    
    render_diagrams(markdown_file, method=method)


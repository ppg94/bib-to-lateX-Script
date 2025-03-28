import re
import os

def parse_bib_file(bib_file_path):
    """解析BibTeX文件并返回格式化后的参考文献列表"""
    print(f"正在处理文件: {bib_file_path}")
    
    with open(bib_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = []
    seen_keys = set()
    
    # 解析每个条目
    pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\s*\}'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        fields_text = match.group(3)
        
        # 跳过重复条目
        if key in seen_keys:
            print(f"跳过重复条目: {key}")
            continue
            
        seen_keys.add(key)
        
        # 解析字段
        fields = {}
        field_pattern = r'(\w+)\s*=\s*\{(.*?)\}'
        field_matches = re.finditer(field_pattern, fields_text, re.DOTALL)
        
        for field_match in field_matches:
            name = field_match.group(1).lower()
            value = field_match.group(2).strip()
            value = clean_text(value)  # 清理Unicode字符
            fields[name] = value
        
        # 格式化参考文献
        formatted = format_reference(entry_type, key, fields)
        entries.append(formatted)
        
    print(f"已处理 {len(entries)} 个条目")
    return entries

def format_reference(entry_type, key, fields):
    """格式化参考文献条目"""
    # 基本信息
    title = fields.get('title', '').replace('{', '').replace('}', '')
    year = fields.get('year', '')
    
    # 处理作者
    authors = format_authors(fields.get('author', ''))
    
    # 初始化引用
    ref = f"\\bibitem{{{key}}}\n{authors},\n``{title},''"
    
    # 根据类型添加详细信息
    if entry_type == 'article':
        journal = fields.get('journal', '')
        volume = fields.get('volume', '')
        number = fields.get('number', '')
        pages = fields.get('pages', '')
        publisher = fields.get('publisher', '')
        
        ref += f"\nin \\emph{{{journal}}}"
        
        if volume:
            ref += f", vol. {volume}"
            
        if number:
            ref += f", no. {number}"
            
        if pages:
            ref += f", pp. {pages}"
            
        if publisher:
            ref += f", {publisher}"
            
        if year:
            ref += f", {year}"
            
    elif entry_type == 'inproceedings' or entry_type == 'conference':
        booktitle = fields.get('booktitle', '')
        pages = fields.get('pages', '')
        publisher = fields.get('publisher', '')
        
        ref += f"\nin \\emph{{{booktitle}}}"
        
        if pages:
            ref += f", pp. {pages}"
            
        if publisher:
            ref += f", {publisher}"
            
        if year:
            ref += f", {year}"
    
    else:
        # 默认处理
        venue = fields.get('journal', fields.get('booktitle', ''))
        if venue:
            ref += f"\nin \\emph{{{venue}}}"
            
        if year:
            ref += f", {year}"
    
    ref += "."
    return ref

def format_authors(author_str):
    """格式化作者列表"""
    if not author_str:
        return "Unknown"
        
    # 移除花括号
    author_str = author_str.replace('{', '').replace('}', '')
    authors = []
    
    # 处理每个作者
    for author in author_str.split(' and '):
        author = author.strip()
        
        # 跳过"others"
        if author.lower() == 'others':
            continue
            
        # 解析姓名
        if ',' in author:  # Last, First
            parts = author.split(',')
            last = parts[0].strip()
            first = parts[1].strip()

            initials = ''.join([n[0] + '.' for n in first.split() if n])
            authors.append(f"{initials} {last}")
        else:  # First Last
            names = author.split()
            if len(names) > 1:
                last = names[-1]
                first = names[:-1]
                
                # 获取首字母
                initials = ''.join([n[0] + '.' for n in first if n])
                authors.append(f"{initials} {last}")
            else:
                authors.append(author)
    
    return " and ".join(authors)

def clean_text(text):
    """清理文本中的特殊字符和Unicode"""
    replacements = {
        '≥': '>=',
        '≈': 'approx.',
        '−': '-',
        '–': '-',
        "'": "'",
        '"': '"',
        '"': '"',
        '…': '...',
        '≤': '<=',
        '²': '2',
        '³': '3'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    return text

def process_bib_file(input_file, output_file):
    """处理BibTeX文件并输出LaTeX参考文献"""
    if not os.path.exists(input_file):
        print(f"错误：找不到{input_file}文件")
        return

    references = parse_bib_file(input_file)
    

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\\begin{thebibliography}{99}\n\n")
        
        for ref in references:
            f.write(ref + "\n\n")
            
        f.write("\\end{thebibliography}\n")
    
    print(f"参考文献已写入{output_file}")
    

    with open(output_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        preview_lines = min(10, len(lines))
        preview = "".join(lines[:preview_lines])
        print(f"\n输出预览 (前{preview_lines}行):\n{preview}...")

def main():

    bib_file = "shuju.bib"
    output_file = "output.txt"

    process_bib_file(bib_file, output_file)
    
    print("\n处理完成！请检查输出文件。")

if __name__ == "__main__":
    main()
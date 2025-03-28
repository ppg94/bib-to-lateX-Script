# BibTeX 到 LaTeX 参考文献转换器

这个工具可以将 BibTeX 文件转换为 LaTeX 格式的参考文献列表。

## 功能特点

- 支持多种参考文献类型（article、inproceedings、conference 等）
- 自动处理作者名字格式
- 自动跳过重复条目
- 适用于中英文环境

## 使用方法

1. 将您的 BibTeX 文件命名为 `shuju.bib` 放在与程序相同的目录下
2. 运行 `python transport_fixed.py`
3. 程序会生成 `output.txt` 文件，包含格式化后的参考文献

## 注意事项

- 支持的字段：title、author、journal、booktitle、volume、number、pages、publisher、year
- 如果想处理其他文件名，可以修改脚本中的 `bib_file` 和 `output_file` 变量
- 作者支持 "Last, First" 和 "First Last" 两种格式

## 输出示例

```
\begin{thebibliography}{99}

\bibitem{smith2020example}
J. Smith and A.B. Jones,
``An example paper title,''
in \emph{Journal of Examples}, vol. 10, no. 2, pp. 100-110, Example Publisher, 2020.

\end{thebibliography}
``` 

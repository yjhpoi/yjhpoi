"""自动售货机工具函数模块。

该模块负责：
1. 从库存文件读取商品信息。
2. 将最新库存保存回库存文件。
3. 提供简单的输入解析辅助函数。
"""

from __future__ import annotations

from typing import Dict


def load_stock(file_path: str) -> Dict[str, int]:
    """从文本文件读取库存数据。

    文件格式约定（每行一条）：
        商品名,库存数量
    例如：
        可乐,10
        雪碧,8

    Args:
        file_path: 库存文件路径。

    Returns:
        dict: 键为商品名，值为库存数量（int）。

    Raises:
        FileNotFoundError: 文件不存在时抛出。
        ValueError: 文件内容格式不合法时抛出。
    """
    stock: Dict[str, int] = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.strip()

            # 跳过空行，避免因为手动编辑导致程序报错
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 2:
                raise ValueError(f"第 {line_no} 行格式错误，应为 '商品名,数量'：{line}")

            name = parts[0].strip()
            qty_text = parts[1].strip()

            if not name:
                raise ValueError(f"第 {line_no} 行商品名为空")

            try:
                qty = int(qty_text)
            except ValueError as exc:
                raise ValueError(f"第 {line_no} 行数量不是整数：{qty_text}") from exc

            if qty < 0:
                raise ValueError(f"第 {line_no} 行数量不能为负数：{qty}")

            stock[name] = qty

    return stock


def save_stock(file_path: str, stock: Dict[str, int]) -> None:
    """将库存字典保存到文本文件。

    Args:
        file_path: 库存文件路径。
        stock: 库存字典，键为商品名，值为库存数量。
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for name, qty in stock.items():
            f.write(f"{name},{qty}\n")


def parse_coin_input(text: str) -> int:
    """将用户输入的投币文本解析为整数金额。

    Args:
        text: 用户输入内容。

    Returns:
        int: 解析后的金额。

    Raises:
        ValueError: 输入不是整数时抛出。
    """
    return int(text.strip())

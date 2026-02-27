"""自动售货机核心类模块。"""

from __future__ import annotations

from typing import Dict

from utils import load_stock, save_stock


class VendingMachine:
    """自动售货机类。

    该类封装了自动售货机的主要行为：
    1. 读取库存
    2. 展示商品
    3. 处理购买流程（选商品、投币、出货找零）
    4. 更新并保存库存

    注意：
    - 本实现不使用 global 变量。
    - 所有状态都保存在类实例属性中。
    """

    VALID_COINS = {1, 5, 10}

    def __init__(self, stock_file: str):
        """初始化自动售货机。

        Args:
            stock_file: 库存文件路径。
        """
        self.stock_file = stock_file
        self.stock: Dict[str, int] = load_stock(stock_file)

    def show_products(self) -> None:
        """显示当前可选商品与库存。"""
        print("\n=== 当前商品列表 ===")
        for index, (name, qty) in enumerate(self.stock.items(), start=1):
            print(f"{index}. {name}（库存：{qty}，价格：5 元）")
        print("===================")

    def get_product_by_index(self, choice: int) -> str:
        """根据序号返回商品名称。

        Args:
            choice: 用户输入的商品序号（从 1 开始）。

        Returns:
            str: 商品名称。

        Raises:
            ValueError: 序号不在合法范围时抛出。
        """
        names = list(self.stock.keys())
        if choice < 1 or choice > len(names):
            raise ValueError("商品序号超出范围")
        return names[choice - 1]

    def check_stock(self, product_name: str) -> None:
        """检查指定商品库存是否充足。

        Args:
            product_name: 商品名称。

        Raises:
            ValueError: 库存不足时抛出。
        """
        if self.stock[product_name] <= 0:
            raise ValueError(f"抱歉，{product_name} 已售罄")

    def collect_money(self, price: int) -> int:
        """循环接收投币，直到金额达到商品价格。

        仅接受硬币面额：1、5、10。

        Args:
            price: 商品价格。

        Returns:
            int: 需要找零的金额。
        """
        total = 0

        while total < price:
            remain = price - total
            user_input = input(f"请投币（仅 1/5/10 元），还需 {remain} 元：")

            try:
                coin = int(user_input)
            except ValueError:
                print("输入无效：请只输入整数面额。")
                continue

            if coin not in self.VALID_COINS:
                print("不支持该面额，请投 1、5 或 10 元。")
                continue

            total += coin
            print(f"已投入：{total} 元")

        change = total - price
        return change

    def dispense(self, product_name: str) -> None:
        """执行出货并扣减库存。"""
        self.stock[product_name] -= 1
        print(f"\n正在出货：{product_name} ...")

    def save(self) -> None:
        """将当前库存写回文件。"""
        save_stock(self.stock_file, self.stock)

    def purchase(self, choice: int, price: int = 5) -> None:
        """执行一次完整购买流程。

        Args:
            choice: 商品序号。
            price: 商品价格，默认 5 元。
        """
        product_name = self.get_product_by_index(choice)
        self.check_stock(product_name)
        change = self.collect_money(price)
        self.dispense(product_name)
        self.save()

        print("购买成功，感谢使用！")
        if change > 0:
            print(f"找零：{change} 元")

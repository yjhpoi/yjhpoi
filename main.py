"""自动售货机程序入口。

运行方式：
    python main.py
"""

from __future__ import annotations

from machine import VendingMachine


def main() -> None:
    """主函数：创建售货机对象并驱动交互流程。"""
    stock_file = "stock.txt"

    try:
        vm = VendingMachine(stock_file)
    except FileNotFoundError:
        print(f"错误：未找到库存文件 {stock_file}。请先创建该文件。")
        return
    except ValueError as e:
        print(f"错误：库存文件内容不合法 -> {e}")
        return

    print("欢迎使用 Python 自动售货机！")
    vm.show_products()

    try:
        choice_text = input("请输入商品序号：")
        choice = int(choice_text)
        vm.purchase(choice)
    except ValueError as e:
        # 捕获用户输入错误、商品序号错误、库存不足等业务异常
        print(f"操作失败：{e}")
    except Exception as e:
        # 基础兜底异常处理，防止程序直接崩溃
        print(f"发生未知错误：{e}")


if __name__ == "__main__":
    main()

import pytest

# 执行标签
smoke = pytest.mark.smoke
dxts = pytest.mark.dxts

# 跳过标签
skipif = pytest.mark.skipif(1 == 1, reason="按照条件跳过")
skip = pytest.mark.skip(reason="跳过用例")
skip1 = pytest.mark.skip(reason="功能改造，跳过执行")

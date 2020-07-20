# 判決書格式轉換
## 使用方法
安裝套件
`
    pip install VerdictFormat
`

把正式格式轉成測試格式
```python
from VerdictFormat import Formal_to_Test
Formal_to_Test(Formal_format,output_path)
```

把測試格式轉成正式格式
```python
from VerdictFormat import Test_to_Formal
Test_to_Formal(Test_format,output_path)
```
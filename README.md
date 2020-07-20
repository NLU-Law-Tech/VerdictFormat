# 判決書格式轉換
## 使用方法
安裝套件
`
    pip install VerdictFormat
`

把正式格式轉成測試格式
```python
from VerdictFormat import Formal_to_Test
Formal_to_Test(Formal_format_path,output_path)
```

把測試格式轉成正式格式
```python
from VerdictFormat import Test_to_Formal
Test_to_Formal(Test_format_path,output_path)
```

Formal Format
```python
{
    "name": "姓名",
    "statuses": [
        {
          "status":"公務員", 
          "locations": 
          [
            {
              "field":"JFull",
              "start": 28, 
              "end":40
            }
          ]
        }
      ], 
    "positions": [
        {
          "work unit": "勞動部職業安全衛生署南部職業安全衛生中心",
          "title": "檢查員",
          "locations": 
          [
            {
              "field":"JFull",
              "start": 28, 
              "end":40
            }
          ]
        },
        {
          "work unit": "勞動部職業安全衛生署",
          "title": "職員",
          "locations": []
        }
      ],
    "laws": [
        {
          "act": "貪污治罪條例",
          "article": 4, 
          "paragraph":  1,
          "subparagraph": 2, 
          "locations": 
          [
            {
              "field":"JLaw",
              "start": 28, 
              "end":40
            }, 
            {
              "field":"JLaw",
              "start": 156, 
              "end":168
            }
          ]
        } 
      ]  
  }
  ```
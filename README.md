# AutoCatcher
자동으로 틀린그림찾기



### 파이썬 버전

3.9.10



### exe 만들기

https://wikidocs.net/21952

https://kwonkyo.tistory.com/534

를 참고했습니다.



실행파일 하나만 만들기

```
pyinstaller main.py -w -F -n autoCatcher
```

main.spec 열기

Analysis 위쪽에 ui = [('mainScreen.ui', '.')] 라고 쓰고 

```
Analysis(

...

datas=ui

...

)
```

로 고치기

그리고 다시 pyinstaller 실행

```
pyinstaller .\autoCatcher.spec
```


# 수정사항 (2021. 12. 09 목)

## WebODM 수정사항
* 사이드바 토글 형태로 수정
* 부트스트랩 버전 변경 3.3.1 -> 3.3.7
* 색상 변경
* 디자인 변경

## Windroneus 수정사항
* Maps.js 파일 수정
- iframe으로 WebODM 호출
- ↓↓↓ Maps.js 수정사항 ↓↓↓
- [Maps.js.txt](https://github.com/k3t7le/WebODM/files/7685358/Maps.js.txt)


<br><br>
# 실행 방법
* 수정 사항 실시간 반영을 위해 --dev 사용

```bash
git clone https://github.com/k3t7le/WebODM --config core.autocrlf=input --depth 1
cd WebODM
./webodm.sh start --dev
```

* 파일을 Docker 이미지 내의 저장소가 아닌 host filesystem에 저장하기 위해서는 media-dir 옵션 사용

```bash
cd WebODM
./webodm.sh start --dev --media-dir /c/IMG_DATA
```

<br><br>
# 테마 수정
기존 설치된 docker이미지가 있을 경우 테마가 적용 안될 수 있음 
아래와 같은 색상 구성이 아나면 테마 변경 필요

1. Administration -> Theme
![image](https://user-images.githubusercontent.com/61860152/145421175-6ba91bb3-2bb4-4f2d-a9df-86bc56edbc99.png)

2. 세부 수정 사항(필요시 테마 항목에서 직접 수정 필요)
<table>
<tr><td>Primary</td> <td>2C3E50</td></tr>
<tr><td>Secondary</td> <td>FFFFFF</td></tr>
<tr><td>Tertiary</td> <td>22147A</td></tr>
<tr><td>Button Primary</td> <td>005490</td></tr>
<tr><td>Button Default</td> <td>558DB5</td></tr>
<tr><td>Button Danger</td> <td>E74C3C</td></tr>
<tr><td>Header Background</td> <td>527A57</td></tr>
<tr><td>Header Primary</td> <td>FFFFFF</td></tr>
<tr><td>Border</td> <td>F4F4F4</td></tr>
<tr><td>Highlight</td> <td>EBECF1</td></tr>
<tr><td>Dialog Warning</td> <td>F39C12</td></tr>
<tr><td>Failed</td> <td>FFCBCB</td></tr>
<tr><td>Success</td> <td>CBFFCD</td></tr>
<tr><td>CSS</td> 
<td>
<pre>
body {
font-family: -apple-system
       , BlinkMacSystemFont
       , "Segoe UI"
       , Roboto, "Helvetica Neue"
       , Arial, "Noto Sans"
       , "Liberation Sans"
       , sans-serif
       , "Apple Color Emoji"
       , "Segoe UI Emoji"
       , "Segoe UI Symbol"
       , "Noto Color Emoji";
font-size: 1.3em;
}

.nav > li {
background-color: white;
}

.navbar-default .navbar-text {
color: #FFFFFF;
}
</pre>
</td>
</tr>
</table>


<br><br>
# Brand 수정
![image](https://user-images.githubusercontent.com/61860152/145426680-2e740480-c424-4505-a726-7480c13ffde9.png)


<br><br><br><br>
# 수정 후 화면
## WebODM 화면
![화면 캡처 2021-12-09 220615](https://user-images.githubusercontent.com/61860152/145403072-3172df31-9f06-4371-9b65-4a8c20683bad.png)
## Windroneus + WebODM 화면
![화면 캡처 2021-12-09 220644](https://user-images.githubusercontent.com/61860152/145403337-8f2031c6-c8b6-4c8a-ba88-b04ed9245c45.png)

<br><br>
# 오류 처리
## 글자가 겹쳐 보일 경우 
![image](https://user-images.githubusercontent.com/61860152/145431323-6d0732fa-b869-4b5a-b9c7-cf5a43333a6d.png)

브랜드 항목에서 App Logo 재 업로드
![image](https://user-images.githubusercontent.com/61860152/145431548-4f63c1d4-07fb-4a0e-b07f-24dd493db2af.png)

## 사이드바에 html script가 보일 때
![image](https://user-images.githubusercontent.com/61860152/145432190-611622ab-8f68-44c4-8af9-ba8e7cdab1e9.png)

Administration -> Plugin에서 posm-gcpi, lightning Disabled
![image](https://user-images.githubusercontent.com/61860152/145432406-0962dc26-8d0e-4c4a-9d2c-3dbaf32416ae.png)


<br><br>
# 제약 사항
FireFox에서만 정상 작동 Chrome, Edge의 경우 Cross site 관련되어 오류 발생 (로그인 실패)
![image](https://user-images.githubusercontent.com/61860152/145428216-5e282ce3-89ea-4967-986d-02a17a5aa62f.png)

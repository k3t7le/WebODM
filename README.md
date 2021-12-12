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

## Chrome, Edge 로그인 실패
Windroneus를 https 에서 http로 변경 (혹시 <b>Windroneus에서 https가 필수라면 알려주세요.</b>)

방법 : Windroneus 프로젝트 설정에서 Enable SSL 항목을 체크 해제 (추후 리눅스 서버에 설정할 때도 http로 설정)
![image](https://user-images.githubusercontent.com/61860152/145605336-8da69d6a-93bb-4e35-849e-1dd1497b89f2.png)



<br><br>
# 제약 사항
* Windroneus에 iframe으로 표시되기 때문에 Windorneus와 http or https를 동일하게 설정 필요(서버 http 프로토콜이 다를 경우 쿠키 관련 오류 발생)

<br><br>
# 수정사항 (2021. 12. 12 일)
## 정사이미지 생성 완료 후 정사이미지만 최상위 폴더에 복사 

`--media-dir /c/IMG_DATA`

![image](https://user-images.githubusercontent.com/61860152/145703527-90945df2-964f-41be-b2c6-de8b03037581.png)

![image](https://user-images.githubusercontent.com/61860152/145703799-0fe36297-5c83-4484-9185-27101b919ef6.png)

ODM_RESULT_IMG 폴더에 프로젝트명_날짜_시간.tif로 파일 저장 (라벨프로그램에서 리눅스 파일시스템 저장 이미지 사용할 경우 위 폴더의 데이터 사용)


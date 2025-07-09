# Raspberrypi_Study
라즈베리파이 관련 내용 정리
## 1일차 
### 라즈베리 파이 환경설정
- [vnc 설치](https://www.realvnc.com/en/connect/download/viewer/?lai_vid=MM1063K0RcJA&lai_sr=0-4&lai_sl=l)
- [sdcard format](https://www.sdcard.org/downloads/formatter/)
- [라즈베리파이 os](https://www.raspberrypi.com/software/)
#### 무선 와이파이 설정
라즈베리파이 OS 를 설치할 때 자동으로 공유기 주소를 잡아내지 못했다. 
무선으로 연결해주기 위해 아래와 같은 설정을 했다.
1. 모니터와 키보드, 마우스 라즈베리파이에 연결
2. 터미널 창을 열어 `wpa_supplicant.conf` 파일 수정
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
```
country=KR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="네트워크ID"
    psk="비밀번호"
    key_mgmt=WPA-PSK
}
```

3. Wi-Fi 서비스 재시작
```
sudo wpa_cli reconfigure
```
또는
```
sudo systemctl restart dhcpcd
```
4. 연결 상태 확인
```
iwgetid
```
```
ifconfig wlan0
```

#### GUI환경 - VNC 설정
1. 아래의 명령어로 설정 창 열기
```bash
> sudo raspi-config
```
2. Interface Options → VNC → <Yes> 메뉴 이동

3. `The VNC server is enabled` 메시지가 나오면 성공

4. `sudo reboot` 명령 입력, 종료 후 재부팅

**`vncserver-virtual`** 명령을 이용한 가상 데스크탑 생성
- 회색화면만 나오는 문제 발생
- 나중에 다시 시도해볼 것!

#### 한글 설정
언어 한글 선택시에 한글 폰트가 없어서 깨지는 현상 발생

한글 폰트 설치로 깨짐 해결
```bash
sudo apt update
sudo apt install fonts-nanum
```

#### 한글 입력기 설정
한글 폰트를 설치하더라도 기본적으로 한글 입력이 되지 않는다.
별도로 한글 입력기를 설치해주는 과정이 필요하다.
1. 터미널에서 아래의 명령어를 통해 입력기 설치
```
sudo apt install fcitx-hangul
```

2. 메뉴에서 "Fcitx 설정" 또는 "입력기 설정" 실행
    - 기본 입력기를 fcitx로 바꿔주기

3. Input Method 항목에서:
    - + 버튼 클릭
    - Korean - Hangul 추가

4. 환경변수 설정
```
`nano ~/.xprofile`
```
편집기에 아래의 내용 추가
```
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"
```
**📌한글 입력이 바로 안 되면 재부팅 또는 로그아웃 → 로그인 해보기**
#### 라즈베리파이 공유폴더 사용
1. samba 설치
```
sudo apt update
sudo apt install samba
```
2. 계정생성 (시스템 사용자와 동일한 계정이어야 함)
```
sudo smbpasswd -a {사용자명}
```
- Smba 사용자 목록 확인 방법: `sudo pdbedit -L`
3. 공유할 폴더 생성
```
mkdir -p /home/pknu62/piShare
```
```
sudo chown -R pknu62:pknu62 /home/pknu62/piShare
sudo chmod -R 777 /home/pknu62/piShare  # 테스트용
```
> 📌 실제 운영 시엔 777 대신 755나 770 등 적절한 권한 설정하기!
4. `/etc/samba/smb.conf` 파일 수정
```ini
[PiShare]
    path = /home/pknu62/piShare
    valid users = pknu62
    browseable = yes
    writable = yes              # 또는 read only = no
    create mask = 0777
    directory mask = 0777
    public = no                 # 보안상 yes 보단 no 권장
    guest ok = no               # 게스트 접근 비활성화
```
5. Samba 서비스 재시작
```
sudo systemctl restart smbd
```
6. win + R `\\192.168.0.x` 입력
Win + R → \\192.168.0.x 입력

인증창이 뜨면:

- 사용자명: `pknu62`
- 비밀번호: `smbpasswd` 명령으로 설정한 비번

7. 공유 폴더 생성 완료

- ⚠️ 접근 오류가 생기면:
    - 윈도우 방화벽: 파일 및 프린터 공유 허용 상태 확인
    - 폴더 권한: `sudo chmod -R 777 /home/pknu62/piShare` 등도 필요할 수 있음

<img src="./image/rasp0005.png" width=400>

🔴 에러사항
1. 동일 사용자 접속
<img src="./image/rasp0006.png" width=400>

- 해결방법
    - 기존 SMB 연결 끊기 (Windows에서) `net use * /delete`

2. 폴더경로 맞지 않음
<img src="./image/rasp0007.png" width=400>
- 해결방법
    - `nano /etc/samba/smb.conf` 에 적은 폴더경로와 실제 파일경로 확인
    - 홈디렉토리 경로: `/home/{사용자명}`


## 2일차
### 라즈베리파이 구조
<img src="./image/rasp0008.jpg" width=800>
출처 

### 직렬과 병렬 연결
#### 직렬연결
- 전류가 하나의 경로만 따라 흐르는 연결 방식
- 특징
    - 전류는 모든 소자에 동일하게 흐름
    - 전체 전압은 각 소자에 분배
    - 저항은 모두 더해짐
- LED 3개를 직렬으로 연결할 경우 마지막 LED는 전압 부족으로 불이 약할 수 있음


#### 병렬 연결
- 전류가 여러 갈래로 나뉘어 흐를 수 있는 연결 방식
- 특징
    - 전압은 모든 소자에 동일하게 걸림
    - 전체 전류는 갈래마다 나뉘어 흐름
    - 저항
- LED 두 개를 병렬로 연결하면, 각 LED는 같은 전압을 받고 밝기 차이가 없음

### 입력 회로 안정화 기법: Pull-up과 Pull-down
입력 핀(GPIO)은 입력이 "없을 때" 상태가 애매모호해지는 경우가 있다(플로팅 상태)
전압이 1 OR 0 이 아닌 떠 있는 상태 -> 노이즈나 오작동 발생
이것을 방지하기 위해 기본값을 강제로 0 또는 1로 고정해주는 안정화 기법이다.
#### 풀 업(Pull-up) 저항
- 기본 상태를 HIGH(1) 로 유지하고 싶을 때 사용
- 회로를 끊었을 때 입력이 자동으로 1이 되도록 함
#### 풀 업(Pull-down) 저항
- 기본 상태를 LOW(0) 로 유지하고 싶을 때 사용
- 회로를 끊었을 때 입력이 자동으로 0이 되도록 함

라즈베리파이에서는 내장 풀업/풀다운 저항 기능을 소프트웨어로 설정이 가능하다.
```
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
```

#### 키르호크 법칙

### 아날로그와 디지털
#### 아날로그
- 연속적인 값
#### 디지털
- 1 또는 0

0이 그라운드
5v 가 1

RPi.GPIO 모듈
GPIO.setemode(GPIO.BOARD)       # wPi
GPIO.setmode(GPIO.BCM)          # BCM
GPIO.setup(channel, GPIO.mode)  # 사용할 핀의 모드 설정(IN/OUT)
GPIO.cleanup()                  # 모든 핀 초기화 
GPIO.output(channel, state)     # HIGH(1) / LOW(0)
GPIO.input(channel)

#### 트렌지스터
#### RPi.GPIO
라즈베리파이의 GPIO 핀을 제어하는 파이썬 라이브러리
**기본 사용 흐름**
```
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)             # 핀 번호 모드 설정
GPIO.setup(17, GPIO.OUT)           # GPIO17 핀을 출력으로 설정
GPIO.output(17, GPIO.HIGH)         # GPIO17 핀에 3.3V 출력 → LED 켜짐
GPIO.cleanup()                     # 사용한 GPIO 핀 초기화
```
**주요 함수**
`GPIO.setmode()`: 핀 번호 체계 설정
    - GPIO.BCM: GPIO 이름 기준 (추천)
    - GPIO.BOARD: 핀 위치 기준

`GPIO.setup(pin, mode)`: 핀을 입력/출력으로 설정
`GPIO.output(pin, state)`: 출력 핀에  HIGH/LOW 전압 출력
`GPIO.input(pin)`: 입력 핀에서 값 읽기
`GPIO.cleanup():`: 설정 초기화(중복 실행 방지)


그라운드는 맨 마지막에 연결하기 


### 풀다운 저항
### 풀업 저항
풀다운저항?' 풀업저항
전류는 항상 낮은 전류로 가려는 성질이 있음
저항을 안 달아주면 그라운드로 전류가 흐를 수 있음
스위치를 누른다고해서 무조건 1이되는 것이 아님 저항이 어디있냐에 따라서 0일수도 1일 수도 있음


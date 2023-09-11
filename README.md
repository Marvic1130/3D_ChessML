# 3D 시공간 Chess 게임
**오리지널 스타트렉 TV 시리즈에 처음 등장했던 변형체스의 한 종류이다.
특이하게도 여러 개의 체스판이 3차원으로 배치되어있고, 그걸 통해서 체스게임을 하는 일종의 3차원 보드 게임.**

## 파트 분배
|개발자|담당 파트|개발환경 및 언어|
|:------:|:---:|:---:|
|최재욱|클라이언트|Unity, C#|
|이명재|백앤드|Sprignboot, Java|
|강예성|AI인공지능|Colab(임시), Python|

## 간단한 게임 설명
![image](https://github.com/3DimensionSpaceTime/WikiRepository/assets/56966606/f8b5c9ef-601d-4fec-b623-9b6adb06c48f)

**3차원 보드는 7개의 서로 다른 레벨로 구성됩니다. 이들 중 3개는 크기가 4 x 4이고 위치가 고정되어 있습니다.      
나머지 4개는 2x2크기이고 플레이어가 턴을 소모하여 특정 지정위치로 이동할 수 있습니다. 또한 같은 레벨에는 판이 존재 할수 없습니다.    
각 다음 레벨은 이전 레벨의 세 번째 행 위에서 시작하고 모든 고정된 레벨의 다른 측면은 평행합니다.    
이동식 레벨은 처음에는 상부 및 하부 레벨의 가장 바깥쪽 모서리 위에 위치합니다. 즉, 모서리 중 하나 아래에 보드 모서리가 있고 다른 세 모서리 아래에는 고정 레벨 보드가 없습니다.**   

![image](https://github.com/3DimensionSpaceTime/WikiRepository/assets/56966606/8260bc73-4feb-41b9-91cc-949f06d9a315)

**피스의 이동은 정통 체스의 이동과 유사하지만 두 가지 추가 규칙이 있습니다.       
첫째, 위에서 보드를 바라볼 때, 그 말은 가고 싶은 칸으로 정상적인 체스 이동을 할 수 있어야 합니다.   
둘째, 각 단계를 수행할 때마다 작품은 하나 이상의 레벨을 올리거나 내릴 수 있습니다. 여기서 레벨을 올리거나 내리는 것은 항상 이동 가능한 레벨에서 고정 레벨로 또는 그 반대로 가는 것을 의미합니다.**   

[출처 : chessvariants](https://www.chessvariants.com/3d.dir/startrek.html)

# Act1. 게임 개발 기획

<br>

## 초기 기획 

### **1. 기획 및 디자인**

#### 클라이언트 역할:
- 게임의 전체적인 UI/UX 디자인
- 게임 내 3D 체스 말 모델링 및 플레이어와 인게임 시점 조정
- 게임 규칙 및 플레이어 대 플레이어 간의 상호작용 정의
- 게임 규칙 및 플레이어 대 AI 간의 상호작용 정의

#### 백엔드 역할:
- 서버 아키텍처 및 기술 스택 결정
- 클라이언트와의 통신 방식 및 데이터 포맷 결정

### **2. 개발**

#### 클라이언트 역할:
- 게임 로직 구현 및 검수 (체스 규칙, 체크 및 체크메이트 판단 등)
- 사용자 인터페이스 및 게임 상태 업데이트 구현
- 서버와의 HTTP 통신을 위한 API 호출 구현

#### 백엔드 역할:
- 게임 로직 구현 및 검수 (체스 규칙, 체크 및 체크메이트 판단 등)
- 사용자 계정 관리 시스템 구현 (로그인, 회원가입, 프로필 관리 등)
- 온라인 멀티플레이어 매칭 로직 구현
- 게임 상태 및 결과 데이터 저장 및 관리

### **3. 테스트**

#### 클라이언트 역할:
- 빌드 파일의 동작 검수
- 게임 내 버그 및 이상 동작 테스트
- UI/UX 검토 및 수정
- 딜레이와 메모리 사용량 체크 (temp)  

#### 백엔드 역할:
- 서버 성능 테스트
- 데이터 일관성 및 보안 테스트
- 클라이언트와 서버 간의 통신 테스트

### **4. 배포 및 유지 보수**

### 클라이언트 역할:
- 게임 클라이언트의 배포 및 업데이트 관리
- 버그 수정 및 UI개선
- 확장성이 용이하도록 로직 검수 및 수정

### 백엔드 역할:
- 서버 배포 및 확장
- 데이터 백업 및 복구 전략 구현
- 서버 모니터링 및 오류 대응

### 기물 이동 시 작동 단계

다음은 유저가 체스 기물을 이동하려 할 때의 단계적 설계입니다:

### **1. 웹소켓 연결**

두 플레이어가 게임을 시작하면 각 클라이언트는 백엔드 서버에 웹소켓 연결을 초기화합니다. 이 연결은 게임 세션이 종료될 때까지 지속됩니다.

### **2. 기물 이동 요청**

플레이어가 기물을 이동하려고 선택하면, 해당 이동의 유효성을 클라이언트 측에서 먼저 확인할 수 있습니다. 이는 사용자 경험을 빠르게 만들기 위한 단계입니다.

유효한 이동이라 판단되면, 클라이언트는 웹소켓을 통해 백엔드 서버에 이동 요청을 보냅니다. 요청에는 현재 위치, 목표 위치, 선택된 기물 등의 정보가 포함됩니다.

### **3. 서버에서의 유효성 검사**

백엔드에서도 이동의 유효성을 다시 한 번 확인합니다. 이는 클라이언트의 잠재적인 조작이나 오류를 방지하기 위한 중요한 단계입니다.

멀티플레이 게임에서 클라이언트와 서버에서의 2중 검수로 동기화하여 확실한 정보를 가진 게임환경을 플레이어에게 제공하기 위함 입니다.

만약 이동이 유효하지 않다면, 오류 메시지를 해당 플레이어에게 웹소켓을 통해 전송합니다.

### **4. 상대 플레이어에게 정보 전달**

이동이 유효하다고 판단되면, 해당 정보를 상대 플레이어의 클라이언트에게 웹소켓을 통해 전달합니다. 상대 플레이어의 클라이언트는 이 정보를 기반으로 게임 보드를 업데이트합니다.

### **5. 게임 상태 업데이트**

서버는 게임의 현재 상태를 저장하고, 필요한 경우 이를 업데이트합니다. 예를 들어, 특정 기물이 상대 기물을 잡았거나 체크메이트 상황이 발생했을 때 등의 상황을 처리합니다.

### **6. 게임 종료 및 웹소켓 연결 종료**

게임이 종료되면, 두 플레이어에게 결과를 알리고 웹소켓 연결을 종료합니다.

이러한 과정을 통해 두 플레이어는 실시간으로 게임을 진행할 수 있습니다. 웹소켓의 장점은 데이터 교환에 있어서 지연 시간이 짧다는 것입니다. 따라서 플레이어는 거의 실시간으로 상대방의 움직임을 볼 수 있게 됩니다.

import pygame
import time
import copy
import random


class node:
    def __init__(self, Data):
        self.data = Data
        self.value = 0
        self.child = []

def AI(pane , p_len):
    # 공격 : 내 이어진 돌 개수의 최대값
    # 수비 : 상대 이어진 돌 개수 최대값
    # 최종 : max(공격점수 , 수비점수) 동점일경우 공격우선
    pane_cp = list(pane)
    vaild_poss = get_vaild_pos(0 , 1)
    
    root = node('root')
    for i in vaild_poss:
        temp = node([i])
        temp.value = get_score(pane_cp , i , p_len)
        root.child.append(temp)
        
    re = 0
    for child in root.child:
        re = max(child.value, re)
                
    result = []
    for child in root.child:
        if child.value == re:
            result.append(child.data[0])
            
    print('\nresult : ' , re)
    print('result : ' , result)
    print('\n')
    
    
#    return result[0]
    return result[random.randrange(0,len(result))]

#============================================================    

def get_score(pane, pos , p_len): #돌에대한 단편적인 보상 산출. 관찰자 관점이므로 모든 돌에 대한 보상임.

            
    ways = [[12,6],[9,3],[11,5],[1,7]]
    W_list = []
    B_list = []
    W_vhdd = [] #vertical , horizontal , diagonal_11_5 , diagonal_1_7
    B_vhdd = [] #
    
    color = 0
    for way1, way2 in ways: #[돌의개수 , 첫 번째 나오는 돌의 좌표 , 돌의개수 , 첫 번째 나오는 돌의 좌표]
        a , b = find_numof_dool(pane , p_len, copy.deepcopy(pos) , way1 , color, True)
        c , d = find_numof_dool(pane , p_len , copy.deepcopy(pos) , way2 , color, True)
        temp = [a,b,c,d]
        W_list.append(temp)
        
    color = 1
    for way1, way2 in ways: #[돌의개수 , 첫 번째 나오는 돌의 좌표 , 돌의개수 , 첫 번째 나오는 돌의 좌표]
        a , b = find_numof_dool(pane, p_len , copy.deepcopy(pos) , way1 , color, True)
        c , d = find_numof_dool(pane , p_len, copy.deepcopy(pos) , way2 , color, True)
        temp = [a,b,c,d]
        B_list.append(temp)

        
    for i in range(4):
#        B_list[i][1] 은 첫번쨰 방향으로 나오는 첫번째 검은돌
#        B_list[i][3] 은 두번쨰 방향으로 나오는 첫번째 검은돌
#      
#        W_list[i][0] 은 첫번쨰 방향으로 이어진 흰돌의 개수
#        W_list[i][2] 은 두번쨰 방향으로 이어진 흰돌의 개수
#        W_list[i][0] + W_list[i][2] 은 pos에 돌을 둠으로써 이어지는 흰돌의 개수, 즉 점수
        
#        B_list[i][1] 과 B_list[i][3] 은 모두 False가 아님

        
        distance1 = between_len(B_list[i][1] , pos) 
        distance2 = between_len(B_list[i][3] , pos)
        way1blocked = W_list[i][0]+1 == distance1 #첫번쨰 바로 방향이 막혀있는가? 
        way2blocked = W_list[i][2]+1 == distance2 #두번째 바로 방향이 막혀있는가?
        bet_distance = between_len(B_list[i][1] , B_list[i][3])
        
        
        if W_list[i][0] + W_list[i][2] >= 4: # AI승리로 게임을 끝낼 수 있는 경우
            W_vhdd.append(101)
            break
        
        if bet_distance < 6:
            W_vhdd.append(0)
            
        elif way1blocked or way2blocked:
            W_vhdd.append(W_list[i][0] + W_list[i][2] - 1)
        
        elif W_list[i][0]+2 == distance1 and W_list[i][2]+2 == distance2: #특수 케이스  ●x000x●
            W_vhdd.append(W_list[i][0] + W_list[i][2] - 1)
            
        else:
            W_vhdd.append(W_list[i][0] + W_list[i][2])
            
    for i in range(4):
#        W_list[i][1] 은 첫번쨰 방향으로 나오는 첫번째 흰돌
#        W_list[i][3] 은 두번쨰 방향으로 나오는 첫번째 흰돌
##        
#        B_list[i][0] 은 첫번쨰 방향으로 이어진 검은돌의 개수
#        B_list[i][2] 은 두번쨰 방향으로 이어진 검은돌의 개수
#        B_list[i][0] + B_list[i][2] 은 pos에 돌을 둠으로써 이어지는 검은돌의 개수, 즉 점수
        
#        W_list[i][1] 과 W_list[i][3] 은 모두 False가 아님
            
        distance1 = between_len(W_list[i][1] , pos) 
        distance2 = between_len(W_list[i][3] , pos)
        way1blocked = B_list[i][0]+1 == distance1 #첫번쨰 바로 방향이 막혀있는가? 
        way2blocked = B_list[i][2]+1 == distance2 #두번째 바로 방향이 막혀있는가?
        bet_distance = between_len(W_list[i][1] , W_list[i][3])
        
        
        if B_list[i][0] + B_list[i][2] >= 4: # 플레이어 승리로 게임을 끝낼 수 있는 경우
            B_vhdd.append(99)
            break
        
        if bet_distance < 6:
            B_vhdd.append(0)
            
        elif way1blocked or way2blocked:
            B_vhdd.append(B_list[i][0] + B_list[i][2] - 1)
        
        elif B_list[i][0]+2 == distance1 and B_list[i][2]+2 == distance2: #특수 케이스  ●x000x●
            B_vhdd.append(B_list[i][0] + B_list[i][2] - 1)
            
        else:
            B_vhdd.append(B_list[i][0] + B_list[i][2])
    
    total_max = max(max(W_vhdd)+0.5 , max(B_vhdd))
    
    if total_max < 98:
        vhdd = sorted(B_vhdd)
        vhdd.reverse()
        dis_F = 0.5
        for i in range(4):
            vhdd[i] = vhdd[i]*(dis_F**i)
        total_max += sum(vhdd)/20
    
    return total_max
    
def between_len(a,b): #거리는 두개 돌 사이의 빈 공간 개수를 의미
    ax = ord(a[0]) - 64
    ay = int(a[1:])
    bx = ord(b[0]) - 64
    by = int(b[1:])
    return max( abs(ax - bx) , abs(ay - by) )

def get_alldools(p_len):
    all_d = []   
    for i in range(65 , 65+p_len):
        for j in range(1,1+p_len):
            all_d.append(chr(i)+str(j))
    return list(all_d)



def get_vaild_pos(dool , mode):
    # mode 0 은  vaild_pos 갱신
    # mode 1 은  vaild_pos 갱신 , 리턴
    #유효한 계산범위 산출을 위한 작업
    global vaild_pos
    global all_dools
    
    length = 2
    
    if mode == 1:
        return list(vaild_pos)
    else:
        for Alpha in range( ord(dool[2][0])-length , ord(dool[2][0])+length + 1 ):
            for num in  range( int(dool[2][1:])-length , int(dool[2][1:])+length + 1 ):
                dom = chr(Alpha) + str(num)
                if dom in all_dools:
                    vaild_pos.append(dom)
                    all_dools.remove(dom)
        vaild_pos.remove(dool[2])

#==============================================================================

def printFont(string , color_tuple , size , pos_tuple):
    fontObj = pygame.font.Font('MaplestoryLight.ttf' , size)                  # 현재 디렉토리로부터 myfont.ttf 폰트 파일을 로딩한다. 텍스트 크기를 32로 한다
    textSurfaceObj = fontObj.render(string, True, color_tuple)   # 텍스트 객체를 생성한다. 첫번째 파라미터는 텍스트 내용, 두번째는 Anti-aliasing 사용 여부, 세번째는 텍스트 컬러를 나타낸다
    textRectObj = textSurfaceObj.get_rect();                      # 텍스트 객체의 출력 위치를 가져온다
    textRectObj.center = pos_tuple                               # 텍스트 객체의 출력 중심 좌표를 설정한다
    screen.blit(textSurfaceObj, textRectObj)                      # 설정한 위치에 텍스트 객체를 출력한다
    
def conv_board(pos, mode): #실제 바둑판 좌표와 가상좌표간 변환
    # mode == 0 인 경우는 A1좌표를 실제좌표로 변환
    # mode == 1 인 경우는 실제좌표를 A1좌표로 변환
    # mode == 2 인 경우는 사용자 입력좌표를 실제좌표로 변환
    position = [0,0]
    if mode == 0:
        position[0] = ord(pos[0]) - 64
        position[1] = int(pos[1:])
        
        position[0] = 30 + (position[0] - 1) * 50
        position[1] = 30 + (position[1] - 1) * 50
        return position
    elif mode == 1:
        position = ""
        position += chr(int((pos[0] - 30 + 50)/50) - 1 + 65)
        position += str(int((pos[1] - 30 + 50)/50) - 1 + 1)
        return position
    elif mode == 2:
        if ((pos[0] - 30)%50 <= 10 or (pos[0] - 30)%50 >= 40) and ((pos[1] - 30)%50 <= 10 or (pos[1] - 30)%50 >= 40):
            position[0] = int((pos[0] + 10 - 30)/50) * 50 + 30
            position[1] = int((pos[1] + 10 - 30)/50) * 50 + 30
            return position
        else:
            return 0
    
def is_end(pane, newdool , color , p_len): 
    #1이 흑돌 , 0이 백돌   newdool 은 A1형태  color은 0혹은1
    
    vertical = find_numof_dool(pane ,p_len, newdool , 12 , color , False) + find_numof_dool(pane,p_len , newdool , 6 , color, False)
    horizontal = find_numof_dool(pane,p_len , newdool , 9 , color, False) + find_numof_dool(pane ,p_len, newdool , 3 , color, False)
    diagonal_11_5 = find_numof_dool(pane,p_len , newdool , 11 , color, False) + find_numof_dool(pane ,p_len, newdool , 5 , color, False)
    diagonal_1_7 = find_numof_dool(pane,p_len , newdool , 1 , color, False) + find_numof_dool(pane ,p_len, newdool , 7 , color, False)
    
    if vertical >= 4 or horizontal >= 4 or diagonal_11_5 >= 4 or diagonal_1_7 >= 4:
        return True
    else:
        return False
 
def find_numof_dool(pane ,p_len ,start_pos , way , color , mode): 
    #start_pos는 A1 형태 , way는 12시 1시 3시 5시 6시 7시 9시 11시 
    first_dool = False
    num_dool = 0
    tikel_1 = 0
    tikel_2 = 0
    
    if way == 12:
        tikel_2 = -1
    elif way == 1:
        tikel_1 = 1
        tikel_2 = -1
    elif way == 3:
        tikel_1 = 1
    elif way == 5:
        tikel_1 = 1
        tikel_2 = 1
    elif way == 6:
        tikel_2 = 1
    elif way == 7:
        tikel_1 = -1
        tikel_2 = 1    
    elif way == 9:
        tikel_1 = -1
    elif way == 11:
        tikel_1 = -1
        tikel_2 = -1
    
    pos = [start_pos[0],int(start_pos[1:])]
    while 1: #어이진 돌의 개수 탐색
        pos[0] = chr(ord(pos[0]) + tikel_1)
        pos[1] = pos[1] + tikel_2
        if find_listin(pane , color ,  pos[0] + str(pos[1]) ):
            num_dool += 1
        else:
            break
        if num_dool >= 4:
            break
        
    pos = [start_pos[0],int(start_pos[1:])]
    pos[0] = ord(pos[0])
    for _ in range(p_len+2): # 가장 첫 번째로 나오는 돌 탐색
        pos[0] = pos[0] + tikel_1
        pos[1] = pos[1] + tikel_2
        if pos[0] >= 65+p_len or pos[1] >= 1+p_len or pos[0] <= 64 or pos[1] <= 0:
            first_dool = chr(pos[0]) + str(pos[1])
            break
        if find_listin(pane , color ,  chr(pos[0]) + str(pos[1]) ):
            first_dool = chr(pos[0]) + str(pos[1])
            break
        
    if mode:
        return num_dool , first_dool
    else:
        return num_dool
        
def find_listin(listt , color, pos):
    re = False
    for i in listt:
        if i[0] == color and i[2] == pos:
            re = True
            break
    return re
            
def restart_poses(pane_length , AI_first):
    if AI_first:
        vaild_pos = []
        temp = int((pane_length - 1)/2)
        for i in range(64 + temp ,64 + temp + 3):
            for j in range(temp , temp + 3):
                vaild_pos.append(chr(i)+str(j))
        
        all_dools = list(set(get_alldools(pane_length)) - set(vaild_pos))
    else:
        vaild_pos = []
        all_dools = get_alldools(pane_length)
    
    return vaild_pos , all_dools

def initialize():
    print('판의 크기를 선택하세요')
    print('1. 15x15')
    print('2. 13x13')
    size = input()
    

    while size != '1' and size != '2':
        print('\n1이나 2를 입력하세요')
        size = input()

    print('\n흑/백을 골라주세요')
    print('1. 흑돌')
    print('2. 백돌')
    color = input()

    while color != '1' and color != '2':
        print('\n1이나 2를 입력하세요')
        color = input()
        
    if size=='1':
        size = 15
    else:
        size = 13
    if color=='1':
        color = False
    else:
        color = True
    
    return size , color
#=========================================MAIN=======================================================================================


blackstone = pygame.image.load("black-go-stone48.png")
whitestone = pygame.image.load("white-go-stone48.png")

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (84, 77, 207)
PURPLE = (130, 0, 255)
RED = (255,0,0)
WRED = (253, 113, 91)
WBROWN = (255,191,0)
LEFT = 1 # 마우스 왼쪽 클릭


# 판의 크기는 무조건 13 or 15
pane_length = 0
# AI가 백인지 흑인지
AI_first = 0

pane_length , AI_first = initialize()
len_ftr = (pane_length - 13)*50




turn = 0

AI_color_RGB = 0
User_color_RGB = 0

AI_color_text =0
User_color_text =0

AI_color_img = 0
User_color_img = 0

if AI_first:
    turn = 0
    AI_color_text = '흑'
    AI_color_RGB = BLACK
    AI_color_img = blackstone
    User_color_text = '백'
    User_color_RGB = WHITE
    User_color_img = whitestone
else:
    turn = 1
    User_color_text = '흑'
    User_color_RGB = BLACK
    User_color_img = blackstone
    
    AI_color_text = '백'
    AI_color_RGB = WHITE
    AI_color_img = whitestone

    
    

pygame.init() 
width, height = 750 + len_ftr , 660 + len_ftr
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('SAKphago.v7')

vaild_pos , all_dools = restart_poses(pane_length,AI_first)

dool_list = []
text_list = []
lastdool = 0
enable_dool = True
game_end =  False
Quit = False
dool_inserted = False
timebowl = 0
NoWinner = False
while 1:
    if Quit:
        break
    #=========항상 실행되는 부분(화면, 턴 ,바둑돌 , 텍스트 표시)====
    time.sleep(0.01)
    # 5 - clear the screen before drawing it again
    screen.fill(WBROWN)
    # 6 - draw the 바둑판 가로 : 650 세로 : 520
    for i in range(30 , 631 + len_ftr , 50): # 세로
        pygame.draw.line(screen, BLACK, (i, 30), (i, 630 + len_ftr))
    for i in range(30 , 631 + len_ftr , 50):
        pygame.draw.line(screen, BLACK, (30, i), (630 + len_ftr, i))  
    if lastdool != 0:
        printFont('●' , WRED , 70  , (lastdool[1][0] , lastdool[1][1]))
    for color , R_pos , V_pos in dool_list:
        if color == 1: #color 1이 검은돌
            screen.blit(User_color_img, (R_pos[0] - 24 , R_pos[1] - 24) )
        else:
            screen.blit(AI_color_img, (R_pos[0] - 24 , R_pos[1] - 24) ) 
    
    for text , color , Fontsize , pos in text_list:
        printFont(text , color , Fontsize , pos )    
    if turn%2 == 1:
        printFont( User_color_text +' 차례' , User_color_RGB , 24 , (690 + len_ftr,40 + len_ftr))
        printFont('플레이어' , User_color_RGB , 20 , (690 + len_ftr,90+len_ftr))
        printFont('차례' , User_color_RGB , 20 , (690+len_ftr,120+len_ftr))
    else:
        printFont( AI_color_text+' 차례' , AI_color_RGB , 24 , (690+len_ftr,40+len_ftr))
        printFont('AI(컴퓨터)' , AI_color_RGB , 20 , (690+len_ftr,90+len_ftr))
        printFont('차례' , AI_color_RGB , 20 , (690+len_ftr,120+len_ftr))
        printFont('연산중...' , BLUE , 24 , (690+len_ftr,180+len_ftr))
        
    printFont('made by 이삭' , BLACK , 14 , (690+len_ftr,630+len_ftr))
    printFont('●' , RED , 14 , (330+len_ftr/2 ,330+len_ftr/2 ))
    
    #=======================승리조건 검사 및 게임 재시작============
    
    if game_end:
        if NoWinner:
            printFont('무승부' , PURPLE , 64 , (370+int(len_ftr/2),60+int(len_ftr/2)))
        else:
            if lastdool[0] == 1:
                printFont('게임종료 : 플레이어 승리!' , PURPLE , 64 , (370+int(len_ftr/2),60+int(len_ftr/2)))
            else:
                printFont('게임종료 : AI 승리!' , PURPLE , 64 , (370+int(len_ftr/2),60+int(len_ftr/2)))
        enable_dool = False
        printFont('화면을 클릭하면 새로운 게임이 시작됩니다' , PURPLE , 32 , (370+int(len_ftr/2),150+int(len_ftr/2)))
        
        if AI_first:
            turn = 0
        else:
            turn = 1
    #=======================AI 처리=================================
    enable_dool = turn%2 and (not game_end)
    
    
    if turn%2 == 0 and not game_end:
        if timebowl == 0:
            timebowl = time.time()
        if time.time() - timebowl > 0.5:        
            pos = AI(dool_list ,pane_length) #A1좌표
            poss = conv_board(pos , 0)
            
            lastdool = (0 , poss , pos )
            dool_list.append(lastdool)
            dool_inserted = True
            
            timebowl = 0
    
    #========================마우스 이벤트 처리=====================
    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            Quit = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: # 왼쪽 버튼이 눌렸을 때의 처리
            if game_end:
                game_end = False
                NoWinner = False
                dool_list = []
                text_list = []
                vaild_pos , all_dools = restart_poses(pane_length,AI_first)
                lastdool = 0
                

            if enable_dool:
                ppos = conv_board(list(event.pos) , 2)
                if ppos!=0 :
                    pppos = conv_board( ppos , 1)
                    if (( 0 , ppos , pppos ) not in dool_list) and (( 1  , ppos , pppos ) not in dool_list):
                        lastdool = (turn%2 , ppos , pppos )
                        dool_list.append(lastdool)
                        
                        dool_inserted = True
                        
                        
    #=======================바둑돌이 추가된 경우 처리===============
    if dool_inserted:
        get_vaild_pos(lastdool , 0)
        
        dfdf = 0
        if AI_first:
            dfdf = 1
        else:
            dfdf = 0
            
        if lastdool[0]==dfdf:
            text_list.append((  str( len(dool_list)) , BLACK , 16, lastdool[1] ))
        else:
            text_list.append((  str( len(dool_list)) , WHITE , 16, lastdool[1] ))
            
        game_end = is_end(dool_list , lastdool[2] , lastdool[0] , pane_length) or vaild_pos==[]
        if vaild_pos==[]:
            NoWinner = True
        dool_inserted = False
        turn += 1

                
                

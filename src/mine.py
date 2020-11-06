import time
import sys
import ctypes

#=======================================================
#RO41 課題4
#RO14A161 15 70002 矢倉天心
#３０秒間矢倉が作った壁の中で壁を検出すると向きを変えて走ります
# 注意：モーターが逆向きについてるのでマイナスで前進します
#=======================================================

# 接続開始
try:
    import sim
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')

print('Program started')
sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

# 接続できない場合
if clientID != -1:
    print('Connected to remote API server')
else:
    print('Failed connecting to remote API server')
    sys.exit('Program Ended')

# オブジェクトID取得
res, objs = sim.simxGetObjects(
    clientID, sim.sim_handle_all, sim.simx_opmode_blocking)
if res == sim.simx_return_ok:
    print('Number of objects in the scene: ', len(objs))
else:
    print('Remote API function call returned with error code: ', res)

time.sleep(2)

startTime = time.time()
sim.simxGetIntegerParameter(
    clientID, sim.sim_intparam_mouse_x, sim.simx_opmode_streaming)

# オブジェクトハンドラ初期化
# 前方センサ
res, FSensor = sim.simxGetObjectHandle(
    clientID, "FrontSensor", sim.simx_opmode_blocking)

# 左前方センサ
res, LFSensor = sim.simxGetObjectHandle(
    clientID, "Left_FSensor", sim.simx_opmode_blocking)

# 左後方センサ
res, LBSensor = sim.simxGetObjectHandle(
    clientID, "Left_BSensor", sim.simx_opmode_blocking)

# 右前方センサ
res, RFSensor = sim.simxGetObjectHandle(
    clientID, "Right_FSensor", sim.simx_opmode_blocking)

# 右後方センサ
res, RBSensor = sim.simxGetObjectHandle(
    clientID, "Right_BSensor", sim.simx_opmode_blocking)

# 左モーター
res, LMotor = sim.simxGetObjectHandle(
    clientID, "Lmotor", sim.simx_opmode_blocking)
# 右モーター
res, RMotor = sim.simxGetObjectHandle(
    clientID, "Rmotor", sim.simx_opmode_blocking)

# センサ値確認
if res != sim.simx_return_ok:
    print('Failed to get sensor Handler')
    sim.simxFinish(clientID)
    sys.exit('Program ended')

stepCount = 0

# センサ保存辞書
dic = {}

# センサ取得関数


def checkdistance():
    Fdist = sim.simxReadProximitySensor(
        clientID, FSensor, sim.simx_opmode_oneshot)

    LFdist = sim.simxReadProximitySensor(
        clientID, LFSensor, sim.simx_opmode_oneshot)

    LBdist = sim.simxReadProximitySensor(
        clientID, LBSensor, sim.simx_opmode_oneshot)

    RFdist = sim.simxReadProximitySensor(
        clientID, RFSensor, sim.simx_opmode_oneshot)

    RBdist = sim.simxReadProximitySensor(
        clientID, RBSensor, sim.simx_opmode_oneshot)

    for(symbol, val) in locals().items():
        dic[symbol] = val


def changevelocity(key):
    if key == "Fdist":
        print("cvero")
        sim.simxSetJointTargetVelocity(
            clientID, LMotor, 2.0, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            clientID, RMotor, -2.0, sim.simx_opmode_oneshot)
    elif key == "LFdist":
        sim.simxSetJointTargetVelocity(
            clientID, LMotor, -0.5, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            clientID, RMotor, 1.0, sim.simx_opmode_oneshot)
    elif key == "LBdist":
        sim.simxSetJointTargetVelocity(
            clientID, LMotor, -1.0, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            clientID, RMotor, -0.5, sim.simx_opmode_oneshot)
    elif key == "RFdist":
        sim.simxSetJointTargetVelocity(
            clientID, LMotor, 1.0, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            clientID, RMotor, -0.5, sim.simx_opmode_oneshot)
    elif key == "RBdist":
        sim.simxSetJointTargetVelocity(
            clientID, LMotor, -0.5, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            clientID, RMotor, -1.0, sim.simx_opmode_oneshot)
    else:
        time.sleep(0.005)
    time.sleep(0.05)


# Main loop
while time.time() - startTime < 30:
    returnCode, data = sim.simxGetIntegerParameter(
        clientID, sim.sim_intparam_mouse_x, sim.simx_opmode_buffer)  # Try to retrieve the streamed data

    checkdistance()
    # センサがtrueだったら車輪の回転を変える
    for (key, value) in dic.items():
        if value[1]:
            flag = True
            print(key, value)
            changevelocity(key)
            sim.simxSetJointTargetVelocity(
                clientID, LMotor, 1.0, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(
                clientID, RMotor, 1.0, sim.simx_opmode_oneshot)
        # else:
        #     print("else")
    sim.simxSetJointTargetVelocity(
        clientID, LMotor, -1.0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        clientID, RMotor, -1.0, sim.simx_opmode_oneshot)
print(time.time())
# 車輪止めて終了
sim.simxSetJointTargetVelocity(clientID, LMotor, 0, sim.simx_opmode_oneshot)
sim.simxSetJointTargetVelocity(clientID, RMotor, 0, sim.simx_opmode_oneshot)

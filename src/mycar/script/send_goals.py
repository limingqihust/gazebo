#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 上面两行不可省略，第一行是：告诉操作系统执行这个脚本的时候，调用 /usr/bin 下的 python 解释器。第二行是：定义编码格式 "UTF-8-" 支持中文
from actionlib.action_client import GoalManager
import rospy 
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
def send_goals_python():
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    #定义四个发送目标点的对象
    goal0 = MoveBaseGoal()
    goal1 = MoveBaseGoal() 
    goal2 = MoveBaseGoal() 
    goal3 = MoveBaseGoal()
    # 初始化四个目标点在 map 坐标系下的坐标,数据来源于《采集的目标点.docx》
    goal0.target_pose.pose.position.x = 1
    goal0.target_pose.pose.position.y = -1
    goal0.target_pose.pose.orientation.z = 0
    goal0.target_pose.pose.orientation.w = 1
    
    goal1.target_pose.pose.position.x = 1
    goal1.target_pose.pose.position.y = 1
    goal1.target_pose.pose.orientation.z = 0
    goal1.target_pose.pose.orientation.w = 1
    
    goal2.target_pose.pose.position.x = -1
    goal2.target_pose.pose.position.y = 1
    goal2.target_pose.pose.orientation.z = 0
    goal2.target_pose.pose.orientation.w = 1
    
    goal3.target_pose.pose.position.x = -1
    goal3.target_pose.pose.position.y = -1
    goal3.target_pose.pose.orientation.z = 0
    goal3.target_pose.pose.orientation.w = 1
    
    goal_lists=[goal0, goal1, goal2, goal3]       # 采用 python 中的列表方式，替代实现C/C++ 中的数组概念 
    goal_number = 4     # total is 4 goals
    for i in range(10):     
        goal_lists[i % 4].target_pose.header.frame_id = "map"
        goal_lists[i % 4].target_pose.header.stamp = rospy.Time.now()
        client.send_goal( goal_lists[i % 4])
        str_log = "Send NO. %s Goal !!!" %str(i % 4)
        rospy.loginfo(str_log)

        wait = client.wait_for_result(rospy.Duration.from_sec(30.0))  # 发送完毕目标点之后，根据action 的机制，等待反馈执行的状态，等待时长是：30 s.
        if not wait:
            str_log="The NO. %s Goal Planning Failed for some reasons" %str(i % 4)
            rospy.loginfo(str_log)
            continue
        else:
            str_log="The NO. %s Goal achieved success !!!" %str(i % 4)
            rospy.loginfo(str_log)
if __name__ == '__main__':
        rospy.init_node('mycar',anonymous=True)    # python 语言方式下的　初始化 ROS 节点，
        result = send_goals_python()
        rospy.loginfo(result)

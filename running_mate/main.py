import pose
import pose_clear

if __name__ == '__main__':
    # Todo : 해당 부분 날짜 + 시간으로 자동으로 input주고 output까지 자동화 진행 시키기
    # Todo : 드론에서 비디오 녹화 포맷 확인해서 Path 작성

    video_path = '../pose_input/11_5/11_5.mov'
    out_path = '../pose_output/video/11_5/11_5.avi'
    csv_path = '../pose_output/csv/11_5/11_5.csv'
    clear_out_path = '../pose_output/clear_video/11_5/11_5.mp4'

    pose.pose(video_path,out_path, csv_path)
    pose_clear.clear_pose(video_path, clear_out_path, csv_path)
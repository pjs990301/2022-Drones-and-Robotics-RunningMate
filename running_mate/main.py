import pose
import pose_clear

if __name__ == '__main__':

    video_path = '../pose_input/2022-11-05/11_5.mov'
    out_path = '../pose_output/video/2022-11-05/11_5.avi'
    csv_path = '../pose_output/csv/2022-11-05/11_5.csv'
    clear_out_path = '../pose_output/clear_video/2022-11-05/11_5.mp4'

    pose.pose(video_path,out_path, csv_path)
    pose_clear.clear_pose(video_path, clear_out_path, csv_path)
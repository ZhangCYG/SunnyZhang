# -*- coding: utf-8 -*-
# @Author: meng-zha
# @Date:   2020-07-15 11:40:12
# @Last Modified by:   meng-zha
# @Last Modified time: 2020-07-15 14:11:47

import open3d as o3d
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Time Alignment for Point Cloud')
    parser.add_argument("--data_path",default="/media/meng-zha/58b26bdb-c733-4c63-b7d9-4d845394a721/FuXiao_20200111/mid100_pcd/mid100_seq_10hz", type=str)
    parser.add_argument("--init_pos",default=[450,50,0,300],type=int,nargs='+')
    parser.add_argument("--amount",default=4,type=int)

    return parser.parse_args()


class Display(object):
    def __init__(self,data_path, position, amount):
        self.current_position = position
        self.path_number = amount
        self.data_path = data_path
        self.path = [data_path]*amount
        self.activated_path = 1

    def pre_process(self):
        points = []
        for i in range(self.path_number):
            self.path[i] = os.path.join(self.data_path, "FuXiao_"+str(i+1),
                                        "FuXiao_"+str(i+1)+"__"+str(self.current_position[i])+".pcd")
            # judge the exists of the path here
            points.append(o3d.io.read_point_cloud(self.path[i]))

        points[0].paint_uniform_color([254/254, 67/254, 101/254])  # FuXiao1 is red
        points[1].paint_uniform_color([249/254, 205/254, 173/254])  # FuXiao2 is yellow
        points[2].paint_uniform_color([131/254, 175/254, 155/254])  # FuXiao3 is green
        points[3].paint_uniform_color([38/254, 188/254, 213/254])  # FuXiao4 is blue
        result = points[0] + points[1] + points[2] + points[3]
        print("Read point cloud")
        print(f'The current position:{self.current_position}')
        return result

    def draw_geometry_with_key_callback(self):

        def move_next_100_simul(vis):
            for i in range(self.path_number):
                self.current_position[i] = self.current_position[i] + 100
            points = self.pre_process()
            vis.clear_geometries()
            vis.add_geometry(points)
            vis.poll_events()
            vis.update_renderer()

        def move_pre_100_simul(vis):
            for i in range(self.path_number):
                self.current_position[i] = self.current_position[i] - 100
            points = self.pre_process()
            vis.clear_geometries()
            vis.add_geometry(points)
            vis.poll_events()
            vis.update_renderer()

        def free_choose_frame(vis):
            # Some bugs here, maybe from the input cache.
            # If you use the "p" for choose for the first operation after 
            # the start of the Display, the panel will break down.
            i, j = map(int, input("input your choice of path and frame for subsequent operation: ").strip().split())
            self.activated_path = i
            self.current_position[i-1] = j
            print("Next frame is FuXiao_", self.activated_path, " ", self.current_position[i-1], "pcd")
            points = self.pre_process()
            vis.clear_geometries()
            vis.add_geometry(points)
            vis.poll_events()
            vis.update_renderer()

        def activate_path(vis):
            self.activated_path = int(input("input your choice of path for subsequent operation: "))
            print(f"Activate LiDar {self.activated_path}")

        def dropout(vis):
            print("\nDisplay finished\n")
            exit(0)

        def move_next_10_for_activated_path(vis):
            self.current_position[self.activated_path-1] = self.current_position[self.activated_path-1] + 10
            points = self.pre_process()
            vis.clear_geometries()
            vis.add_geometry(points)
            vis.poll_events()
            vis.update_renderer()
            print(f'The current position:{self.current_position}')

        def move_pre_10_for_activated_path(vis):
            self.current_position[self.activated_path-1] = self.current_position[self.activated_path-1] - 10
            points = self.pre_process()
            vis.clear_geometries()
            vis.add_geometry(points)
            vis.poll_events()
            vis.update_renderer()
            print(f'The current position:{self.current_position}')

        def move_next_for_activated_path(vis):
            self.current_position[self.activated_path-1] = self.current_position[self.activated_path-1] + 1
            points = self.pre_process()
            vis.clear_geometries()
            vis.add_geometry(points,reset_bounding_box=False) # keep current viewpoint
            vis.poll_events()
            vis.update_renderer()
            print(f'The current position:{self.current_position}')

        def move_pre_for_activated_path(vis):
            self.current_position[self.activated_path-1] = self.current_position[self.activated_path-1] -1
            points = self.pre_process()
            vis.clear_geometries()
            vis.add_geometry(points)
            vis.poll_events()
            vis.update_renderer()
            print(f'The current position:{self.current_position}')

        points = self.pre_process()
        vis = o3d.visualization.VisualizerWithKeyCallback()
        vis.create_window()
        vis.add_geometry(points)

        # Router
        while True:
            vis.poll_events()
            vis.update_renderer()

            vis.register_key_callback(ord("."), move_next_100_simul)
            vis.register_key_callback(ord(","), move_pre_100_simul)
            vis.register_key_callback(ord("O"), dropout)
            vis.register_key_callback(ord("P"), free_choose_frame)
            vis.register_key_callback(ord("A"), activate_path)
            vis.register_key_callback(ord("E"), move_next_10_for_activated_path)
            vis.register_key_callback(ord("W"), move_pre_10_for_activated_path)
            vis.register_key_callback(ord("S"), move_pre_for_activated_path)
            vis.register_key_callback(ord("D"), move_next_for_activated_path)


if __name__ == '__main__':
    args = parse_args()
    print(args)
    assert(args.amount == len(args.init_pos))
    demo = Display(args.data_path,args.init_pos,args.amount)
    demo.draw_geometry_with_key_callback()

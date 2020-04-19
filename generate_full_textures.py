import os
import sys
import pygame


def generate_full_textures(dir):

    texture_items = {}

    # if dir exiss
    if os.path.exists(dir):
        # print("Dir exists")
        subfolders_names = [f.name for f in os.scandir(dir) if f.is_dir()]
        # print(subfolders_names)

        # only straight angles
        directions = ["left", "right", "up", "down"]
        # could be more

        for folder_name in subfolders_names:
            folder_path = os.path.join(dir, folder_name)

            if folder_name in directions:

                texture_items[folder_name] = []
                # print("-----------")
                # print("Folder path: " + folder_path)

                # print("Folder name: " + folder_name)
                current_folder_texture_paths = []

                for r, d, f in os.walk(folder_path):
                    for file in f:

                        texture_path = os.path.join(r, file)
                        current_folder_texture_paths.append(texture_path)

                        texture = pygame.image.load(texture_path)
                        texture_items[folder_name].append(texture)

                # print(texture_items[folder_name])
                # print(current_folder_textures)

    # print(texture_items)

    return texture_items


# mario_textures = generate_full_textures(os.path.join("src", "mario_textures"))
# print(mario_textures)

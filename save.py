from settings import FILENAME


class Save:

    def __init__(self):

        self.path = f"../saves/{FILENAME}.txt"

    def push_to_save(self, x_info: int, y_info: int):
        
        with open(self.path, "w") as file:
    
            info = [x_info, y_info]
            file.writelines(str(info))
        
        file.close()
    
    def pull_from_save(self):

        x_info = 384
        y_info = 320

        try:

            with open(self.path, "r") as file:

                content = file.read().split()

                if len(content) >= 2:
                    
                    x_info = content[0].replace("[", "")
                    x_info = x_info.replace(",", "")
                    y_info = content[1].replace("]", "")
                    
                    return x_info, y_info
                
                else:
                    
                    return x_info, y_info
        
        except FileNotFoundError:

            return x_info, y_info

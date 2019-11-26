class UIFactory:

    @staticmethod
    def AddFileExtension(path, ext):
        fileName = path

        if not path.endswith(ext):
            fileName += ext

        return fileName

    @staticmethod
    def TruncatePath(path, length, invert = False, test = None):
        if len(path) > length:
            stringOffset = len(path) - length
            trunc = "..."
        else:
            stringOffset = 0
            trunc = ""

        if invert:
            result = path[:stringOffset] + trunc
        else:
            result = trunc + path[stringOffset:]

        return result

    @staticmethod
    def ScrollBinding(container, scrollableCanvas, child, subInterface = False):
        child.bind("<Configure>", lambda event : UIFactory.SetScrollRegion(root = scrollableCanvas, child = child))
        
        if not subInterface:
            container.bind('<Enter>', lambda event : UIFactory.BindMouseToScroll(root = scrollableCanvas))
            container.bind('<Leave>', lambda event : UIFactory.UnbindMouseFromScroll(root = scrollableCanvas))

    @staticmethod
    def BindMouseToScroll(root):
        root.bind_all("<MouseWheel>", lambda event : UIFactory.MouseScroll(event = event, root = root))

    @staticmethod
    def UnbindMouseFromScroll(root):
        root.unbind_all("<MouseWheel>") 

    @staticmethod
    def MouseScroll(event, root):
        root.yview_scroll(int(-1*(event.delta/120)), "units")

    @staticmethod
    def SetScrollRegion(root, child):
        root.configure(scrollregion = root.bbox("all"))
        root.yview_moveto(0)
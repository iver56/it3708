class NeatNetWrapper(object):
    def __init__(self, net):
        self.net = net

    def activate(self, input_values):
        self.net.Input(list(input_values))
        self.net.Activate()
        return list(self.net.Output())

class InfoObject:

    data = []
    placement = ''
    posX = ''

    field1 = ''
    field2 = ''

    def __init__(self, data):
        self.data = data

    def countCols(self):
        return len(self.data)

    def countRows(self):
        rows = 0
        for i, x in enumerate(self.data):
            rows = i + 1
        return rows

    def getPlacement(self):
        return self.placement

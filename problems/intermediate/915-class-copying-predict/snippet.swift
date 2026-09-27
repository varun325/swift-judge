final class Box { var value: Int; init(_ v: Int) { value = v } }
struct Cell { var value: Int }

let boxes = [Box(1), Box(2)]
var boxesCopy = boxes
boxesCopy[0].value = 100
boxesCopy.append(Box(3))

let cells = [Cell(value: 1), Cell(value: 2)]
var cellsCopy = cells
cellsCopy[0].value = 100

print(boxes.map(\.value), boxesCopy.map(\.value))
print(cells.map(\.value), cellsCopy.map(\.value))
print(boxes[0] === boxesCopy[0], boxes.count, boxesCopy.count)

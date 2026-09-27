final class Room { var name = "lobby" }
final class House { var room: Room? }

let house = House()
let r1: Void? = (house.room?.name = "kitchen")
print(r1 == nil ? "not assigned" : "assigned")
house.room = Room()
let r2: Void? = (house.room?.name = "kitchen")
print(r2 == nil ? "not assigned" : "assigned", house.room?.name ?? "-")

var scores = ["ana": [1, 2]]
scores["ana"]?.append(3)
scores["bo"]?.append(9)
print(scores["ana"]!, scores["bo"] as Any)

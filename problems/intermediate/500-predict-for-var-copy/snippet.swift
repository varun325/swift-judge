struct Player { var score: Int }
final class Box { var score: Int; init(_ s: Int) { score = s } }

var players = [Player(score: 1), Player(score: 2)]
for var p in players { p.score *= 10 }
print(players.map(\.score))

for i in players.indices { players[i].score *= 10 }
print(players.map(\.score))

let boxes = [Box(1), Box(2)]
for b in boxes { b.score *= 10 }
print(boxes.map(\.score))

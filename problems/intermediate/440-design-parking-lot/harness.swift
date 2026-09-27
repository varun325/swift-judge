struct __Input: Decodable { let ops: [String]; let args: [[Int]] }

 func __run(_ __i: __Input) async throws -> [Bool?] {
     var lot: ParkingLot?
     var out: [Bool?] = []
     for (op, args) in zip(__i.ops, __i.args) {
         if op == "init" {
             lot = ParkingLot(big: args[0], medium: args[1], small: args[2])
             out.append(nil)
         } else {
             out.append(lot!.park(args[0]))
         }
     }
     return out
 }
